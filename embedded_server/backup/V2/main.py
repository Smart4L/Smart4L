#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "25-08-2020"
__version__ = "1.1.0"
__status__ = "Prototype"

"""
Conf GIL : https://www.youtube.com/watch?v=7SSYhuk5hmc
Conf expert : https://github.com/austin-taylor/code-vault/blob/master/python_expert_notebook.ipynb
Conf everything : https://github.com/hellerve/programming-talks#python

SQL Lite avec base en mémoire ♥: http://www.python-simple.com/python-autres-modules-non-standards/sqlite3.php

Decorateur property : https://www.freecodecamp.org/news/python-property-decorator/
Decorateur property : https://www.journaldev.com/14893/python-property-decorator

RestFull API with Flask : https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
API Temps réelle :  https://dvic.devinci.fr/resource/tutorial/api-python/
Site web avec Flask : https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask
Conf Flask : https://www.youtube.com/watch?v=1ByQhAM5c1I
Flask Socket : https://www.youtube.com/watch?v=uJC8A_7VZOA
Flask : https://realpython.com/flask-by-example-part-1-project-setup/ 

websocket : https://websockets.readthedocs.io/en/stable/intro.html
websocket : https://pypi.org/project/websocket_client/
websocket : https://websockets.readthedocs.io/en/stable/intro.html
websocket : https://pypi.org/project/websocket_client/
websocket : https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549
websocket : https://stackoverflow.com/questions/10112178/differences-between-socket-io-and-websockets
websocket : https://developerinsider.co/difference-between-http-and-http-2-0-websocket/#:~:text=WebSocket%20is%20a%20protocol%20providing,HTTP%20providing%20half%2Dduplex%20communication.&text=Means%2C%20server%20can%20push%20information,does%20not%20allow%20direct%20HTTP).
websocket : https://openclassrooms.com/fr/courses/1056721-des-applications-ultra-rapides-avec-node-js/1057825-socket-io-passez-au-temps-reel

Socket : https://www.youtube.com/watch?v=T0rYSFPAR0A
Socket : https://www.youtube.com/watch?v=Lbfe3-v7yE0
Socket : https://www.youtube.com/watch?v=3QiPPX-KeSc
Socket : https://realpython.com/python-sockets/
Socket : https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/234698-gerez-les-reseaux
Socket : https://docs.python.org/fr//3/howto/sockets.html

Wifi : https://www.framboise314.fr/raspap-creez-votre-hotspot-wifi-avec-un-raspberry-pi-de-facon-express/

MQTT : https://www.framboise314.fr/utiliser-le-protocole-mqtt-pour-communiquer-des-donnees-entre-2-raspberry-pi/
COAP : https://raspberry-valley.azurewebsites.net/CoAP-Getting-Started/

Singleton : https://medium.com/@sinethneranjana/5-ways-to-write-a-singleton-and-why-you-shouldnt-1cf078562376

Fichier property : 
"""


"""
Les classes doivent porter leurs fonctions métier

Résoudre un problème d'import cyclique en créant une classe plus haut niveau, les classes ne doivent pas s'autogérer...

Une classe n'est pas "programme" en soit, elle est piloté depuis l'extérieur

Singleton doit donner acces qu'a des variables imutables ou parfaitement encapsulé
"""


# Standard Library
import os
import sys
import time

# TODO fix this shitty import
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface

# Custom Modules
# from embedded_server.sensor_camera_module.DHT11 import DHT11
# from embedded_server.smart4l_service.utils import Message, Status, ServiceObjectInterface

from smart4l import Smart4l
from sensor import Sensor
from http_api import FlaskAPI
from persistent import Persistent
from service import Service


"""
dic = {'1Key':'1Value', '2Key':'2Value', '3Key':'3Value', '4Key':'4Value'}

for k,v in dic.items():
    print(f"{k}:{v}")
"""

# execute only if run as a script
if __name__ == "__main__":
    # --- PID FILE EXISTS ---
    if os.path.isfile('smart4l.lock'):
        # TODO check if python process run with this pid
        Message.wrn("PID file  already exists")
        os.remove("smart4l.lock")
    open("smart4l.lock", "w+").write(str(os.getpid()))
    # --- === ---

    app = Smart4l()

    app.persistent = Persistent(app)
    app.httpApi = FlaskAPI(app.persistent)
    app.socket = Smart4lServeur(app.update_measure)

    app.add_service(
        Service(Sensor(DHT11(), "DHT11", app.update_measure), 1, "Temperature")
    )
    app.add_service(Service(app.persistent, 20, "DB"))
    app.add_service(Service(app.httpApi, "API Http"))

    app.reload()

    try:
        # Infinite loop for keyboard interuption
        while True:
            continue
    except KeyboardInterrupt:
        app.stop()
        os.remove("smart4l.lock")
else:
    Message.err(f"{__name__} : must be run as a script\n")
