# -*- coding: utf-8 -*-
import sys
from enum import Enum


class Status(Enum):
	START = 'start'
	STOP = 'stop'
	RESTART = 'restart'


class Message:

	@staticmethod
	def error(msg):
		sys.stderr.write("Error : " + msg)
		# sys.exit(1)
