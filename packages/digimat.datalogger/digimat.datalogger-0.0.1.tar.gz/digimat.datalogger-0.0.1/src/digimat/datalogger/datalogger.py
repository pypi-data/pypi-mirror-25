from __future__ import print_function  # Python 2/3 compatibility

import time
import datetime
import os
import uuid
import glob
import random
import logging

from threading import RLock
from threading import Event
from threading import Thread

import gzip
import cStringIO

# pip install pytz
from pytz import UTC

# pip install python-dateutil
import dateutil.parser

# pip install tzlocal
import tzlocal


class Record(object):
    def __init__(self, name, value, stamp=None, unit=None, flags=None):
        self._name=name
        self._value=self.load(value)
        self._stamp=stamp
        self._unit=unit
        self._flags=set()
        self.setFlags(flags)

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def stamp(self):
        return self._stamp

    @property
    def unit(self):
        return self._unit

    @property
    def flags(self):
        return self._flags

    def load(self, value):
        return value

    def hasFlags(self, flags):
        """check if the given flags is a subset of the actual record.flags set"""
        try:
            if set(flags.upper())<=self._flags:
                return True
        except:
            pass

    def setFlags(self, flags):
        try:
            self._flags.update(set(flags.upper()))
        except:
            pass

    def checkForFlagsDifference(self, flags):
        try:
            if not flags and not self._flags:
                return False

            if self._flags.symmetric_difference(set(flags.upper())):
                return True
        except:
            pass

    def getElapsedTime(self, stamp):
        try:
            return (stamp-self._stamp).total_seconds()
        except:
            pass

    def isElapsed(self, stamp, seconds):
        if seconds is not None:
            if self.getElapsedTime(stamp)>=seconds:
                return True

    def valueAsString(self):
        return str(self.value)

    def stampAsString(self):
        dtutc=self.stamp.astimezone(tz=UTC)
        return dtutc.isoformat()

    def unitAsString(self):
        return self.unit or ''

    def flagsAsString(self):
        return ''.join(self.flags)

    def toString(self):
        data=[self.name,
            self.stampAsString(),
            self.valueAsString(),
            self.unitAsString(),
            self.flagsAsString()]
        return ';'.join(data)

    @classmethod
    def fromString(cls, sdata):
        try:
            (name, stamp, value, unit, flags)=sdata.split(';')
            dt=dateutil.parser.parse(stamp)
            if name and dt and value:
                return cls(name=name, stamp=dt, value=value, unit=unit, flags=flags)
        except:
            pass


class RecordFloat(Record):
    def load(self, value):
        try:
            return float(value)
        except:
            pass

    def isDelta(self, value, delta):
        try:
            if delta is not None:
                if abs(value-self._value)>=delta:
                    return True
        except:
            pass


class SpoolerChild(object):
    def __init__(self, maxrefs=0):
        self._maxrefs=maxrefs
        self._spoolers=[]

    @property
    def spooler(self):
        try:
            return self._spoolers[0]
        except:
            pass

    def isAttached(self):
        if self._spoolers:
            return True

    def isAlive(self):
        return False

    @property
    def logger(self):
        if self.isAttached():
            return self.spooler.logger

    def isStopped(self):
        if self.spooler.isStopped():
            return True

    def attach(self, spooler):
        if spooler and isinstance(spooler, Spooler) and spooler not in self._spoolers:
            if self._maxrefs==0 or len(self._spoolers)<self._maxrefs:
                self._spoolers.append(spooler)
                return True

    def detach(self, spooler):
        if spooler and spooler in self._spoolers:
            try:
                while self.isAlive():
                    time.sleep(0.1)
                self._spoolers.remove(spooler)
                return True
            except:
                pass


class Provider(SpoolerChild):
    def __init__(self, name, rtype, unit=None, timeTrigger=None, inhibitTime=5, tz=None):
        super(Provider, self).__init__(maxrefs=0)

        assert issubclass(rtype, Record)

        self._name=name.strip()
        self._rtype=rtype
        self._lastRecord=None
        self._tz=tz or tzlocal.get_localzone()
        self._unit=unit
        self._timeTrigger=timeTrigger
        self._inhibitTime=inhibitTime
        self._timeoutInhibit=0

    @property
    def name(self):
        return self._name

    @property
    def unit(self):
        return self._unit

    def setInhibitTime(self, delay):
        self._inhibitTime=delay

    def setTimeTrigger(self, delay):
        self._timeTrigger=delay

    def now(self):
        return datetime.datetime.now(tz=self._tz)

    def isTriggerForStamp(self, dt):
        try:
            if self._lastRecord.isElapsed(dt, self._timeTrigger):
                return True
        except:
            pass

    def isTriggerForValue(self, value):
        return False

    def isTriggerForUnit(self, unit):
        try:
            if unit is not None and self._lastRecord.unit!=unit:
                return True
        except:
            pass

    def isTriggerForFlags(self, flags):
        try:
            if self._lastRecord.checkForFlagsDifference(flags):
                return True
        except:
            pass

    def updateValue(self, value, dt=None, unit=None, flags=None):
        if not self.isAttached():
            return
        if self._inhibitTime>0 and time.time()<self._timeoutInhibit:
            return

        dt=dt or self.now()
        unit=unit or self._unit

        update=False
        if not self._lastRecord:
            update=True
        elif self.isTriggerForStamp(dt):
            update=True
        elif self.isTriggerForUnit(unit):
            update=True
        elif self.isTriggerForFlags(flags):
            update=True
        elif self.isTriggerForValue(value):
            update=True

        if update:
            self._timeoutInhibit=time.time()+self._inhibitTime
            record=self._rtype(self.name, value, dt, unit, flags)
            self._lastRecord=record
            for spooler in self._spoolers:
                spooler.spool(record)


class Dispatcher(SpoolerChild):
    def __init__(self, name, *args, **kwargs):
        super(Dispatcher, self).__init__(maxrefs=1)

        assert name
        self._name=name.strip()
        self._stampDispatch=0
        self._timeoutInhibitDispatch=0
        self._delayInhibitDispatch=900
        self._eventDispatching=Event()
        self._threadDispatch=None

        self.onInit(self, *args, **kwargs)

    @property
    def name(self):
        return self._name

    def onInit(self, *args, **kwargs):
        pass

    def setDispatchInhibitDelay(self, delay):
        self._delayInhibitDispatch=int(delay)

    def getStoragePath(self):
        if self.isAttached():
            return self.spooler.getStoragePath(self.name)

    def getJobs(self):
        try:
            if self.isAttached():
                files=glob.glob(os.path.join(self.getStoragePath(), '*.datalogger'))
                random.shuffle(files)
                return files
        except:
            pass

    def removeJob(self, fpath):
        try:
            os.remove(fpath)
            self.logger.info('%s:job %s deleted' % (self.name, fpath))
        except:
            pass

    def removeJobs(self, files):
        for fpath in files:
            self.removeJob(fpath)

    def retrieveJobRecords(self, fpath):
        if self.isAttached():
            records=self.spooler.loadRecordsFromFile(fpath)
            return records

    def getLastDispatchAge(self):
        return time.time()-self._stampDispatch

    def isAlive(self):
        if self._threadDispatch and self._threadDispatch.isAlive():
            return True

    def dispatch(self):
        try:
            now=time.time()
            if now<self._timeoutInhibitDispatch or self._eventDispatching.isSet():
                return

            self._timeoutInhibitDispatch=now+120
            age=self.getLastDispatchAge()
            if age<300 or not self.isDispatchAllowed(age):
                return

            if self.isAlive():
                return

            if self._threadDispatch and self._threadDispatch.isAlive():
                return

            self._eventDispatching.set()
            try:
                self._threadDispatch=Thread(target=self.dispatcherManager)
                self._threadDispatch.start()
            except:
                self._eventDispatching.clear()
        except:
            pass

    def dispatcherManager(self):
        try:
            self._eventDispatching.set()

            jobs=self.getJobs()
            files=[]
            records=[]

            while jobs and len(records)<1024:
                fpath=jobs.pop()
                if fpath:
                    files.append(fpath)
                    r=self.retrieveJobRecords(fpath)
                    if r:
                        records.extend(r)
                        self.logger.debug('%s:job %s loaded (%d records)' % (self.name, fpath, len(r)))
                else:
                    break

            if records:
                self.logger.debug('%s:dispatching %d records' % (self.name, len(records)))
                if self.dispatchRecords(records):
                    self.removeJobs(files)
                    self._stampDispatch=time.time()
                    delay=max(120, self._delayInhibitDispatch)
                    self.logger.debug('%s:dispatch inhibited for %ds' % (self.name, delay))
                    self._timeoutInhibitDispatch=time.time()+delay
        except:
            self.logger.exception('%s:dispatch' % self.name)
        finally:
            self._eventDispatching.clear()

    def isDispatchAllowed(self, age):
        return True

    def recordsToData(self, records):
        """encode given records to a cStringIO (must be closed by caller)"""
        if records:
            data=cStringIO.StringIO()
            try:
                for record in records:
                    data.write(record.toString())
                    data.write('\n')
                data.seek(0)
                return data
            except:
                self.logger.exception('%s:encode' % self.name)
                data.close()

    def compressData(self, data):
        """gzip the given data to a cStringIO (must be closed by caller)"""
        if data:
            gzdata = cStringIO.StringIO()
            try:
                with gzip.GzipFile(mode='wb', fileobj=gzdata) as gzip_obj:
                    gzip_obj.write(data.getvalue())
                gzdata.seek(0)
                return gzdata
            except:
                self.logger.exception('%s:compress' % self.name)
                gzdata.close()

    def dispatchRecords(self, records):
        """
        User job to store/dispatch the given records. Called in a Thread context.
        Must return True if every records was successfully archived
        Must exit (False) as fast as possible if self.isStopped() returns True
        Any exception will by trapped by the caller
        """

        print("NOW dispatching %d recs for dispatcher %s" % (len(records), self.name))
        for record in records:
            print("DISPATCHING", self.name, record.name, record.value, record.stamp)
            if self.isStopped():
                return False
            time.sleep(1.0)

        return True


class ProviderFloat(Provider):
    def __init__(self, name, deltaTrigger=None, **kwargs):
        super(ProviderFloat, self).__init__(name=name, rtype=RecordFloat, **kwargs)
        self._deltaTrigger=deltaTrigger

    def isTriggerForValue(self, value):
        try:
            if self._deltaTrigger is not None:
                if value is not None and self._lastRecord.isDelta(value, self._deltaValue):
                    return True
        except:
            pass

    def setDeltaTrigger(self, delta):
        self._deltaTrigger=delta


class Spooler(object):
    def __init__(self, datalogger, name, cacheMaxSize=1024):
        assert isinstance(datalogger, DataLogger)
        assert name

        self._datalogger=datalogger
        datalogger.attach(self)

        self._lock=RLock()
        self._name=name.strip()
        self._stop=False

        self._cache=[]
        self._cacheMaxSize=cacheMaxSize
        self._cacheTimeout=0

        self._providers=[]
        self._dispatchers=[]

    @property
    def datalogger(self):
        return self._datalogger

    @property
    def logger(self):
        return self.datalogger.logger

    @property
    def name(self):
        return self._name

    def isStopped(self):
        if self._stop:
            return True

    # def providerFloat(self, *args, **kwargs):
        # provider=ProviderFloat(*args, **kwargs)
        # self.attach(provider)
        # return provider

    def attach(self, child):
        try:
            with self._lock:
                if isinstance(child, Provider):
                    if child.attach(self):
                        self._providers.append(child)
                elif isinstance(child, Dispatcher):
                    if child.attach(self):
                        self._dispatchers.append(child)
        except:
            self.logger.exception('%s:attach' % self.name)
            pass

    def detach(self, child):
        try:
            with self._lock:
                if isinstance(child, Provider):
                    if child.detach(self):
                        self._providers.remove(child)
                elif isinstance(child, Dispatcher):
                    if child.detach(self):
                        self._dispatchers.remove(child)
        except:
            self.logger.exception('%s:detach' % self.name)
            pass

    def isEmpty(self):
        if not self._cache:
            return True

    def clear(self):
        with self._lock:
            self._cache=[]

    def getStoragePath(self, subpath, filename=None):
        try:
            path=os.path.join(self.datalogger.path, self.name, subpath)
            try:
                os.makedirs(path)
            except:
                pass
            if filename:
                return os.path.join(path, filename)
            return path
        except:
            pass

    def spool(self, record):
        assert isinstance(record, Record)

        with self._lock:
            self._cache.append(record)
            self.logger.debug('%s:record %s spooled in queue %s' % (self.name, record.name, self.name))

            if self._cacheMaxSize>0 and len(self._cache)>=self._cacheMaxSize:
                if not self.store():
                    self.logger.error('%s:autoprune', self.name)
                    try:
                        self._cache.pop()
                    except:
                        pass

        self.manager()

    def manager(self):
        if time.time()>=self._cacheTimeout:
            self.store()

    def dispatch(self):
        with self._lock:
            for dispatcher in self._dispatchers:
                dispatcher.dispatch()

    def store(self):
        try:
            with self._lock:
                self._cacheTimeout=time.time()+60
                if not self.isEmpty():
                    for dispatcher in self._dispatchers:
                        fname='%s.datalogger' % str(uuid.uuid4())
                        fpath=self.getStoragePath(dispatcher.name, fname)

                        with open(fpath, 'w') as f:
                            count=0
                            for record in self._cache:
                                data=record.toString()
                                if data:
                                    f.write(data)
                                    f.write('\n')
                                    count+=1

                            self.logger.info('%s:%d records spooled in file %s' % (self.name, count, fpath))

                    self.clear()
                    return True
        except:
            self.logger.exception('%s:store' % self.name)
        finally:
            if not self._stop:
                self.dispatch()

    def loadRecordsFromFile(self, fpath):
        try:
            records=[]
            with open(fpath, 'r') as f:
                data=f.read()
                if data:
                    lines=data.splitlines()
                    for line in lines:
                        record=Record.fromString(line)
                        if record:
                            records.append(record)
            return records
        except:
            self.logger.exception('%s:load %s' % (self.name, fpath))

    def stop(self):
        with self._lock:
            self._stop=True

            children=self._providers
            while children:
                child=children[0]
                self.detach(child)

            self.store()

            children=self._dispatchers
            while children:
                child=children[0]
                self.detach(child)


class DataLogger(object):
    def __init__(self, path='~/tmp/datalogger', logger=None):
        self._logger=logger or logging.getLogger(self.__class__.__name__)
        self._path=os.path.expanduser(path)
        self._spoolers=[]
        self._indexByName={}

    @property
    def logger(self):
        return self._logger

    def attach(self, spooler):
        if spooler and isinstance(spooler, Spooler):
            if spooler not in self._spoolers:
                self._spoolers.append(spooler)
                return True

    def detach(self, spooler):
        if spooler and spooler in self._spoolers:
            try:
                self._spoolers.remove(spooler)
                return True
            except:
                pass

    def spooler(self, name, cacheMaxSize=1024):
        if name:
            try:
                spooler=self._indexByName[name.lower()]
            except:
                spooler=Spooler(self, name=name, cacheMaxSize=cacheMaxSize)
                self._indexByName[name.lower()]=spooler
            return spooler

    @property
    def path(self):
        return self._path

    def stop(self):
        for spooler in self._spoolers:
            spooler.stop()


if __name__ == "__main__":
    pass
