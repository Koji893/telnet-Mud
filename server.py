
import asyncio
class Client:
    def __init__(self,reader,writer):
        self.reader= reader
        self.writer = writer
        self.address= writer.get_extra_info('peername')
        self.userdata= {}

    async def send(self, message):
            self.writer.write(message.encode('utf-8'))
            await self.writer.drain()
    async def receive(self):
        try:
            data = await self.reader.readline()
            return data.decode('utf-8').strip()
        except:
            return None
    def close(self):
        self.writer.close()


class Server:
    def __init__(self, host, port, client_handler):
        self.host = host
        self.port = port
        self.client_handler = client_handler
        self.clients = []
    async def handle_connection(self,reader,writer):
        client = Client(reader, writer)
        self.clients.append(client)
        await self.client_handler(client)
        client.close()
        self.clients.remove(client)

    async def start(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'serving on {addr}')
        async with server:
            await server.serve_forever()
