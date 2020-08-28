#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# --- Tester MQTT en ligne de commande ---

# MQTT server
sudo apt install mosquitto -y
# MQTT client
sudo apt install mosquitto-clients -y

# Run MQTT Broker
mosquitto
# Connect to MQTT broker and subscribe to channel1
mosquitto_sub -h 127.0.0.1 -v -t channel1
# Connect to MQTT broker and send message to channel1
mosquitto_pub -h 127.0.0.1 -t channel1 -m "Test Payload Message"

# A tester : Éteignez le Raspberry Pi avec le Broker et le subscriber. Démarrez ensuite le publisher. Regardez ce qui se passe…

# --- === ---

# --- ThingsBoard : Open-source IoT Platform ---
# https://thingsboard.io/
# https://thingsboard.io/docs/samples/raspberry/temperature/
# https://thingsboard.io/docs/user-guide/install/rpi/
# --- === ---

# --- Install MQTT dependencies for Python ---
sudo pip3 install paho-mqtt

# Maybe useless : 
sudo apt-get install python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
# --- === ---

"""

import time
import paho.mqtt.client as mqtt

# Set access token
# client.username_pw_set(ACCESS_TOKEN)

try:
    client = mqtt.Client()
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    while True:
        client.publish("channel1", "New Message", 1)
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()


