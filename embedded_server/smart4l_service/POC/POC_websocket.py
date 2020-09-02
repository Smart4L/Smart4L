#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
pip3 install websockets
https://websockets.readthedocs.io/en/stable/intro.html
https://websockets.readthedocs.io/en/stable/intro.html
https://pypi.org/project/websocket_client/
https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549

Learn asyncio, async, await, signal
"""


# WS server example
"""
import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


start_server = websockets.serve(hello, "127.0.0.1", 8520)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
"""



import time
import websockets
import asyncio
import logging
from random import randint
from websockets import WebSocketServerProtocol


logging.basicConfig(level=logging.INFO)


class ServerWS():
    clients = set()
    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects.")

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects.")

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)

    async def closeAllConnections(self):
        pass



server = ServerWS()

start_server = websockets.serve(server.ws_handler, "127.0.0.1", 8520)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()






