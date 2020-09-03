#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import time
from threading import Thread
import websockets
from random import randint
from websockets import WebSocketServerProtocol


logging.basicConfig(level=logging.INFO)

"""
avec la classe WebSocketHandler
1 - Faire une liste de tous les websockets
2 - Faire une liste de tous les messages

onOpen → add client to wsList, send all the messages to the new client
onMessage → add it to messageList and send it to every client 
onClose → delete client from wsList

En websockets il faut implémenter le drop de connexion, les erreurs diverses etc...

https://www.youtube.com/watch?v=n9mRjkQg3VE
Short Polling
Long Polling
SSE Server-Sent Events
WebSockets

Multiplex connection
Bidirectional connection


https://www.freecodecamp.org/news/how-to-secure-your-websocket-connections-d0be0996c556/
https://www.youtube.com/watch?v=sUEq35F-ELY

https://www.youtube.com/watch?v=cXxEiWudIUY
"""

class ServerWS():
    clients = set()
    messages = []

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
        self.messages.append(message)
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])


    # TODO find what do this thing
    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            # Flush all previous messages to the new client
            [await self.send_to_client(ws, message) for message in self.messages]
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
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(server.ws_handler, "127.0.0.1", 8520)
    loop.run_until_complete(start_server)
    loop.run_forever()




loop = asyncio.get_event_loop()

t = Thread(target=runWebsocket, args=(loop,))
t.start()


try:
    while True:
        asyncio.run_coroutine_threadsafe(server.send_to_clients(str(randint(100,999))), loop)
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







# --- ----------------------------------------------------- ---

# https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058
"""
def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def get_title(html: str) -> Optional[str]:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.title.string


async def fetch(url: str, session: aiohttp.ClientSession = None) -> Tuple[str, str]:
    async def _fetch(url: str, session: aiohttp.ClientSession):
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return url, get_title(html)

    if session:
        return await _fetch(url, session)
    else:
        async with aiohttp.ClientSession() as session:
            return await _fetch(url, session)

async def fetch_urls(loop: asyncio.AbstractEventLoop) -> Sequence[Tuple[str, str]]:
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(fetch(url, session)) for url in URLS]
        results = await asyncio.gather(*tasks)
        return results



loop = asyncio.new_event_loop()
t = Thread(target=start_background_loop, args=(loop,), daemon=True)
t.start()



"""

