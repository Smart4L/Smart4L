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

from flask import Flask
import time as time
import threading
import multiprocessing
import globalVar
import DHT11 as DHT11


class Smart4l():
	def __init__(self):
		self.app = Flask(__name__)
		self.flaskProc = multiprocessing.Process(target=self.app.run, args=())

	def start(self):
		print("Started !")
		# Start web service
		#threading.Thread(target=app.run).start()
		self.flaskProc.start()
		# Start measurement service
		print("Running ...")
		while True:
			print(DHT11.measure())
			time.sleep(2)

		print("! Starting completion !")

	def stop(self):
		# Stop services
		print("\nCleaning ...")
		# Close socket & db connection
		
		# Stop web service
		#threading.Thread(target=app.run)
		self.flaskProc.terminate()  # sends a SIGTERM
		# Stop measurement service 
		
		# Cleanup GPIO
		
		print("Stopped !")
		sys.exit()


# execute only if run as a script
if __name__ == "__main__":
    globalVar.process = Smart4l()
    try:
    	globalVar.process.start()
    except KeyboardInterrupt:
    	globalVar.process.stop()
else:
	sys.stderr.write("Error : smart4l.py : must be run as a script\n")
