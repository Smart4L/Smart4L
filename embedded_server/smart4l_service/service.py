# -*- coding: utf-8 -*-

from threading import Thread, Event
from utils import Message, Status, ServiceObjectInterface


# Class de gestions de service
class Service(Thread):
    def __init__(self, service_object: ServiceObjectInterface, timeout=0, name="unname", description="description unavailable"):
        Thread.__init__(self)
        self.status = Status.START.value
        self.eventStopService = Event()

        self.serviceObject = service_object
        self.timeout = timeout
        self.name = name
        self.description = description

    def run(self):
        while self.status == Status.START.value:
            self.serviceObject.do()
            self.eventStopService.wait(self.timeout)

    def __start__(self):
        Message.out(f"Service \"{self.name}\" is now started")
        self.start()

    def __repr__(self):
        return f"{self.name}: {self.description}"

    def stop(self):
        self.status = Status.STOP.value
        self.eventStopService.set()
        self.serviceObject.stop()
