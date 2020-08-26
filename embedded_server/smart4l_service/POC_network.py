#!/usr/bin/env python3
# -*- coding: utf-8 -*

import json
import os
import requests
import sys
import time
from random import randint
from threading import Thread, Event
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface

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
        Message.out(f"Service \"{self.name}\" is now started")
        self.start()

    def __repr__(self):
        return f"{self.name}: {self.description}"

    def stop(self):
        self.status = Status.STOP.value
        self.eventStopService.set()
        self.serviceObject.stop()

class Capteur(ServiceObjectInterface):
    def __init__(self, sensor_object, uid, values):
        self.sensorObject = sensor_object
        self.uid = uid
        self.values = values

    def do(self):
        self.values[self.uid] = self.sensorObject.measure()

    def stop(self):
        self.sensorObject.clean()



class Server():
    def __init__(self):
        pass

    def send_message(self,):
        pass

    def receive_message(self):
        pass


class Client():
    def __init__(self):
        pass

    def send_message(self,):
        pass

    def receive_message(self):
        pass



if __name__ == "__main__":
    services = []
    lastMeasure = {}
    capteurs = [Capteur(DHT11(), "DHT11 EXT RPI2", lastMeasure), Capteur(DHT11(), "DHT11 INT RPI2", lastMeasure)]
    [services.append(Service(service_object=capteur, timeout=2, name=capteur.uid)) for capteur in capteurs]
    [service.__start__() for service in services if not service.is_alive()]
    try:
        while True:
            Message.out(lastMeasure)
            time.sleep(2)
    except KeyboardInterrupt:
        [service.stop() for service in services]
else:
    Message.err("POC_network.py : must be run as a script\n")



"""
Socket Ressource :
socketserver lib : https://docs.python.org/3/library/socketserver.html
socker lib : https://fiches-isn.readthedocs.io/fr/latest/FicheReseauxClient01.html
pickle module allow to pass python object via socket

https://www.youtube.com/watch?v=Lbfe3-v7yE0
https://www.youtube.com/watch?v=3QiPPX-KeSc
--- ---
Socket Begening : https://www.youtube.com/watch?v=T0rYSFPAR0A

# Server.py
import socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(), 8080))
s.listen(1) 
while True:
    clt, adr = s.accept()
    print(f"Connection {adr} done")
    clt.send(bytes("First Message","utf-8"))
    clt.close()

# Client.py
import socket
s=socker.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(socker.gethostname(),8080)
msg = s.recv(1024)
print(msg.decode('utf-8'))

# while True:
#    msg = s.recv(8)
#    print(msg.decode('utf-8'))

# fullMessage = ""
# while True:
#   msg = s.recv(8)
#   if len(msg)<=0:
#        break
#    fullMessage+=msg.decode('utf-8')    
# print(fullMessage)


# pickle usage .py
import pickle
list = [1, 2 , 3]
ser = pickle.dumps(list)
print(ser)

# picker socket server
import socket
import pickle

a=10
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8080))
s.listen(5)
while True:
    clt, adr = s.accept()
    print(f"Connection to {adr} established")

    m={1:"Client",2 :"Server"}
    mymsg = pickle.dumps(m)
    mymsg = bytes(f"{len(mymsg):<{a}}","utf-8") + mymsg
    clt.send(mymsg)

# pickle socket client
import socket
import pickle
a=10
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socker.gethostname(),8080))

while True:
    fullMessage = b""
    rec_message = True
    while True:
        mymsg = s.recv(16)
        if rec_message:
            print(f"The length of message : {mymsg[:a]}")
            x = int(mymsg[:a])
            rec_message = False
        fullMessage += mymsg
        if len(fullMessage)-a ==x:
            print(f"Received the complete message")
            print(fullMessage)
            m = pickle.loads(fullMessage[a:])
            print(m)
            rec_message = True
    print(fullMessage)
--- ---
















"""