# -*- coding: utf-8 -*-
import store_smart4l
import json
from threading import Thread, Event
from utils import RunnableObjectInterface, Status, SensorInterface


class Service(Thread):
    def __init__(self, runnable_object : RunnableObjectInterface, delay : int=0):
        Thread.__init__(self)
        self.delay_between_tasks = delay
        self.runnable_object = runnable_object

        self.status = Status.CREATED.value
        self.event_stop_service = Event()

    def run(self):
        self.status = Status.RUNNING.value
        while self.status == Status.RUNNING.value:
            self.runnable_object.do()
            self.event_stop_service.wait(self.delay_between_tasks)

    def stop(self):
        self.status = Status.TERMINATED.value
        self.event_stop_service.set()
        self.runnable_object.stop()

    def __str__(self):
        return f"Current status: {self.status} - RunnableObject {str(self.runnable_object)} - Delay {str(self.delay_between_tasks)}"

    def __repr__(self):
        return str(self)



class Sensor(RunnableObjectInterface):
    def __init__(self, sensor_object, name, on_measure):
        self.sensor_object = sensor_object
        self.on_measure = on_measure
        self.name = name

    def do(self):
        self.on_measure(self.name, self.sensor_object.measure())        

    def stop(self):
        pass

    def __str__(self):
        return f"{str(self.sensor_object)} : {self.name}"

    def __repr__(self):
        return str(self)



class Smart4LApp():
    
    def start(self):
        # Init main service
        
        # Launch service
        self.reload_services()

    def reload_services(self):
        [service.start() for service_id, service in store_smart4l.services.items() if not service.is_alive()]

    def stop(self):
        [service.stop() for service_id, service in store_smart4l.services.items()]

    def add_service(self, service_id:int, service:Service):
        # TODO : Check if service_id not already exists
        store_smart4l.services[service_id]=service
        

    def update_data(self, uid, value):
        # If value has not changed exit
        if uid in store_smart4l.last_measure.keys() and store_smart4l.last_measure[uid] == value:
            return

        store_smart4l.websocket_server.send_message(json.dumps( {"type": "UPDATE_SENSOR", "content": {"id": uid,"value": value}}))
        store_smart4l.last_measure[uid] = value
        
    def parse_service_file(self):
        pass

