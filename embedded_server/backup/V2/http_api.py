# -*- coding: utf-8 -*-

import requests
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, join_room, leave_room
from utils import Message, Status, ServiceObjectInterface


class FlaskAPI(ServiceObjectInterface):
    def __init__(self, db):
        self.db = db
        self.conf = {"host": "localhost", "port": 80}

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)
        self.app.add_url_rule('/history', 'history', self.history)
        self.app.add_url_rule('/service', 'service', self.service)
        self.app.add_url_rule('/measure', 'measure', self.measure)

    def do(self):
        self.app.run(**self.conf)

    def index(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(self.db.app.data)

    def history(self):
        # TODO fix this ugly thing, should not use app variable
        return jsonify(self.db.history())

    def service(self):
        return jsonify(str(self.db.app.services))

    def measure(self, data):
        self.socketio.emit('receive_message', data)

    # Must be call from HTTP request
    def shutdown(self):
        app_shutdown = request.environ.get('werkzeug.server.shutdown')
        if app_shutdown is None:
            raise RuntimeError(
                "Http FlaskAPI can\'t be shutdown with this server version, check for WSGI version"
            )
        else:
            app_shutdown()
        return "FlaskAPI shuting down ..."

    def stop(self):
        requests.get(
            f"http://{self.conf.get('host')}:{self.conf.get('port')}/shutdown"
        )
