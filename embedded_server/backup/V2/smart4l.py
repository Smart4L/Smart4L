# -*- coding: utf-8 -*-

from utils import Message, Status, ServiceObjectInterface

# Class des gestions de l'application / service
class Smart4l:
    # TODO implement Early Loading Singleton

    def __init__(self):
        # TODO implement message Queue
        Message.out("Started !")
        self.socket = None
        self.persistent = None
        self.httpApi = None
        self.websocket = None

        self.data = {}
        self.services = []

        Message.out("Running ...")

    def update_measure(self, uid, value):
        self.data[uid] = value
        # emit websocket event

    def reload(self):
        [
            service.__start__()
            for service in self.services
            if not service.is_alive()
        ]

    def add_service(self, service):
        self.services.append(service)
        # Must use reload function to start the new service

    def stop(self):
        Message.out("\nCleaning ...")
        [service.stop() for service in self.services]
        self.services = []
        Message.out("Stopped !")
