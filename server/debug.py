# debug.py
import json
import os

DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

debug_data = json.dumps({
    "event": "request",
    "data": {
        "room": "debug_room",
        "content": "https://www.example.com"
    }
}).encode()

debug_address = ('127.0.0.1', 12345)

async def get_debug_data():
    return debug_data, debug_address

async def print_debug_info(data, address):
    print(f"Debug: Received {len(data)} bytes from {address}")
    print(f"Debug: Received data : {data.decode()}")