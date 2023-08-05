from logging import Formatter, PercentStyle

class LogglyJSONFormatter(Formatter):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._style = PercentStyle(PercentStyle.asctime_format)

    def format(self, record):
        # Need to do this to set time and exception fields on the
        # record. Python's logging module just loves state
        super().format(record)
        if record.exc_info:
            message = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            message = record.getMessage()

        data = {
            'loggerName': record.name,
            'ascTime': record.asctime,
            'fileName': record.filename,
            'logRecordCreationTime': record.created,
            'functionName': record.funcName,
            'levelNo': record.levelno,
            'lineNo': record.lineno,
            'time': record.msecs,
            'levelName': record.levelname,
            'message': message
        }
        return data
