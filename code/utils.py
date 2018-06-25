#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
import base64
import logging
import traceback
from datetime import date, datetime
from dateutil.relativedelta import *
from conf import config

def getLogger(log_name):
    LOG_LEVEL = config.LOG_LEVEL or logging.INFO
    LOG_FORMAT = '%(levelname)s: %(asctime)s: %(name)s %(process)d %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(level=int(LOG_LEVEL), format=LOG_FORMAT)
    logger = logging.getLogger(log_name)
    return logger

def datetime2str(dt=None, _format=None):
    if not dt:
        dt = datetime.today()
    if not _format:
        _format = '%Y-%m-%d %H:%M:%S'

    dt_str = dt.strftime(_format)

    return dt_str

def get_relative_time(unit, relative, dt=None):
    '''
    unit: month, day, hour
    relative: -1, -2, 1, 4
    dt: 相对于哪一天，默认为今天
    '''

    if not dt:
        dt = datetime.today()

    if unit == 'year':
        return dt + relativedelta(years=relative)
    elif unit == 'month':
        return dt + relativedelta(months=relative)
    elif unit == 'day':
        return dt + relativedelta(days=relative)
    elif unit == 'hour':
        return dt + relativedelta(hours=relative)
