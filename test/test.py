#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import base64
import requests

if __name__ == '__main__':
    sys.path.insert(0, '../')

from code.utils import encrypt_token
selectid = 'query;select * from table limit 10'
#selectid = "query;select table_name from information_schema.tables where table_schema='schema' limit 10"

pri_key = './id_rsa.pem'
name = base64.b64encode('{modulename}/1.0.0/api/v1')
selectid = encrypt_token(pri_key, selectid).encode('hex')

api = 'http://ip:port/api/v1/trigger/test?auth=true&name=test'
data = {'name': name , 'themeid': selectid}
res = requests.post(api, json=data)
print json.loads(res.text)
