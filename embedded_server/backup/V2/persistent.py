# -*- coding: utf-8 -*-

import sqlite3
import json
from utils import Message, Status, ServiceObjectInterface
import time


# TODO rework this class
class Persistent(ServiceObjectInterface):
    def __init__(self, app):
        self.app = app
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute(
            "create table if not exists smart4l(date varchar(50), data json)"
        )
        cur.close()
        con.commit()
        con.close()

    def do(self):
        # TODO DB registration
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute(
            'insert into smart4l(date, data) values(?,?)',
            [str(time.time()), json.dumps(self.app.data)],
        )
        cur.close()
        con.commit()
        con.close()
        Message.out("DB registration")

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
