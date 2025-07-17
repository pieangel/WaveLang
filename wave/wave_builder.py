from datetime import datetime
from typing import List, Optional
from .direction import Direction
from .wave_box import WaveBox

class WaveBuilder:
    def __init__(self, box_size: float, reverse_count: int = 5):
        self.box_size = box_size
        self.reverse_size = box_size * reverse_count
        self.waves: List[WaveBox] = []
        self.current_wave: Optional[WaveBox] = None

    def add_price(self, price: float, time: datetime):
        if self.current_wave is None:
            self.current_wave = WaveBox(Direction.NONE, price, price, price, price, time)
            return

        if self.current_wave.direction == Direction.NONE:
            self.current_wave.high = max(self.current_wave.high, price)
            self.current_wave.low = min(self.current_wave.low, price)
            self.current_wave.close = price

            if self.current_wave.high - self.current_wave.low >= self.reverse_size:
                if self.current_wave.close > self.current_wave.open:
                    self.current_wave.direction = Direction.UP
                elif self.current_wave.close < self.current_wave.open:
                    self.current_wave.direction = Direction.DOWN
            return

        if self.current_wave.direction == Direction.UP:
            if price > self.current_wave.high:
                self.current_wave.high = price
            if price <= self.current_wave.high - self.reverse_size:
                self.current_wave.close = self.current_wave.high
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(Direction.DOWN, self.current_wave.high, self.current_wave.high, price, price, time)
            return

        if self.current_wave.direction == Direction.DOWN:
            if price < self.current_wave.low:
                self.current_wave.low = price
            if price >= self.current_wave.low + self.reverse_size:
                self.current_wave.close = self.current_wave.low
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(Direction.UP, self.current_wave.low, price, self.current_wave.low, price, time)
            return

    def finalize(self):
        if self.current_wave:
            self.waves.append(self.current_wave)
            self.current_wave = None

    def get_waves(self) -> List[WaveBox]:
        return self.waves
