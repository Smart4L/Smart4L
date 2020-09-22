#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from random import randint

"""
1 - Le serveur ouvre un socket d'écoute et attend
2 - Un client se connecte au socket d'écoute du serveur
3 - Le serveur crée un nouveau socket unique et l'envoie au client pour communiquer avec lui
"""


class Server:
    def __init__(self):
        # Connexion en mode IPV4 avec le protocole TCP
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Précisez une ip permet de restreindre les connexion sur une interface réseaux précise, le port est compris entre 1-65535, Some systems may require superuser privileges if the port is < 1024.
        self.connection.bind(('', 8520))
        # Nombre de connection maximum en attente d'acceptation, peut être laissé vide
        self.connection.listen(5)
        # Attente d'une connexion cliente, renvoie le socket de communication et l'ip du client dans la configuration IPV4, légèrement différent pour IPV6
        self.conn, self.addr = self.connection.accept()

        with self.conn:
            print('Connected by', self.addr)
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                self.conn.sendall(data)

        # Fermeture du socket de communication avec le client
        # self.client.close()

    def stop(self):
        # Fermeture du socket d'écoute du serveur
        self.connection.close()


class Client:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('127.0.0.1', 8520))

        self.connection.sendall("I'm new client".encode('utf-8'))
        data = self.connection.recv(1024)
        print(f"Received : {repr(data)}")

    def stop(self):
        self.connection.close()
