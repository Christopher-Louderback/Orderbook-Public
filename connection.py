from config import URL, PRODUCT_IDS
import logging
import websockets
import json

class Connection:
    def __init__(self, url, product_ids, order_book):
        self.url = url
        self.product_ids = product_ids
        self.order_book = order_book
        self.ws = None
        self.l2_message = { #messages should have jwt but yk
                "type": "subscribe",
                "product_ids": self.product_ids,
                "channel": "level2"
        }
        self.heartbeats_message = { #messages declared here or fully written in the send? DI? thinkl on it
                "type": "subscribe",
                "channel": "heartbeats"
        }
        self.l2_unsub = {
                "type": "unsubscribe",
                "product_ids": self.product_ids,
                "channel": "level2"
        }
        self.heartbeats_unsub = {
                "type": "unsubscribe",
                "channel": "heartbeats"
        }

    async def connect(self):
        logging.info(f"Attempting to connect to {self.url}.")

        try:
            async with websockets.connect(self.url) as ws:
                self.ws = ws

                await ws.send(json.dumps(self.l2_message))
                logging.info("Subscribed to level2 channel.")

                await ws.send(json.dumps(self.heartbeats_message))
                logging.info("Subscribed to heartbeats channel.")

                async for received_message in ws:
                    await self.handle_data(received_message)

        except KeyboardInterrupt:
            await self.disconnect()

        except Exception as e:
            logging.error(f"Connection error: {e}")


    async def disconnect(self):
        logging.info("Disconnecting.")

        await self.ws.send(json.dumps(self.l2_unsub))
        logging.info("Disconnected from level2 channel.")

        await self.ws.send(json.dumps(self.heartbeats_unsub))
        logging.info("Disconnected from heartbeats channel.")

    async def handle_data(self, received_message):#underscore?
        data = json.loads(received_message)
        print(data) #outputs to terminal
        channel = data.get("channel") #.get the right way to do this?

        if channel == "l2_data": #refactor so there's no if check before update call?
            event = data["events"][0]["type"]

            if event == "update":
                self.order_book.process_update(data)

            elif event == "snapshot":
                self.order_book.process_snapshot(data)
                logging.info("Initial data processed.")

        elif channel == "heartbeats":
            pass
