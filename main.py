from config import URL, PRODUCT_IDS
from order_book import OrderBook
from recorder import Recorder
from connection import Connection
from server import Server
import asyncio
import logging
import os

async def main(): #type = snapshot vs update important - should reconnect if sequence_num out of sync and log
    logging.info("Initiated at .")
    os.makedirs("data", exist_ok=True)

    live = OrderBook()
    connection = Connection(URL, PRODUCT_IDS, live) #could prompt user for id and pass it or just update in file
    recorder = Recorder(PRODUCT_IDS, live)
    server = Server(live)

    await recorder.connect()

    try:
        await asyncio.gather(server.run(), connection.connect(), recorder.run())
    except KeyboardInterrupt:
        pass
    finally:
        await recorder.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
