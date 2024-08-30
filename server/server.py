import asyncio
import socket
from server.handler import handle_data
from server.debug import DEBUG_MODE, get_debug_data, print_debug_info

class UDPServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.queue = asyncio.Queue()

    async def start(self):
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
        sock.bind((self.ip_address, self.port))

        print(f"Server listening on {self.ip_address}:{self.port}")

        asyncio.create_task(self.worker())

        if DEBUG_MODE:
            data, address = await get_debug_data()
            await self.queue.put((data, address, sock))
            await asyncio.sleep(9999999)

        else:
            while True:
                data, address = await asyncio.wait_for(self.recvfrom(sock), timeout=None)
                print(f"Received {len(data)} bytes from {address}")
                print(f"Received data : {data.decode()}")
                await self.queue.put((data, address, sock))

    async def recvfrom(self, sock: socket.socket):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sock.recvfrom, 4096)

    async def worker(self):
        while True:
            data, address, sock = await self.queue.get()
            data: bytes
            address: tuple
            sock: socket.socket
            response = await handle_data(data)
            print(f"Sent {len(response)} bytes back to {address}")
            await asyncio.wait_for(self.sendto(sock, response.encode(), address), timeout=None)
            self.queue.task_done()

    async def sendto(self, sock: socket.socket, data, address):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sock.sendto, data, address)