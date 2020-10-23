# -*- coding: utf-8 -*-

import json
import sqlite3
import time
import logging
from utils import RunnableObjectInterface
import store_smart4l

# TODO rework this class
class Persistent(RunnableObjectInterface):
    def __init__(self):
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute("create table if not exists smart4l(date varchar(50), data json)")
        cur.close()
        con.commit()
        con.close()

    def do(self):
        # TODO DB registration
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute('insert into smart4l(date, data) values(?,?)', [str(time.time()), json.dumps(store_smart4l.last_measure)])
        cur.close()
        con.commit()
        con.close()
        logging.info("DB registration")

    def history(self):
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute('select date, data from smart4l')
        row = cur.fetchone()
        res = []
        while row != None:
            res.append({"date": row[0], "data": json.loads(row[1])})
            row = cur.fetchone()
        cur.close()
        con.commit()
        con.close()
        
        return res

    def stop(self):
        pass
