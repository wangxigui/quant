#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
FileName:     service.py

Description:

'''

import os
import copy
import MySQLdb
import traceback

from utils import getLogger
from conf.config import (
    SQL_HOST,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWD,
    SQL_DB,
    SQL_CHARSET,
)

logger = getLogger(__file__)

class BasicSQLService():

    def __init__(self, connection=None, *args, **kwargs):
        self.conn = connection or self.init_conn()
        self.cur = self.conn.cursor()

    def init_conn(self):
    	conn = MySQLdb.connect(
                host=SQL_HOST,
                port=SQL_PORT,
                user=SQL_USER,
                passwd=SQL_PASSWD,
                db=SQL_DB,
                charset=SQL_CHARSET
            )
        return conn

    def query(self, sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()

        return res

    def commit(self, sql, param=()):
        try:
            n = self.cur.execute(sql, param)
            self.conn.commit()
            return n
        except Exception, e:
            self.conn.rollback()
            logger.error(sql)
            logger.error(traceback.format_exc())

    def format_dict(self, d):
        ''' convert dict to a new format: key=val'''
        res = []
        for key, val in d.items():
            sen = '''{k}="{v}"'''
            if isinstance(val, int):
                sen = '''{k}={v}'''
            sub_cond = sen.format(k=key, v=val)
            res.append(sub_cond)

        return res

    def get_one(self, table, fields, **query):
        _fields = []
        cond = self.format_dict(query)
        _fields = ', '.join(fields)
        _cond = ' and '.join(cond)

        sql = '''
            SELECT {fields} FROM {table} WHERE {cond}
        '''
        sql = sql.format(fields=_fields, table=table, cond=_cond)
        # logger.info(sql)
        res = self.query(sql)

        return res[0] if res else None

    def update(self, table, conds, vals):
        cond_tmp = self.format_dict(conds)
        vals_tmp = self.format_dict(vals)

        _cond = ' and '.join(cond_tmp)
        _vals = ', '.join(vals_tmp)

        sql = '''
            UPDATE {table} SET {vals} WHERE {cond}
        '''
        sql = sql.format(table=table, vals=_vals, cond=_cond)
        # logger.info(sql)

        res = self.commit(sql)
        return res

    def insert(self, table, fields, vals):
        _fields = ', '.join(fields)
        _vals = ', '.join(self.format_dict(vals))

        sql = '''
            INSERT INTO {table}({fields}) VALUES({vals})
        '''

        sql = sql.format(table=table, fields=_fields, vals=_vals)
        res = self.commit(sql)

        return res

    def insertmany(self, table, data):
        '''
            插入多行, data 为list:[{key, val}, {}]
        '''
        if not data or not isinstance(data, list):
            return

        fields = data[0].keys()
        fields_str = ', '.join(fields)

        _format_str = '(' + ', '.join(['\'%s\''] * len(fields)) + ')'# (%s, %s, %s, ....)

        values = []
        for item in data:
            row = []
            for f in fields:
                row.append(item.get(f))
            values.append(row)

        sql = 'INSERT INTO {table}(' + fields_str + ') VALUES'
        args_str = ','.join(_format_str%tuple(x) for x in values)
        sql = sql.format(table=table) + args_str
        self.commit(sql)

    def truncate(self, table):
        sql = '''TRUNCATE {table}'''.format(table=table)
        self.commit(sql)
        return True

    def __del__(self):
        self.cur.close()
        self.conn.close()

