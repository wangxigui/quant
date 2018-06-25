#!/usr/bin/env python
# -*- coding: utf8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from service import BasicSQLService
from constants import swindexcode, fieldlist, colors
from conf.config import SQL_TABLE

sqlServ = BasicSQLService()

def readDataFromDb(swindex=None):
    indexcode = swindex or swindexcode[0]
    close_index = 'select CloseIndex from %s where SwIndexCode="%s" order by BargainDate'%(SQL_TABLE, indexcode)
    bargaindate = 'select BargainDate from %s where SwIndexCode="%s" order by BargainDate'%(SQL_TABLE, indexcode)

    indexes = sqlServ.query(close_index)
    dts = sqlServ.query(bargaindate)

    return dts, indexes


def render(swindex, closeindexes, dts):
    x = np.array(dts)
    y = np.array(closeindexes)

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='date(day)', ylabel='closeindex',
           title='index %s trend' %swindex)
    ax.grid()
    plt.show()

def renderall():
    candidate = []
    color_num = len(colors)
    for index, swindex in enumerate(swindexcode[10:]):
        dts, indexes = readDataFromDb(swindex)
        clr = colors[index%color_num]
        candidate.append(np.array(dts))
        candidate.append(np.array(indexes))
        candidate.append(clr)

    fig, ax = plt.subplots()
    ax.plot(*candidate)

    ax.set(xlabel='date(day)', ylabel='closeindex',
           title='sw index trend')
    ax.grid()
    plt.show()

def run():
    renderall()
    return

    swindex = swindexcode[0]
    dts, indexes = readDataFromDb(swindex)
    render(swindex, indexes, dts)

if __name__ == '__main__':
    run()
