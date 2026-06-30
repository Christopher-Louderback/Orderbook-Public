from config import DEPTH_PERCENTAGE

class OrderBook: #probably can be better doing some sort of bst - note for transition out of python
    def __init__(self): #attributes belong to class
        self.bids = {}
        self.asks = {}
        self.best_bid = None #better to compute on demand or have variables?
        self.best_ask = None

    def get_best_bid(self):#could have both updates in one bigger updates bests function, inital thought dont like
        if self.bids:#fuck ternary
            self.best_bid = max(self.bids, key=float)
        else:
            self.best_bid = None

    def get_best_ask(self):
        if self.asks:
            self.best_ask = min(self.asks, key=float)
        else:
            self.best_ask = None

    def process_snapshot(self, data):
        self.bids = {} #need to clear out?
        self.asks = {}

        updates = data["events"][0]["updates"]

        for update in updates:
            price = update["price_level"]
            quantity = update["new_quantity"]
            side = update["side"]

            if side == "bid":
                self.bids[price] = quantity
            elif side == "offer":
                self.asks[price] = quantity

        self.get_best_bid()
        self.get_best_ask()

    def process_update(self, data):
        updates = data["events"][0]["updates"]

        for update in updates:
            price = update["price_level"]
            quantity = update["new_quantity"]
            side = update["side"]

            if side == "bid":
                if quantity == "0":
                    if price in self.bids:
                        del self.bids[price]
                else:
                    self.bids[price] = quantity
                self.get_best_bid()

            elif side == "offer":
                if quantity == "0":
                    if price in self.asks:
                        del self.asks[price]
                else:
                    self.asks[price] = quantity
                self.get_best_ask()

    def charting_data(self):
        if not self.best_bid or not self.best_ask:
            return {"bids": {}, "asks": {}}
        
        mid = (float(self.best_bid) + float(self.best_ask)) / 2
        lower = mid * (1 - DEPTH_PERCENTAGE)
        upper = mid * (1 + DEPTH_PERCENTAGE)
        
        bids = {}
        for p, q in self.bids.items():
            if float(p) >= lower:
                bids[float(p)] = float(q) #update ps nb qs
        
        asks = {}
        for p, q in self.asks.items():
            if float(p) <= upper:
                asks[float(p)] = float(q)
        
        return {
            "bids": bids,
            "asks": asks,
            "mid": mid,
            "best_bid": float(self.best_bid),
            "best_ask": float(self.best_ask)
        }