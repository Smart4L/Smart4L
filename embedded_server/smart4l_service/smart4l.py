#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

"""
RestFull API with Flask : https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
API Temps réelle :  https://dvic.devinci.fr/resource/tutorial/api-python/
Site web avec Flask : https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask
Some example : https://realpython.com/flask-by-example-part-1-project-setup/ 
Conf Flask : https://www.youtube.com/watch?v=1ByQhAM5c1I
Conf GIL : https://www.youtube.com/watch?v=7SSYhuk5hmc
Conf expert : https://github.com/austin-taylor/code-vault/blob/master/python_expert_notebook.ipynb
SQL Lite avec base en mémoire ♥: http://www.python-simple.com/python-autres-modules-non-standards/sqlite3.php
"""

"""
Les classes doivent porter leurs fonctions métier

Résoudre un problème d'import cyclique en créant une classe plus haut niveau, les classes ne doivent pas s'autogérer...

Une classe n'est pas "programme" en soit, elle est piloté depuis l'extérieur


"""


# Standard Library
import json
import logging
import os
import requests
import sqlite3
import sys
import time
from flask import Flask, jsonify, request
from random import randint
from threading import Thread, Event

# TODO fix this shitty import
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface
# Custom Modules
#from embedded_server.sensor_camera_module.DHT11 import DHT11
#from embedded_server.smart4l_service.utils import Message, Status, ServiceObjectInterface


# Class de gestions de service
class Service(Thread):
    def __init__(self, service_object: ServiceObjectInterface, timeout=0, name="unname", description="description unavailable"):
        Thread.__init__(self)
        self.status = Status.START.value
        self.eventStopService = Event()

        self.serviceObject = service_object
        self.timeout = timeout
        self.name = name
        self.description = description

    def run(self):
        while self.status == Status.START.value:
            self.serviceObject.do()
            self.eventStopService.wait(self.timeout)

    def __start__(self):
        Message.out(f"Service \"{self.name}\" now started")
        self.start()

    def __repr__(self):
        return f"{self.name}: {self.description}"

    def stop(self):
        self.status = Status.STOP.value
        self.eventStopService.set()
        self.serviceObject.stop()


class FlaskAPI(ServiceObjectInterface):
    def __init__(self,):
        self.conf = {"host":"localhost", "port":80}
        
        self.app = Flask("flask_api")
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)
        self.app.add_url_rule('/history', 'history', self.history)
        self.app.add_url_rule('/service', 'service', self.service)

    def do(self,):
        self.app.run(**self.conf)

    def index(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(Smart4l.lastMeasure)

    def history(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(Persistent().history())

    def service(self):
        return jsonify(str(Smart4l.services))

    # Must be call from HTTP request
    def shutdown(self):
        app_shutdown = request.environ.get('werkzeug.server.shutdown')
        if app_shutdown is None:
            raise RuntimeError('The function is unavailable!')
        else:
            app_shutdown()  
        return "FlaskAPI shuting down ..."

    def stop(self):
        # TODO fix this ugly thing, should use variable instead of statid string
        requests.get(f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown")


class Capteur(ServiceObjectInterface):
    def __init__(self, sensor_object, uid, do_func):
        self.sensorObject = sensor_object
        self.uid = uid
        self.doFunc = do_func

    def do(self):
        self.doFunc(self.uid, self.sensorObject.measure())

    def stop(self):
        self.sensorObject.clean()


class Persistent(ServiceObjectInterface):
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
        cur.execute('insert into smart4l(date, data) values(?,?)', [str(time.time()), json.dumps(Smart4l.lastMeasure)])
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


# Class des gestions de l'application / service
class Smart4l():
    lastMeasure = {}
    services = []
    def __init__(self):
        # TODO implement message Queue
        # TODO implement singleton pattern
        #self.lastMeasure = {}
        #self.services = []
        Message.out("Started !")
        Message.out("Running ...")

    @staticmethod
    def update_measure(uid, value):
        Smart4l.lastMeasure[uid] = value

    def reload(self):
        [service.__start__() for service in Smart4l.services if not service.is_alive()]

    def addService(self, service):
        Smart4l.services.append(service)
        # Must use reload function to start the new service

    def stop(self):
        Message.out("\nCleaning ...")
        [service.stop() for service in Smart4l.services]
        Message.out("Stopped !")


# execute only if run as a script
if __name__ == "__main__":

    if os.path.isfile('smart4l.pid'):
        Message.wrn("PID file  already exists")
        os.remove("smart4l.pid")
    open("smart4l.pid","w+").write(str(os.getpid()))

    app = Smart4l()
    
    app.addService(Service(service_object=Capteur(DHT11(),"DHT11 ext",Smart4l.update_measure), timeout=2, name="DHT11 ext", description=""))
    app.addService(Service(service_object=Capteur(DHT11(),"DHT11 int",Smart4l.update_measure), timeout=5, name="DHT11 int", description=""))
    app.addService(Service(service_object=Persistent(), timeout=20))
    app.addService(Service(service_object=FlaskAPI()))

    app.reload()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        app.stop()
        os.remove("smart4l.pid")
else:
    Message.err("smart4l.py : must be run as a script\n")
