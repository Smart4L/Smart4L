# -*- coding: utf-8 -*-

import abc
import datetime
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Message():
	@staticmethod
	def err(msg):
		sys.stderr.write(f"{bcolors.FAIL}Error : {msg}{bcolors.ENDC}\n")
		#sys.exit(1)
	
	@staticmethod
	def out(msg=""):
		sys.stdout.write(f"{msg}\n")

	@staticmethod
	def wrn(msg):
		sys.stdout.write(f"{bcolors.WARNING}Warning : {msg}{bcolors.ENDC}\n")

	@staticmethod
	def log(msg):
		sys.stdout.write(f"{bcolors.BOLD}Log : {msg}{bcolors.ENDC}\n")

	@staticmethod
	def bold(msg):
		sys.stdout.write(f"{bcolors.BOLD}{msg}{bcolors.ENDC}\n")

	@staticmethod
	def underline(msg):
		sys.stdout.write(f"{bcolors.UNDERLINE}{msg}{bcolors.ENDC}\n")

	@staticmethod
	def header(msg):
		sys.stdout.write(f"{bcolors.HEADER}{msg}{bcolors.ENDC}\n")

	@staticmethod
	def okgreen(msg):
		sys.stdout.write(f"{bcolors.OKGREEN}{msg}{bcolors.ENDC}\n")

	@staticmethod
	def okblue(msg):
		sys.stdout.write(f"{bcolors.OKBLUE}{msg}{bcolors.ENDC}\n")



"""
Good example of method overriding
"""
class Logger(object):
    def log(self, message):
        print(message)

class TimestampLogger(Logger):
    def log(self, message):
        message = "{ts} {msg}".format(ts=datetime.datetime.now().isoformat(), msg=message)
        super(TimestampLogger, self).log(message)


