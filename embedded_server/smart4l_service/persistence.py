# -*- coding: utf-8 -*-

import json
import sqlite3
import time
import logging
from utils import RunnableObjectInterface


# TODO rework this class
# TODO check if sqlite3 cursor also have a context manager
# TODO type hint params
class Persistent(RunnableObjectInterface):
    """Main class responsible for DB connection and data handling"""
    def __init__(self, data):
        self.data = data
        con = sqlite3.connect('smart4l.db')
        with con:
            cur = con.cursor()
            cur.execute(
                "create table if not exists smart4l(date varchar(50), data json)"
            )
            cur.close()
            con.commit()

    def do(self):
        # TODO DB registration
        con = sqlite3.connect('smart4l.db')
        with con:
            cur = con.cursor()
            cur.execute(
                'insert into smart4l(date, data) values(?,?)',
                [str(time.time()), json.dumps(self.data["measure"])],
            )
            cur.close()
            con.commit()
            logging.info("DB registration")

    def history(self):
        """fetchall ??"""
        con = sqlite3.connect('smart4l.db')
        res = []
        with con:
            cur = con.cursor()
            cur.execute('select date, data from smart4l')
            row = cur.fetchone()
            while row != None:
                res.append({"date": row[0], "data": json.loads(row[1])})
                row = cur.fetchone()

            cur.close()
            con.commit()
        return res

    def stop(self):
        pass
