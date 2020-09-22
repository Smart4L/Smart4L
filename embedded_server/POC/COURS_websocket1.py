#!/usr/bin/env python3
# -*- coding: utf-8 -*

# Regarder un jeux multi websockets
# Regarder Google doc websockets
# regarder tornado websockets

"""
https://stackoverflow.com/questions/40158596/which-python-library-should-i-use-socketserver-or-asyncio

"""

# --- Cours 1 ---
"""
https://www.youtube.com/watch?v=7i0-lYjtvIE
"""
# ws_client
import asyncio
import websockets


async def message():
    async with websockets.connect("ws://localhost:8520") as socket:
        await socket.send("Test message")
        print(await socket.recv())


asyncio.get_event_loop().run_until_complete(message())

# ws_server
async def response(websocket, path):
    message = await websocket.recv()
    print(f"Message from client : {message}")
    await websocket.send("Message recv confirmation")


start_server = websockets.serve(response, 'localhost', 8520)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


import asyncio
import websockets


async def response(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Message from client : {message}")
        await websocket.send(f"Hey {message}")


start_server = websockets.serve(response, 'localhost', 8520)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# --- -------------------------------------- ---

# --- Cours 2 ♥ ---
"""
https://www.youtube.com/watch?v=8ARodQ4Wlf4
"""
# Libraries :
# flask_sockets
# python_socketio
# flask_socketio

# --- --------------------------------------- ---

# --- Cours 3 ♥ ---
"""
https://www.youtube.com/watch?v=6oQuQ5coSQ0
"""

# libraries
# tornado, async web framework
# django is sync web framework, look django channels
# websockets

"""
avec la classe WebSocketHandler
1 - Faire une liste de tous les websockets
2 - Faire une liste de tous les messages

onOpen → add client to wsList, send all the messages to the new client
onMessage → add it to messageList and send it to every client 
onClose → delete client from wsList

En websockets il faut implémenter le drop de connexion, les erreurs diverses etc...
"""


# --- --------------------------------------- ---

# --- Cours 4 ---
"""
https://www.youtube.com/watch?v=AcZJUQ3y2ek
"""


# --- --------------------------------------- ---

# --- Cours 5 ---
"""
https://www.youtube.com/watch?v=F3pB0PHcUxE
"""
# Code a revoir

# ws_server
import ssl
import pathlib
import asyncio
import websockets


async def response(websocket, path):
    message = await websocket.recv()
    print(f"Message from client : {message}")
    await websocket.send("Message recv confirmation")


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name("mycert.pem"),
    keyfile=pathlib.Path(__file__).with_name("mykey.key"),
)


start_server = websockets.serve(response, 'localhost', 8520, ssl=ssl_context)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# ws_client TODO Find WSS with websockets not websocket
import asyncio
import websocket


async def message():
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect("wss://localhost:8520")
    msg = input("Message to send >")
    ws.send(msg)
    print(ws.recv())


asyncio.get_event_loop().run_until_complete(message())


# --- Cours 6 ---
"""
https://www.youtube.com/watch?v=L5YQbNrFfyw
"""


# --- --------------------------------------- ---
