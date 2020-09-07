# -*- coding: utf-8 -*-

from utils import Message, Status, ServiceObjectInterface


# TODO rework this class
class Sensor(ServiceObjectInterface):
    def __init__(self, sensor_object, uid, do_func):
        self.sensorObject = sensor_object
        self.uid = uid
        self.doFunc = do_func

    def do(self):
        self.doFunc(self.uid, self.sensorObject.measure())

    def stop(self):
        self.sensorObject.clean()
