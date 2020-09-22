#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import time

# TODO fix this shitty import
sys.path.insert(1, '../sensor_camera_module')
from DHT11 import DHT11
from utils import Message, Status, ServiceObjectInterface

# Custom Modules
# from embedded_server.sensor_camera_module.DHT11 import DHT11
# from embedded_server.smart4l_service.utils import Message, Status, ServiceObjectInterface

from smart4l import Smart4l
from sensor import Sensor
from service import Service
from smart4l_socket import Smart4lClient


# execute only if run as a script
if __name__ == "__main__":

    app = Smart4l()

    socket = Smart4lClient()
    app.add_service(
        Service(
            Sensor(DHT11(), "DHT11 RPI2", socket.send_message),
            timeout=1,
            name="Temperature RPI2",
        )
    )

    app.reload()

    try:
        # Infinite loop for keyboard interuption
        while True:
            continue
    except KeyboardInterrupt:
        app.stop()
else:
    Message.err(f"{__name__} : must be run as a script\n")
