#!/usr/bin/env python3
# -*- coding: utf-8 -*

import logging
import requests
import ssl

from flask import Flask, jsonify, request, render_template
from utils import RunnableObjectInterface

class FlaskAPI(RunnableObjectInterface):
    
    def __init__(self, data, host, port, ssl_key_path=None, ssl_cert_path=None):
        self.app = Flask(__name__)
        if ssl_key_path is not None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(ssl_cert_path, ssl_key_path)
            self.conf = {"host": host, "port": port, "ssl_context":context}
        else:
            self.conf = {"host": host, "port": port}
        self.db = data
    
        self.router()
   
    def router(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/service', 'service', self.service)
        self.app.add_url_rule('/history', 'history', self.history)
        self.app.add_url_rule('/log', 'log', self.log)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)

    def do(self):
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

    def log(self):
        with open ("smart4l.log", "r") as smart4l_log_file:
            return smart4l_log_file.readlines()

    def stop(self):
        if self.conf.get("ssl_context", None) is None:
            requests.get(f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown", verify=False)
        else:
            requests.get(f"https://{self.conf.get('host')}:{self.conf.get('port')}/shutdown", verify=False)




