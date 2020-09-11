#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "25-08-2020"
__version__ = "1.1.0"
__status__ = "Prototype"

"""
RestFull API with Flask : https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
API Temps réelle :  https://dvic.devinci.fr/resource/tutorial/api-python/
Site web avec Flask : https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask
Some example : https://realpython.com/flask-by-example-part-1-project-setup/ 
Conf Flask : https://www.youtube.com/watch?v=1ByQhAM5c1I
Flask Socket : https://www.youtube.com/watch?v=uJC8A_7VZOA
Conf GIL : https://www.youtube.com/watch?v=7SSYhuk5hmc
Conf expert : https://github.com/austin-taylor/code-vault/blob/master/python_expert_notebook.ipynb
Conf everything : https://github.com/hellerve/programming-talks#python
SQL Lite avec base en mémoire ♥: http://www.python-simple.com/python-autres-modules-non-standards/sqlite3.php
Decorateur property : https://www.freecodecamp.org/news/python-property-decorator/
Decorateur property : https://www.journaldev.com/14893/python-property-decorator
Socket : https://www.youtube.com/watch?v=T0rYSFPAR0A
Socket : https://www.youtube.com/watch?v=Lbfe3-v7yE0
Socket : https://www.youtube.com/watch?v=3QiPPX-KeSc
Wifi : https://www.framboise314.fr/raspap-creez-votre-hotspot-wifi-avec-un-raspberry-pi-de-facon-express/
MQTT : https://www.framboise314.fr/utiliser-le-protocole-mqtt-pour-communiquer-des-donnees-entre-2-raspberry-pi/
websocket : https://websockets.readthedocs.io/en/stable/intro.html
websocket : https://pypi.org/project/websocket_client/

Fichier property : 


https://openclassrooms.com/forum/sujet/securisee-des-communications-avec-le-module-socket
https://riptutorial.com/fr/python/example/8622/hachage-de-mot-de-passe-securise
https://zestedesavoir.com/forums/sujet/9779/securiser-un-acces-socket/
https://diu-eil.gricad-pages.univ-grenoble-alpes.fr/archi-robotique-systeme-reseau/reseaux/cours_sockets_python.pdf
https://www.codeflow.site/fr/article/python-sockets
https://www.supinfo.com/articles/single/1027-cripts-python-faire-audits-securite
https://docs.python.org/fr//3/howto/sockets.html
https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMFHS-040/Python-et-le-reseau
https://fr.wikipedia.org/wiki/Low_Orbit_Ion_Cannon
https://fr.wikipedia.org/wiki/Script_kiddie

"""


"""
Les classes doivent porter leurs fonctions métier

Résoudre un problème d'import cyclique en créant une classe plus haut niveau, les classes ne doivent pas s'autogérer...

Une classe n'est pas "programme" en soit, elle est piloté depuis l'extérieur

Singleton doit donner acces qu'a des variables imutables ou parfaitement encapsulé
"""


# Standard Library
import logging
import os

import sys
import time

# TODO fix this shitty import
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface
import smart4_websocket
# Custom Modules
#from embedded_server.sensor_camera_module.DHT11 import DHT11
#from embedded_server.smart4l_service.utils import Message, Status, ServiceObjectInterface


# execute only if run as a script
if __name__ == "__main__":

    if os.path.isfile('smart4l.pid'):
        Message.wrn("PID file  already exists")
        os.remove("smart4l.pid")
    open("smart4l.pid","w+").write(str(os.getpid()))

    app = Smart4l()
    persistent = Persistent(data=app.lastMeasure)
    
    app.add_service(Service(service_object=persistent, timeout=20, name="Persistent"))
    app.add_service(Service(service_object=FlaskAPI(db=persistent), name="Http API"))
    app.add_service(Service(service_object=Capteur(DHT11(), "DHT11 ext", app.update_measure), timeout=0.2, name="DHT11 ext", description="Capteur de température extérieur"))
    app.add_service(Service(service_object=Capteur(DHT11(), "DHT11 int", app.update_measure), timeout=0.2, name="DHT11 int"))

    app.reload()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        app.stop()
        os.remove("smart4l.pid")
else:
    Message.err(f"{__name__} : must be run as a script\n")
