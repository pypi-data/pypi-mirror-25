from logging import Formatter, PercentStyle, LogRecord
import traceback

DEFAULT_PROPERTIES = list(LogRecord('', '', '', '', '', '', '', '').__dict__.keys())
# The logging module sucks big time. when Formatter.getMessage is
# called, it just casually sets a message attribute on the
# record. Same thing with Formatter.format and asctime. This same
# extra handling has to be done also in logging/__init__.py, line
# 1387.
DEFAULT_PROPERTIES.extend(['message', 'asctime'])

class LogglyJSONFormatter(Formatter):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._style = PercentStyle(PercentStyle.asctime_format)

    def get_extras(self, record):
        if len(DEFAULT_PROPERTIES) == len(record.__dict__):
            return None
        extras = set(record.__dict__).difference(set(DEFAULT_PROPERTIES))
        if not extras:
            return None
        return {key: getattr(record, key) for key in extras}


    def format(self, record):
        # Need to do this to set time and exception fields on the
        # record. Python's logging module just loves state
        super().format(record)
        message = record.getMessage()
        if record.exc_info:
            message = '\n'.join(
                [message, ''.join(traceback.format_exception(*record.exc_info))])

        data = {
            'loggerName': record.name,
            'timestamp': record.asctime,
            'fileName': record.filename,
            'logRecordCreationTime': record.created,
            'functionName': record.funcName,
            'levelNo': record.levelno,
            'lineNo': record.lineno,
            'time': record.msecs,
            'levelName': record.levelname,
            'message': message
        }
        extras = self.get_extras(record)
        if extras:
            data['extra'] = extras
        return data
