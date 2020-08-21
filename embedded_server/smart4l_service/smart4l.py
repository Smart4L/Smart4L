#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

# Standard Library
import abc
import logging
import os
import sys
import time
from threading import Thread, Event
from random import randint
from flask import Flask
from flask import jsonify

# Custom Modules
from embedded_server.sensor_camera_module.DHT11 import DHT11
from .utils import Message, Status


class ServiceObjectInterface(abc.ABC):
    @abc.abstractmethod
    def do(self):
        pass

    def stop(self):
        pass


# https://dvic.devinci.fr/resource/tutorial/api-python/

# Class de gestions de service
class Service(Thread):
    def __init__(self, service_object: ServiceObjectInterface, timeout):
        super().__init__()
        self.serviceObject = service_object
        self.timeout = timeout
        self.status = Status.START.value
        self.eventStopService = Event()

    def run(self):
        while self.status == Status.START.value:
            self.serviceObject.do()
            self.eventStopService.wait(self.timeout)

    def stop(self):
        self.status = Status.STOP.value
        self.eventStopService.set()
        self.serviceObject.stop()


class Capteur(ServiceObjectInterface):
    def __init__(self, sensor_object, uid, do_fun):
        self.sensorObject = sensor_object
        self.uid = uid
        self.action = do_fun

    def do(self):
        self.action(self.uid, self.sensorObject.measure())

    def stop(self):
        self.sensorObject.clean()


class Persistent(ServiceObjectInterface):
    def __init__(self):
        pass

    def do(self):
        # TODO DB registration
        print("DB registration")
        pass

    def stop(self):
        # TODO close DB connection
        pass


# Class des gestions de l'application / service
class Smart4l:
    lastMeasure = {}
    services = []

    def __init__(self):
        self.services.append(Service(serviceObject=Capteur(DHT11(), "DHT11 ext", self.update_measure), timeout=2))
        self.services.append(Service(serviceObject=Capteur(DHT11(), "DHT11 int", self.update_measure), timeout=5))
        self.services.append(Service(serviceObject=Persistent(), timeout=20))

    def update_measure(self, uid, value):
        self.lastMeasure[uid] = value

    def start(self):
        print("Started !")
        # TODO Si le service le fonctionne pas deja
        # Existence du fichier pid + le pid repond au nom du programme
        # lancement du process, creation du fichier pid
        # Si le service fonctionne ouvrir un PIPE avec le pid du fichier pid
        # 	envoyer les parametre dans le pipe

        # Run thread
        [service.start() for service in self.services if not service.is_alive()]

        print("Running ...")

    def reload(self):
        for service in self.services:
            if not service.is_alive():
                service.start()
                print(f"Service \"{service.serviceObject.uid}\" was not running, now started")

    def add_service(self, service):
        self.services.append(service)

    # Must use reload function to start new service

    def stop(self):
        print("\nCleaning ...")
        # TODO Supprimer le fichier pid

        # Stop Measurement Service Thread
        [service.stop() for service in self.services]
        # TODO Clean GPIO
        print("Stopped !")


# execute only if run as a script
if __name__ == "__main__":
    app = Smart4l()

    flaskApp = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    flaskApp.logger.disabled = True


    @flaskApp.route("/")
    def send_data():
        # convert into JSON format first
        return jsonify(app.lastMeasure)


    def start_flask(host, port):
        # get the host and the port as keywords attributes for flaskApp.run()
        app_kwargs = {'host': host, 'port': port}
        # run the flaskApp on a thread
        return Thread(target=flaskApp.run, kwargs=app_kwargs).start()


    try:
        app.start()
        flaskThread = start_flask("localhost", 80)
        # Si on sort de la boucle, l'exception KeyboardInterrupt n'est plus gérée
        # while not input() == Status.STOP.value:
        switcher = {
            "measure": lambda: print(app.lastMeasure)
            , "add": lambda: app.add_service(
                Service(Capteur(DHT11(), str(randint(100, 999)), lambda x, y: app.update_measure(x, y)), 5))
            , "reload": lambda: app.reload()
            , "stop": lambda: app.stop()
            , "service": lambda: print(app.services)
        }
        run = True
        while run:
            try:
                print(switcher.get(input("Saisir une action : "))())
            except KeyboardInterrupt:
                run = False
            except:
                print("Invalid input")
        # time.sleep(2)
        app.stop()
    except KeyboardInterrupt:
        app.stop()
        flaskThread._stop()
        flaskThread.terminate()
else:
    Message.error("smart4l.py : must be run as a script\n")

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
