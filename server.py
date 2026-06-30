import asyncio
import websockets
import json
import datetime
from config import LOCAL_HOST, LOCAL_PORT, GRAPH_UPDATE_INTERVAL

class Server:
    def __init__(self, order_book):
        self.order_book = order_book
        self.host = LOCAL_HOST
        self.port = LOCAL_PORT

    async def run(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

    async def handle_client(self, ws):
        try:    
            while True:
                snapshot = self.order_book.charting_data()
                snapshot["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                await ws.send(json.dumps(snapshot))
                await asyncio.sleep(GRAPH_UPDATE_INTERVAL)
        except websockets.exceptions.ConnectionClosed:
            pass