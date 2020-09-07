#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Camel and SnaKe Case : https://towardsdatascience.com/why-does-python-recommend-the-snake-case-nomenclature-bf908777c2dc#:~:text=It%20should%20be%20noted%20that,%2Dshaped%20naming%20(lower_case_with_underscores).



Reverse Python code to UML :
sudo apt install pylint
sudo apt install graphviz
pyreverse -o png -p smart4l .

"""

import datetime
import logging
import sys
from random import randint
from threading import Thread, Event
from persistence import Persistent
from utils import RunnableObjectInterface, Status, SensorInterface
from flask_api import FlaskAPI

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

"""


class DHT11(SensorInterface):
    def __init__(self):
        pass

    def measure(self):
        return randint(100,999)

    def stop(self):
        pass

    def __str__(self):
        return "DHT11"

    def __repr__(self):
        return str(self)


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

    def start(self):
        # Parse file
        # Init main service
        self.add_service(service_id = "SENSOR_1", service = Service(Sensor(DHT11(), name="DHT11_in", on_measure=self.update_data), delay=2))
        self.add_service(service_id = "SENSOR_2", service = Service(Sensor(DHT11(), name="DHT11_out", on_measure=self.update_data), delay=1))
        db = Persistent({"measure": self.data, "service": self.services})
    
        self.add_service(service_id = "DB", service = Service(db, delay=20))
        self.add_service(service_id = "HTTP", service = Service(FlaskAPI(db)))

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
    #logging.basicConfig(filename='example.log',level=logging.DEBUG)
    #logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    try:
        start()
    except KeyboardInterrupt:
        logging.warning('KeyboardInterrupt')
    except:
        # Get exception that is currently being handled
        e = sys.exc_info()
        logging.exception(e)
    finally:
        stop()
else:
    logging.error(f"{__name__} : must be run as a script\n")
