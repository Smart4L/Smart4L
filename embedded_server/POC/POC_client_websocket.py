#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import websockets
import logging
from websockets import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"Message: {message}")


loop = asyncio.get_event_loop()
loop.run_until_complete(consume(hostname="127.0.0.1", port=8520))
loop.run_forever()
