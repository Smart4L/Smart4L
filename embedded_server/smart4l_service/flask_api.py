#!/usr/bin/env python3
# -*- coding: utf-8 -*

import logging
import requests
from flask import Flask, jsonify, request, render_template
from utils import RunnableObjectInterface

class FlaskAPI(RunnableObjectInterface):
    def __init__(self, data):
        self.app = Flask(__name__)
        self.conf = {"host": "localhost", "port": 8080}

        self.db = data
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/service', 'service', self.service)
        self.app.add_url_rule('/history', 'history', self.history)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)

    def do(self,):
        self.app.run(**self.conf)

    def index(self):
        return jsonify(self.db.data["measure"])

    def service(self):
        return jsonify(str(self.db.data["service"]))

    def history(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(self.db.history())

    # Must be call from HTTP request
    def shutdown(self):
        app_shutdown = request.environ.get('werkzeug.server.shutdown')
        if app_shutdown is None:
            raise RuntimeError("Http FlaskAPI can\'t be shutdown with this server version, check for WSGI version")
        else:
            app_shutdown()  
        return "FlaskAPI shuting down ..."

    def stop(self):
        requests.get(f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown")




