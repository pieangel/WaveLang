from dataclasses import dataclass
from datetime import datetime
from .direction import Direction

@dataclass
class WaveBox:
    direction: Direction
    open: float
    high: float
    low: float
    close: float
    timestamp: datetime

    def update(self, price: float):
        self.close = price
        if self.direction == Direction.UP and price > self.high:
            self.high = price
        elif self.direction == Direction.DOWN and price < self.low:
            self.low = price
