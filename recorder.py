import asyncio
import json
import logging
import aiosqlite
from datetime import datetime, timezone #avoid double datetimes

class Recorder:
    def __init__(self, product_ids, order_book):
        self.product_ids = product_ids[0]
        self.order_book = order_book
        self.conn = None

    async def connect(self):
        logging.info("Attempting to connect to database.")
        self.conn = await aiosqlite.connect("data/order_book.db")
        await self.create_table()
        logging.info("Connected to database.")
    
    async def disconnect(self):
        logging.info("Attempting to close database connection.")
        if self.conn:
            await self.conn.close()
        logging.info("Database connection closed.")

    async def create_table(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                timestamp DATETIME,
                mid_price REAL,
                spread REAL,
                bids TEXT,
                asks TEXT
            )
        """)
        await self.conn.commit()

    async def write(self):
        if self.order_book.best_bid:
            best_bid = float(self.order_book.best_bid)
        else:
            best_bid = None

        if self.order_book.best_ask:
            best_ask = float(self.order_book.best_ask)
        else:
            best_ask = None

        if best_bid and best_ask:
            midprice = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
        else:
            midprice = None
            spread = None

        await self.conn.execute("""
            INSERT INTO snapshots 
            (product_id, timestamp, mid_price, spread, bids, asks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.product_ids,
            datetime.now(timezone.utc).isoformat(),
            midprice,
            spread,
            json.dumps(self.order_book.bids),
            json.dumps(self.order_book.asks)
        ))
        await self.conn.commit()

    async def run(self):
        while True:
            await self.write()
            await asyncio.sleep(1)