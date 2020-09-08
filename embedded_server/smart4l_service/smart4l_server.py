#!/usr/bin/env python3
# -*- coding: utf-8 -*

import logging
from utils import RunnableObjectInterface, Status

class Smart4lServer(RunnableObjectInterface):
	def __init__(self, on_receive):
		self.on_receive = on_receive
		self.status = Status.CREATED.value

	def do(self):
		self.status = Status.RUNNING.value
		while self.status == Status.RUNNING.value:
			pass
			# Start server

	def stop(self):
		pass

	def __str__(self):
        return f"Socket Server"

    def __repr__(self):
        return str(self)




