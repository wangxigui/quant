#!/user/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import requests
from constants import api, swindexcode, fieldlist
from service import BasicSQLService
from conf.config import SQL_TABLE

def collect(start_dt=None):
    start_dt = start_dt or '2010-01-01'
    end_dt = time.strftime('%Y-%m-%d')
    where = "swindexcode in ('" + "','".join(swindexcode) + "')" + \
        " and BargainDate>='%s' and BargainDate<='%s'"%(start_dt, end_dt)
    page = 1

    payload = {
        'tablename': 'swindexhistory',
        'key': 'id',
        'p': page,
        'where':  where,
        'orderby': 'swindexcode asc,BargainDate_1',
        'fieldlist': ','.join(fieldlist),
        'pagecount': 28 * 300 * 10, # 28个行业10年的数据
        'timed': int(time.time() * 1000)
    }

    total = []
    res = requests.post(api, data=payload)
    data = json.loads(res.text.replace('\'', '"')).get('root')

    while data:
        print ' ----------- page %s done ----------- '%page
        print data[0]
        total += data
        page += 1
        payload['p'] = page
        try:
            res = requests.post(api, data=payload)
            data = json.loads(res.text.replace('\'', '"')).get('root')
        except Exception as e:
            res = requests.post(api, data=payload)
            data = json.loads(res.text.replace('\'', '"')).get('root')

        time.sleep(0.2)

    return total


def save_overwrite(data):
    sqlServ = BasicSQLService()
    sqlServ.truncate(SQL_TABLE)
    sqlServ.insertmany(SQL_TABLE, data)

def run():
    #print ' --- skip --- '
    #return
    data = collect()
    save_overwrite(data)

if __name__ == '__main__':
    run()
