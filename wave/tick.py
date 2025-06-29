from datetime import datetime

class Tick:
    def __init__(self, time: datetime, price: float, volume: float):
        self.time = time
        self.price = price
        self.volume = volume
