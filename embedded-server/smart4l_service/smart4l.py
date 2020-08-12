#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

import os    # standard library
import sys
sys.path.insert(1, '../sensor_camera-module')

import time as time

import threading
import multiprocessing

from flask import Flask
import DHT11 as DHT11


app = Flask(__name__)
flaskProc = multiprocessing.Process(target=app.run, args=())

def measurementService():
	pass

def start():
	print("Started !")
	# Start web service
	#threading.Thread(target=app.run).start()
	flaskProc.start()
	# Start measurement service
	print("Running ...")
	while True:
		print(DHT11.measure())
		time.sleep(2)

	print("! Starting completion !")


def stop():
	# Stop services
	print("\nCleaning ...")
	# Close socket & db connection
	
	# Stop web service
	#threading.Thread(target=app.run)
	flaskProc.terminate()  # sends a SIGTERM
	# Stop measurement service 
	
	# Cleanup GPIO
	
	print("Stopped !")
	sys.exit()


@app.route('/')
def index():
	return str(DHT11.measure())


# execute only if run as a script
if __name__ == "__main__":
    try:
    	start()
    except KeyboardInterrupt:
    	stop()
else:
	sys.stderr.write("Error : smart4l.py : must be run as a script\n")


