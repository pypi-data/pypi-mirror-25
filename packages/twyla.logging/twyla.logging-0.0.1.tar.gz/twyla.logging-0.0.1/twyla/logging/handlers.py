import logging
import logging.handlers
import json

import socket
import traceback

from requests_futures.sessions import FuturesSession

from twyla.logging.formatters import LogglyJSONFormatter

session = FuturesSession()

URL_BASE =  'https://logs-01.loggly.com/inputs/{token}/tag/{tag}'

def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass


class LogglyHTTPSHandler(logging.Handler):

    def __init__(self, token, tag, formatter=None):
        logging.Handler.__init__(self)
        self.url = URL_BASE.format(**locals())
        self.formatter = formatter or LogglyJSONFormatter()


    def emit(self, record):
        data = self.formatter.format(record)
        try:
            payload = json.dumps(data)
            session.post(self.url, data=payload, background_callback=bg_cb)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
