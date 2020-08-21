#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

import random


class DHT11:

    def measure(self):
        return 42 + random.randint(0, 5)

    def clean(self):
        pass
