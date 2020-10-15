#!/usr/bin/env python3
# -*- coding: utf-8 -*

from enum import Enum
import abc


class Status(Enum):
    CREATED = 'created'
    RUNNING = 'running'
    WAITING = 'waiting'
    BLOCKED = 'blocked'
    TERMINATED = 'terminated'

class RunnableObjectInterface(abc.ABC):
    @abc.abstractmethod
    def do(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

class SensorInterface(abc.ABC):
    @abc.abstractmethod
    def measure(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass



