#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from smart4l_socket import Smart4lServer
from smart4l import Smart4l
from service import Service
import sys


def none():
    pass


app = Smart4l()
try:
    app.add_service(Service(Smart4lServer(none)))

    app.reload()
    while True:
        continue
except KeyboardInterrupt:
    app.stop()
