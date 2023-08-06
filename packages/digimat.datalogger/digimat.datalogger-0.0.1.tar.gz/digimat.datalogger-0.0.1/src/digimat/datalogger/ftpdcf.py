import cStringIO
from .ftp import FTPDispatcher


class FTPDcfDispatcher(FTPDispatcher):
    def generateFileNameForRecords(self, records):
        if records:
            count=len(records)
            return self.generateFileName(prefix='%s-%d' % (self.name, count), suffix='.dcfreccsv.gz')

    def recordToString(self, record):
        data=[
            record.stamp.strftime('%Y%m%d%H%M%S'),
            record.name,
            record.valueAsString(),
            '0',  # flags
            record.unitAsString()]
        return ';'.join(data)

    def recordsToData(self, records):
        """encode given records to a cStringIO (must be closed by caller)"""
        if records:
            data=cStringIO.StringIO()
            try:
                for record in records:
                    data.write(self.recordToString(record))
                    data.write('\n')
                data.seek(0)
                return data
            except:
                self.logger.exception('%s:encode' % self.name)
                data.close()


if __name__ == "__main__":
    pass
