#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     config.py
@contact:     wxgatpku@gmail.com

Description:

Changelog:

'''
import os
import logging

CONF_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath('.')

def _set_from_environ():
    d = globals()
    for k in d:
        v = os.environ.get(k)
        if v:
            d[k] = v

ENVIRONMENT = 'dev'
LOG_LEVEL = logging.INFO


SQL_HOST = 'localhost'
SQL_PORT = 3306
SQL_USER = 'root'
SQL_PASSWD = 'fai'
SQL_DB = 'quant'
SQL_CHARSET = 'utf8'
SQL_TABLE = 'swindex'

_set_from_environ()
