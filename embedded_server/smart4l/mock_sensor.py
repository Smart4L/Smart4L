# -*- coding: utf-8 -*-


from random import randint
from utils import SensorInterface

class DHT11(SensorInterface):
    def __init__(self, pin=None):
        pass

    def measure(self):
        temperature = 15+randint(0,20)
        humidity = 80+randint(0,20)
        return {"temperature": temperature  ,"humidity": humidity}

    def stop(self):
        pass

    def __str__(self):
        return "DHT11"

    def __repr__(self):
        return str(self)





class DS18B20(SensorInterface):
    def __init__(self, id=None):
        self.id_sonde = id

    def measure(self):
        if self.id_sonde is None:
            return 42
        return str(float(open("/sys/bus/w1/devices/%s/w1_slave" % self.id_sonde).read().split()[-1][2:])/1000)

    def stop(self):
        pass




class HCSR04(SensorInterface):
    def __init__(self, echo_pin=None, trigger_pin=None):
        pass

    def measure(self):
        return randint(1,4)

    def stop(self):
        pass
