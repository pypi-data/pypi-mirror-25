import os
import uuid
from ftplib import FTP

from .datalogger import Dispatcher


class FTPDispatcher(Dispatcher):
    def onInit(self, *args, **kwargs):
        self._host=kwargs.get('host', None)
        self._user=kwargs.get('user', None)
        self._password=kwargs.get('password', None)
        self._timeout=int(kwargs.get('timeout', 15))
        self._path=kwargs.get('path', None)
        self._ftp=None

    def connect(self):
        try:
            if not self._ftp:
                self.logger.debug('%s:connect FTP(%s)' % (self.name, self._host))
                self._ftp=FTP(self._host, self._user, self._password, timeout=self._timeout)
                self._ftp.set_pasv(True)
        except:
            self.close()
        return self._ftp

    def close(self):
        try:
            self._ftp.quit()
            self.logger.debug('%s:disconnect FTP(%s)' % (self.name, self._host))
        except:
            pass
        self._ftp=None

    def generateFileName(self, prefix=None, suffix='.rec', salt=True):
        fname=prefix or ''
        if salt or not prefix:
            if fname:
                fname+='-'
            fname+='%s' % str(uuid.uuid4())
        if suffix:
            fname+=suffix
        if self._path:
            fname=os.path.join(self._path, fname)
        return fname

    def generateFileNameForRecords(self, records):
        if records:
            count=len(records)
            return self.generateFileName(prefix='%s-%d' % (self.name, count), suffix='.rec.gz')

    def dispatchRecords(self, records):
        try:
            count=len(records)
            fpath=self.generateFileNameForRecords(records)
            ftp=self.connect()
            if ftp:
                data=self.recordsToData(records)
                if data:
                    gzdata=self.compressData(data)
                    data.close()
                    if gzdata:
                        try:
                            ftp.storbinary('STOR %s' % fpath, gzdata)
                            self.logger.info('%s:FTP(%s) %d records stored to %s' % (self.name, self._host, count, fpath))
                            return True
                        except:
                            self.logger.error('%s:FTP(%s) storing %d records to %s' % (self.name, self._host, count, fpath))
                        finally:
                            gzdata.close()
        finally:
            self.close()


if __name__ == "__main__":
    pass
