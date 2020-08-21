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

# Standard Library
import abc
import json
import logging
import os
import requests
import sqlite3
import sys
import time
from threading import Thread, Event
from random import randint
from flask import Flask, jsonify, request

# TODO fix this shitty import
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface
# Custom Modules
#from embedded_server.sensor_camera_module.DHT11 import DHT11
#from embedded_server.smart4l_service.utils import Message, Status, ServiceObjectInterface


# Class de gestions de service
class Service(Thread):
    def __init__(self, service_object: ServiceObjectInterface, timeout=0):
        super().__init__()
        self.serviceObject = service_object
        self.timeout = timeout
        self.status = Status.START.value
        self.eventStopService = Event()
        self.name = ""
        self.description = ""

    def run(self):
        while self.status == Status.START.value:
            self.serviceObject.do()
            self.eventStopService.wait(self.timeout)

    def __start__(self):
        if hasattr(self.serviceObject, 'uid'):
            Message.out(f"Service \"{self.serviceObject.uid}\" now started")
        self.start()

    def stop(self):
        self.status = Status.STOP.value
        self.eventStopService.set()
        self.serviceObject.stop()


class FlaskAPI(ServiceObjectInterface):
    def __init__(self,):
        self.app = Flask("flask_api")
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)
        self.app.add_url_rule('/history', 'history', self.history)
        self.thread = None

    def do(self,):
        # get the host and the port as keywords attributes for flaskApp.run()
        app_kwargs = {'host':"localhost", 'port':80}
        # run the flaskApp on a thread
        self.app.run(**app_kwargs)

    def index(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(app.lastMeasure)

    def history(self):
        # TODO fix this ugly thing, should not use app variable
        con = sqlite3.connect('smart4l.db')
        cur = con.cursor()
        cur.execute('select date, data from smart4l')
        row = cur.fetchone()
        res = []
        while row != None:
            res.append({"date": row[0], "data": json.loads(row[1])})
            row = cur.fetchone()

        cur.close()
        con.close()
        return jsonify(res)


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
        requests.get("http://localhost/shutdown")


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
        self.con = sqlite3.connect('smart4l.db')
        cur = self.con.cursor()
        cur.execute("create table if not exists smart4l(date varchar(50), data json)")
        cur.close()
        self.con.close()

    def do(self):
        # TODO DB registration
        self.con = sqlite3.connect('smart4l.db')
        cur = self.con.cursor()

        cur.execute('insert into smart4l(date, data) values(?,?)', [str(time.time()),json.dumps(app.lastMeasure)])
        cur.close()
        self.con.commit()
        self.con.close()
        # TODO Close connection here too
        Message.out("DB registration")

    def history(self):
        pass

    def stop(self):
        # TODO close DB connection
        try:
            self.con.close()
        except:
            pass


# Class des gestions de l'application / service
class Smart4l():
    def __init__(self):
        self.lastMeasure = {}
        self.services = []
        self.services.append(Service(service_object=Capteur(DHT11(),"DHT11 ext",self.update_measure), timeout=2))
        self.services.append(Service(service_object=Capteur(DHT11(),"DHT11 int",self.update_measure), timeout=5))
        self.services.append(Service(service_object=Persistent(), timeout=20))
        self.services.append(Service(service_object=FlaskAPI()))

    def update_measure(self, uid, value):
        self.lastMeasure[uid] = value

    def start(self):
        Message.out("Started !")
        # Run thread
        [service.__start__() for service in self.services if not service.is_alive()]
        Message.out("Running ...")

    def reload(self):
        [service.__start__() for service in self.services if not service.is_alive()]

    def addService(self, service):
        self.services.append(service)
        # Must use reload function to start new service

    def stop(self):
        Message.out("\nCleaning ...")
        # Stop Measurement Service Thread
        [service.stop() for service in self.services]
        # TODO Clean GPIO
        Message.out("Stopped !")


# execute only if run as a script
if __name__ == "__main__":
    # If pid file already exists
    if os.path.isfile('smart4l.pid'):
        Message.err("File pid already exists")
        sys.exit(1)
    else:
        open("smart4l.pid","w+").write(str(os.getpid()))
    
    app = Smart4l()
    try:
        app.start()
        # Si on sort de la boucle, l'exception KeyboardInterrupt n'est plus gérée
        #while not input() == Status.STOP.value:
        run = True
        
        switcher = {
                "measure"  : lambda : Message.out(app.lastMeasure)
                , "add"    : lambda : app.addService(Service(Capteur(DHT11(),str(randint(100,999)), lambda x, y: app.update_measure(x,y)),5))
                , "reload" : app.reload
                , "service": lambda : Message.out(app.services)
            }
        
        while run:
            try :
                Message.out(switcher.get(input("Saisir une action : "))())
            except KeyboardInterrupt:
                run = False
            except:
                Message.out("Invalid input")
            #time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
        os.remove("smart4l.pid")

else:
    Message.err("smart4l.py : must be run as a script\n")


"""
# Communication inter process via un fichier, pas mal mais peut etre plus opti avec des pipes

import os, time

pipe_path = "/tmp/mypipe"
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)
# Open the fifo. We need to open in non-blocking mode or it will stalls until
# someone opens it for writting
pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
with os.fdopen(pipe_fd) as pipe:
    while True:
        message = pipe.read()
        if message:
            print("Received: '%s'" % message)
        print("Doing other stuff")
        time.sleep(0.5)


echo "your message" > /tmp/mypipe


https://docs.python.org/3/library/os.html
https://docs.python.org/2/library/os.html
"""

"""
# Communication je sais pas comment ^^, par fichier visiblement. Apres un pipe c'est aussi un fichier mais un peut différent quand meme
# MARCHE peut etre ?
import errno, os, sys

try:
    os.mkfifo('some_pipe_name')
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise     # can't open pipe
while True:
    with open('some_pipe_name') as fifo:
        data = fifo.read()
        print data

Client:

import os, sys
pipeout = os.open('some_pipe_name', os.O_WRONLY)
os.write(pipeout, ' '.join(sys.argv[1:]))
"""

"""
# Communication inter process, je sais pas comment ^^
# MARCHE PAS
server.py:

def start_server():
    # create process
    e = receive_messages()
    while true:
        e.wait()
        if e.message == 'quit':
            sys.exit(1)
        # some message handling

And then a client script with this type of function:

client.py:

def send_message(pid):
    pipe = get_pipe_to_process_by_pid(pid)
    pipe.send_message('Hello, World!\n')

"""
