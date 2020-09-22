#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import ssl
import time
import websockets
from random import randint
from threading import Thread
from websockets import WebSocketServerProtocol


class ServerWS:
    clients = set()
    async def register(self, ws: WebSocketServerProtocol):
        """Add client to clients list"""
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects.")

    async def unregister(self, ws: WebSocketServerProtocol):
        """Remove client from clients list"""
        await ws.close(1000, "Normal Closure")
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects.")

    async def send_to_client(
        self, ws: WebSocketServerProtocol, message: str
    ):
        """Send message to one client"""
        await ws.send(message)

    async def send_to_clients(self, message: str):
        """Send message to all clients"""
        if self.clients:
            await asyncio.wait(
                [client.send(message) for client in self.clients]
            )

    # TODO find what do this thing
    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str):
        await self.register(ws)
        try:
            # Start communication
            await self.distribute(ws)
        finally:
            # Remove client from clients list
            await self.unregister(ws)

    # TODO find what do this thing
    async def distribute(self, ws: WebSocketServerProtocol):
        # TODO find what do this thing
        async for message in ws:
            await self.send_to_clients(message)

    async def close_all_connections(self):
        """Close connection for all client in client list"""
        await asyncio.wait(
            [self.unregister(client) for client in self.clients]
        )


class Smart4lWebSocket:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        host: str,
        port: int,
        ssl_key_path: str,
        ssl_cert_path: str,
    ):
        self.loop = loop
        self.ws_server = ServerWS()
        self.conf = {
            "host": host,
            "port": port,
            "ssl_cert": ssl_cert_path,
            "ssl_key": ssl_key_path,
        }

    def do(self):
        asyncio.set_event_loop(self.loop)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            self.conf["ssl_cert"], self.conf["ssl_key"]
        )
        start_server = websockets.serve(
            self.ws_server.ws_handler,
            self.conf["host"],
            self.conf["port"],
            ssl=ssl_context,
        )
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    def stop(self):
        # TODO Look at this example : https://github.com/bsergean/websockets/blob/master/example/shutdown.py
        asyncio.run_coroutine_threadsafe(
            self.ws_server.close_all_connections(), self.loop
        )
        self.loop.stop()

    def send_message(self, message: str):
        asyncio.run_coroutine_threadsafe(
            self.ws_server.send_to_clients(str(message)), self.loop
        )
