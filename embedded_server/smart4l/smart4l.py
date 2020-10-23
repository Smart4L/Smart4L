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


openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ws_cert.key -out ws_cert.pem
enable self signed certs on chrome : chrome://flags/#allow-insecure-localhost    
        
"""
import asyncio
import store_smart4l
from app_smart4l import *
import logging
import sys
import signal
from persistence import Persistent
from flask_api import FlaskAPI
from smart4l_ws_server import Smart4lWebSocket
from utils import RunnableObjectInterface, Status, SensorInterface

from mock_sensor import DHT11

"""

sys.path.insert(1, './sensor_camera_module')
import asyncio
import datetime
import json
from threading import Thread, Event
import time
from random import randint
from DS18B20 import DS18B20
from HCSR04 import HCSR04
"""


def init_service():
    store_smart4l.services = {}
    store_smart4l.last_measure = {}
    # - Measure service -
    store_smart4l.app = Smart4LApp()
    # - Database service -
    store_smart4l.database = Persistent()
    # - Websocket service -
    loop = asyncio.get_event_loop()
    #store_smart4l.websocket_server = Smart4lWebSocket(loop, host="127.0.0.1", port=store_smart4l.port_websocket_server, ssl_key_path="ws_cert.key", ssl_cert_path="ws_cert.pem", data=self.data)
    store_smart4l.websocket_server = Smart4lWebSocket(loop, host="127.0.0.1", port=store_smart4l.port_websocket_server)
    # - Http service -
    store_smart4l.http_api = FlaskAPI(host="127.0.0.1", port=store_smart4l.port_http_api_server)
    #self.http_api = FlaskAPI(self.db, host="localhost", port=8080, ssl_key_path="ws_cert.key", ssl_cert_path="ws_cert.pem")

    store_smart4l.app.add_service(service_id = "DB", service = Service(store_smart4l.database, delay=20))
    store_smart4l.app.add_service(service_id = "HTTP", service = Service(store_smart4l.http_api))
    store_smart4l.app.add_service(service_id = "WS_SERVER", service = Service(store_smart4l.websocket_server))
    # Parse file and add sensor service
    store_smart4l.app.add_service(service_id = "SENSOR_1", service = Service(Sensor(DHT11(), name="DHT11_in", on_measure=store_smart4l.app.update_data), delay=2))
    store_smart4l.app.add_service(service_id = "SENSOR_2", service = Service(Sensor(DHT11(), name="DHT11_out", on_measure=store_smart4l.app.update_data), delay=3))
    """
    store_smart4l.app.add_service(service_id = "SENSOR_ENGINE", service = Service(Sensor(DS18B20(), name="DS18B20_engine", on_measure=self.update_data), delay=1))
    store_smart4l.app.add_service(service_id = "SENSOR_DISTANCE", service = Service(Sensor(HCSR04(), name="HC-SR04_arriere", on_measure=self.update_data), delay=1))
    """

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

app = Smart4LApp()
def main():
    #logging.basicConfig(filename=f'example{datetime.time}.log',level=logging.DEBUG)
    #logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    #logging.basicConfig(filename=f'smart4l.log',level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    logging.basicConfig(level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    signal.signal(signal.SIGTERM, stop)
    try:
        init_service()
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

# Execute only if run as a script
if __name__ == "__main__":
    main()
else:
    logging.critical(f"{__name__} : must be run as a script\n")






















