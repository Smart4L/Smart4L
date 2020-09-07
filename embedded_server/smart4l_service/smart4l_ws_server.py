#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import pathlib
import ssl
import time
import websockets
from random import randint
from threading import Thread
from websockets import WebSocketServerProtocol


logging.basicConfig(level=logging.INFO)

class ServerWS():
    clients = set()
    
    # add client to clients list
    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects.")


    # remove client from clients list
    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        await ws.close(1000,"Normal Closure")
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects.")


    # send message to one client
    async def send_to_client(self, ws: WebSocketServerProtocol, message: str) -> None:
        await ws.send(message)

    # Send message to all clients
    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])


    # TODO find what do this thing
    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            # Start communication
            await self.distribute(ws)
        finally:
            # Remove client from clients list
            await self.unregister(ws)


    # TODO find what do this thing
    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        # TODO find what do this thing
        async for message in ws:
            await self.send_to_clients(message)


    # Close connection for all client in clients list 
    async def close_all_connections(self):
        await asyncio.wait([self.unregister(client) for client in self.clients])

    def stop(self):
        pass
        #loop.close()

server = ServerWS()


def runWebsocket(loop: asyncio.AbstractEventLoop) -> None:
    global server
    #const ws = new WebSocket('wss://localhost:8443/cart', { rejectUnauthorized: false });
    
    asyncio.set_event_loop(loop)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("ws_cert.pem")
    #ssl_context.load_cert_chain(localhost_pem)
    ssl_context.load_cert_chain('ws_cert.pem', 'ws_cert.key')
    """
    ssl.SSLError: [SSL] PEM lib (_ssl.c:3524) : https://fenghe.us/ssl-sslerror-ssl-pem-lib-_ssl-c3824-python-websockets-ssl/
    enable self signed certs on chrome : chrome://flags/#allow-insecure-localhost    
    
    """
    start_server = websockets.serve(server.ws_handler, "127.0.0.1", 8520, ssl=ssl_context)
    
    #start_server = websockets.serve(server.ws_handler, "127.0.0.1", 8520)
    
    loop.run_until_complete(start_server)
    loop.run_forever()


loop = asyncio.get_event_loop()

t = Thread(target=runWebsocket, args=(loop,))
t.start()

"""
Self Signed :
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

 Fix SSH issues en combinant les fichiers, la clé dans le certificat WTF !
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ws_cert.key -out ws_cert.pem

https://github.com/jupyter/notebook/issues/507
https://docs.python.org/3/library/ssl.html#module-ssl
https://github.com/bsergean/websockets/tree/master/example
https://websockets.readthedocs.io/en/stable/intro.html#
"""
try:
    while True:
        asyncio.run_coroutine_threadsafe(server.send_to_clients(str(randint(100,999))), loop)
        
        # Delay Between WebSocket Message
        time.sleep(0.001)


except KeyboardInterrupt:
    task = asyncio.run_coroutine_threadsafe(server.close_all_connections(), loop)
    loop.stop()
    
    """
    while loop.is_running():
        pass
    task.cancel()
    while task.done():
        pass
    loop.close()
    """






