# -*- coding: utf-8 -*-
from enum import Enum
import sys
import abc


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


class Message:
    @staticmethod
    def err(msg):
        sys.stderr.write(f"Error : {msg}\n")
        # sys.exit(1)

    @staticmethod
    def std(msg=""):
        sys.stdout.write(f"{msg}\n")

    @staticmethod
    def wrn(msg):
        pass
