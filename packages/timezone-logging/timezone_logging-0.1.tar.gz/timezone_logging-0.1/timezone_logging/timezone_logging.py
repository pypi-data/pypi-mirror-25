# coding: utf-8
from __future__ import absolute_import, unicode_literals

import logging
from datetime import datetime
import tzlocal

class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt, timezone):
        self.timezone = timezone or tzlocal.get_localzone()
        super(TimezoneFormatter, self).__init__(fmt, datefmt)

    def formatTime(self, record, datefmt=None):
        if datefmt and self.timezone:
            dt = datetime.fromtimestamp(record.created, self.timezone)
            return dt.strftime(datefmt)
        else:
            return super(TimezoneFormatter, self).formatTime(record, datefmt)

def get_timezone_logger(name, fmt="%(asctime)s %(name)-24s %(levelname)-8s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z", log_level=logging.DEBUG, timezone=tzlocal.get_localzone()):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(TimezoneFormatter(fmt, datefmt, timezone))
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger