#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import paho.mqtt.client as mqtt

# Set access token
# client.username_pw_set(ACCESS_TOKEN)


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

try:
	client = mqtt.Client()
	client.connect("127.0.0.1", 1883, 60)
	client.subscribe('channel1', 1)
	client.loop_start()
	client.on_message = on_message
	while True:
		time.sleep(5)
except KeyboardInterrupt:
	pass
finally:
	client.loop_stop()
	client.unsubscribe('channel1')
	client.disconnect()


