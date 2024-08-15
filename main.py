import asyncio
from server.server import UDPServer

async def main():
    udpServer = UDPServer('0.0.0.0', 8000)
    await udpServer.start()

if __name__ == "__main__":
    asyncio.run(main())
