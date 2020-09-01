#!/usr/bin/env python3
# -*- coding: utf-8 -*




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


# --- -------------------------------------- ---

# --- Cours 2 ---
"""
https://www.youtube.com/watch?v=8ARodQ4Wlf4
"""



# --- --------------------------------------- ---

# --- Cours 3 ---
"""
https://www.youtube.com/watch?v=6oQuQ5coSQ0
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






