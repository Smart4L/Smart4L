# -*- coding: utf-8 -*-
from enum import Enum

class Status(Enum):
	START = 'start'
	STOP = 'stop'
	RESTART = 'restart'


class Message():
	def error(self, msg):
		sys.stderr.write("Error : " + msg)
		#sys.exit(1)
