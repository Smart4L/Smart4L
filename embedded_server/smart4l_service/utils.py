# -*- coding: utf-8 -*-

import abc
import sys
from enum import Enum


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


class Message():
	@staticmethod
	def err(msg):
		sys.stderr.write(f"Error : {msg}\n")
		#sys.exit(1)
	
	@staticmethod
	def out(msg=""):
		sys.stdout.write(f"{msg}\n")

	@staticmethod
	def wrn(msg):
		pass
