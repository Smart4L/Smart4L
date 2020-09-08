#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Camel and SnaKe Case : https://towardsdatascience.com/why-does-python-recommend-the-snake-case-nomenclature-bf908777c2dc#:~:text=It%20should%20be%20noted%20that,%2Dshaped%20naming%20(lower_case_with_underscores).

Logging :
https://docs.python.org/fr/3/howto/logging.html
https://docs.python.org/3/library/logging.html
https://realpython.com/python-logging/
https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime
https://www.google.com/search?rlz=1C1GCEB_enFR867FR867&sxsrf=ALeKk023DVKRCALrsEaiUlRuIZrZvlORDg%3A1599471612043&ei=_P9VX_qPAs6LlwTe_b6QBw&q=python+logging+best+practices&oq=logging+datefmt&gs_lcp=CgZwc3ktYWIQAxgDMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHUABYAGDMGGgAcAF4AIABAIgBAJIBAJgBAKoBB2d3cy13aXrAAQE&sclient=psy-ab
https://www.loggly.com/use-cases/6-python-logging-best-practices-you-should-be-aware-of/
https://docs.python-guide.org/writing/logging/
https://www.toptal.com/python/in-depth-python-logging
https://www.datadoghq.com/blog/python-logging-best-practices/



Reverse Python code to UML :
sudo apt install pylint
sudo apt install graphviz
pyreverse -o png -p smart4l .
"""

import asyncio
import datetime
import json
import logging
import sys
import signal
import time
from random import randint
from threading import Thread, Event
from persistence import Persistent
from utils import RunnableObjectInterface, Status, SensorInterface
from flask_api import FlaskAPI
from smart4l_ws_server import Smart4lWebSocket
sys.path.insert(1, './sensor_camera_module')
from DHT11 import DHT11
from DS18B20 import DS18B20
from HCSR04 import HCSR04
"""
--- Logging Level ---
    CRITICAL    50
    ERROR       40
    WARNING     30
    INFO        20
    DEBUG       10
    NOTSET      0

--- Logging functions ---
    logging.info
    logging.error
    logging.critical
    logging.exception
    logging.warning
    logging.debug

# Git repository may not allow root to pull down updates
# Pull updates where $user is allowed to read/write remote.
# command line:
su -s /bin/sh $user -c 'cd /var/www/html/src && /usr/bin/git pull origin master'

# crontab (by executing sudo opens up root crontab)
sudo crontab -e 

# every 1 minute pull changes (if any)
*/1 * * * * su -s /bin/sh $user -c 'cd /var/www/html/src && /usr/bin/git pull origin master'


import RPi.GPIO as GPIO
GPIO.cleanup()

"""



class Sensor(RunnableObjectInterface):
    def __init__(self, sensor_object, name, on_measure):
        self.sensor_object = sensor_object
        self.on_measure = on_measure
        self.name = name

    def do(self):
        self.on_measure(self.name, self.sensor_object.measure())        

    def stop(self):
        pass

    def __str__(self):
        return f"{str(self.sensor_object)} : {self.name}"

    def __repr__(self):
        return str(self)


class Service(Thread):
    def __init__(self, runnable_object : RunnableObjectInterface, delay : int=0):
        Thread.__init__(self)
        self.delay_between_tasks = delay
        self.runnable_object = runnable_object

        self.status = Status.CREATED.value
        self.event_stop_service = Event()

    def run(self):
        self.status = Status.RUNNING.value
        while self.status == Status.RUNNING.value:
            self.runnable_object.do()
            self.event_stop_service.wait(self.delay_between_tasks)

    def stop(self):
        self.status = Status.TERMINATED.value
        self.event_stop_service.set()
        self.runnable_object.stop()

    def __str__(self):
        return f"Current status: {self.status} - RunnableObject {str(self.runnable_object)} - Delay {str(self.delay_between_tasks)}"

    def __repr__(self):
        return str(self)


class Smart4LApp():
    def __init__(self):
        self.services = {}
        self.data = {}
        loop = asyncio.get_event_loop()
        self.ws_server = Smart4lWebSocket(loop, host="0.0.0.0", port=8520, ssl_key_path="ws_cert.key", ssl_cert_path="ws_cert.pem", data=self.data)
        """
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ws_cert.key -out ws_cert.pem
        enable self signed certs on chrome : chrome://flags/#allow-insecure-localhost    
        """
        self.db = Persistent({"measure": self.data, "service": self.services})
        self.http_api = FlaskAPI(self.db, host="localhost", port=8080)
        #self.http_api = FlaskAPI(self.db, host="localhost", port=8080, ssl_key_path="ws_cert.key", ssl_cert_path="ws_cert.pem")

    def start(self):
        # Init main service
        self.add_service(service_id = "DB", service = Service(self.db, delay=20))
        self.add_service(service_id = "HTTP", service = Service(self.http_api))
        self.add_service(service_id = "WS_SERVER", service = Service(self.ws_server))
        # Parse file and add sensor service
        self.add_service(service_id = "SENSOR_1", service = Service(Sensor(DHT11(), name="DHT11_in", on_measure=self.update_data), delay=2))
        self.add_service(service_id = "SENSOR_2", service = Service(Sensor(DHT11(), name="DHT11_out", on_measure=self.update_data), delay=3))
        self.add_service(service_id = "SENSOR_ENGINE", service = Service(Sensor(DS18B20(), name="DS18B20_engine", on_measure=self.update_data), delay=1))
        self.add_service(service_id = "SENSOR_DISTANCE", service = Service(Sensor(HCSR04(), name="HC-SR04_arriere", on_measure=self.update_data), delay=1))
        
        # Launch service
        self.reload_services()

    def reload_services(self):
        [service.start() for service_id, service in self.services.items() if not service.is_alive()]

    def stop(self):
        [service.stop() for service_id, service in self.services.items()]

    def add_service(self, service_id:int, service:Service):
        # TODO : Check if service_id not already exists
        self.services[service_id]=service
        

    def update_data(self, uid, value):
        # If value has not changed exit
        if uid in self.data.keys() and self.data[uid] == value:
            return

        self.ws_server.send_message(json.dumps( {"type": "UPDATE_SENSOR", "content": {"id": uid,"value": value}}))
        self.data[uid] = value
        
    def parse_service_file(self):
        pass


app = Smart4LApp()

def start():
    logging.info('--- Started ! ---')
    # Checking for process already running with pid file
    logging.info('--- Check Lock File ---')

    # Let's start application
    global app
    logging.info('--- Running... ---')
    app.start()
    # Should stay in infinite loop to catch KeyboardInterrupt
    while True:
        pass


def stop():
    logging.info('--- Cleaning... ---')
    global app
    app.stop()
    logging.info('--- Stopped ! ---\n')


# Execute only if run as a script
if __name__ == "__main__":
    #logging.basicConfig(filename=f'example{datetime.time}.log',level=logging.DEBUG)
    #logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    #logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    logging.basicConfig(level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    signal.signal(signal.SIGTERM, stop)
    try:
        start()
    except KeyboardInterrupt:
        logging.warning('KeyboardInterrupt')
    except:
        # Get exception that is currently being handled
        e = sys.exc_info()
        logging.exception(e)
        logging.exception(e.message)

    finally:
        stop()
else:
    logging.critical(f"{__name__} : must be run as a script\n")
