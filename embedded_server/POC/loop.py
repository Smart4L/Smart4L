#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import abc
from enum import Enum
from threading import Thread


class Status(Enum):
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'


class ServiceObjectInterface(abc.ABC):
    @abc.abstractmethod
    def do(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class Wrapper(Thread):
    def __init__(self, service_object: ServiceObjectInterface):
        super().__init__()
        self.service_object = service_object
        self.status = Status.START.value

    def run(self):
        while self.status == Status.START.value:
            self.service_object.do()

    def stop(self):
        self.status = Status.STOP.value
        self.service_object.stop()
        print("Stopped !")


class TestRunner(ServiceObjectInterface):
    def __init__(self):
        self.status = Status.START.value

    def do(self):
        while self.status == Status.START.value:
            print("running ...")
            time.sleep(1)

    def stop(self):
        self.status = Status.STOP.value


w = Wrapper(TestRunner())
w.start()
time.sleep(5)
w.stop()
