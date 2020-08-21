#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

# Standard Library
import os
import sys
from threading import Thread, Event
import time
# Custom Modules
sys.path.insert(1, '../sensor_camera-module')
import DHT11
from utils import Message, Status



# Class de gestions du service d'enregistrement en base
class PersistentService(Thread):
	status = Status.START.value
	eventStopService = None
	def __init__(self, delay=None):
		super().__init__()
		self.delay = delay
		self.eventStopService = event
	def run(self):
		while self.status==Status.START.value:
			# TODO Save date in DB
			# if date is not empty
			#db.save(Smart4l.lastMeasure)
			print(" Data saved !")
			self.eventStopService.wait(self.delay)
			
	def stop(self):
		self.status = Status.STOP.value
		# TODO Emit event for sleep interuption
		# TODO Close DB connection


# Class de gestions du service des mesures temps réelle
class MeasurementService(Thread):
	status = Status.START.value
	eventStopService = None
	def __init__(self, capteur=None, delay=None):
		super().__init__()
		self.capteur = capteur
		self.delay = delay
		self.eventStopService = Event()

	def run(self):
		while self.status==Status.START.value:
			Smart4l.lastMeasure[self.capteur.id]=self.capteur.measure()
			self.eventStopService.wait(self.delay)

	def stop(self):
		self.status = Status.STOP.value
		# TODO Clean GPIO



# Class des gestions de l'application / service
class Smart4l():
	lastMeasure = {"DHT11 ext":None, "DHT11 int":None}
	services = []
	
	def __init__(self):
		self.services.append(MeasurementService(capteur=DHT11.DHT11("DHT11 ext"),delay=2))
		self.services.append(MeasurementService(capteur=DHT11.DHT11("DHT11 int"),delay=2))
		self.services.append(PersistentService(delay=20))

	def start(self):
		print("Started !")
		# TODO Si le service le fonctionne pas deja
		# Existance du fichier pid + le pid repond au nom du programme
		#	lancement du process, creation du fichier pid
		# Si le service fonctionne ouvrir un PIPE avec le pid du fichier pid
		# 	envoyer les parametre dans le pipe

		# Run thread
		[service.start() for service in self.services]
		
		print("Running ...")


	def stop(self):
		print("Cleaning ...")
		# TODO Supprimer le fichier pid

		# Stop Measurement Service Thread
		[service.stop() for service in self.services]
		# TODO Clean GPIO
		print("Stopped !")


# execute only if run as a script
if __name__ == "__main__":
	app = Smart4l()
	try:
		app.start()
		# Si on sort de la boucle, l'exception KeyboardInterrupt n'est plus gérée
		#while not input() == Status.STOP.value:
		while True:
			print(Smart4l.lastMeasure)
			time.sleep(2)
		#app.stop()
	except KeyboardInterrupt:
		app.stop()
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

