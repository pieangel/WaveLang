# Updated version with volume tracking in WaveBox and WaveBuilder

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional
from datetime import datetime


class Direction(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class WaveBox:
    direction: Direction
    open: float
    high: float
    low: float
    close: float
    start_time: datetime
    end_time: Optional[datetime]
    tick_count: int
    volume: int  # total volume for the wave

    def update_price(self, price: float, volume: int, time: datetime):
        self.close = price
        self.high = max(self.high, price)
        self.low = min(self.low, price)
        self.end_time = time
        self.tick_count += 1
        self.volume += volume

    def duration_seconds(self) -> float:
        if self.end_time and self.start_time:
            return max((self.end_time - self.start_time).total_seconds(), 1.0)
        return 1.0

    def speed(self) -> float:
        return self.tick_count / self.duration_seconds()


class WaveBuilder:
    def __init__(self, box_size: float, reverse_count: int = 5):
        self.box_size = box_size
        self.reverse_size = box_size * reverse_count
        self.waves: List[WaveBox] = []
        self.current_wave: Optional[WaveBox] = None
        self.last_extreme_price: Optional[float] = None
        self.last_extreme_time: Optional[datetime] = None
        self.partial_volume: int = 0

    def add_price(self, price: float, volume: int, time: datetime):
        if self.current_wave is None:
            self.current_wave = WaveBox(Direction.NONE, price, price, price, price, time, time, 1, volume)
            return

        self.current_wave.update_price(price, volume, time)

        if self.current_wave.direction == Direction.NONE:
            price_range = self.current_wave.high - self.current_wave.low
            if price_range >= self.reverse_size:
                if self.current_wave.close > self.current_wave.open:
                    self.current_wave.direction = Direction.UP
                    self.last_extreme_price = self.current_wave.high
                    self.last_extreme_time = time
                    self.partial_volume = 0
                elif self.current_wave.close < self.current_wave.open:
                    self.current_wave.direction = Direction.DOWN
                    self.last_extreme_price = self.current_wave.low
                    self.last_extreme_time = time
                    self.partial_volume = 0
            return

        if self.current_wave.direction == Direction.UP:
            if price > self.current_wave.high:
                self.current_wave.high = price
                self.last_extreme_price = price
                self.last_extreme_time = time
                self.partial_volume = 0

            self.partial_volume += volume

            if price <= self.last_extreme_price - self.reverse_size:
                self.current_wave.close = self.last_extreme_price
                self.current_wave.end_time = self.last_extreme_time
                self.current_wave.volume -= self.partial_volume
                self.waves.append(self.current_wave)

                self.current_wave = WaveBox(
                    Direction.DOWN,
                    price,
                    price,
                    price,
                    price,
                    time,
                    time,
                    1,
                    self.partial_volume
                )
                self.partial_volume = 0
            return

        if self.current_wave.direction == Direction.DOWN:
            if price < self.current_wave.low:
                self.current_wave.low = price
                self.last_extreme_price = price
                self.last_extreme_time = time
                self.partial_volume = 0

            self.partial_volume += volume

            if price >= self.last_extreme_price + self.reverse_size:
                self.current_wave.close = self.last_extreme_price
                self.current_wave.end_time = self.last_extreme_time
                self.current_wave.volume -= self.partial_volume
                self.waves.append(self.current_wave)

                self.current_wave = WaveBox(
                    Direction.UP,
                    price,
                    price,
                    price,
                    price,
                    time,
                    time,
                    1,
                    self.partial_volume
                )
                self.partial_volume = 0
            return

    def finalize(self):
        if self.current_wave:
            self.waves.append(self.current_wave)
            self.current_wave = None

    def get_waves(self) -> List[WaveBox]:
        return self.waves


# Test and show result with volume
from ace_tools import display_dataframe_to_user
import pandas as pd

def test_wave_builder_with_volume():
    builder = WaveBuilder(box_size=2.5)
    sample_data = [
        (datetime(2024, 1, 1, 9, 0, 0), 100, 10),
        (datetime(2024, 1, 1, 9, 0, 1), 102, 15),
        (datetime(2024, 1, 1, 9, 0, 2), 104, 20),
        (datetime(2024, 1, 1, 9, 0, 3), 106, 25),
        (datetime(2024, 1, 1, 9, 0, 4), 100, 30),
        (datetime(2024, 1, 1, 9, 0, 5), 95, 40),
        (datetime(2024, 1, 1, 9, 0, 6), 97, 45),
        (datetime(2024, 1, 1, 9, 0, 7), 103, 50),
    ]
    for time, price, volume in sample_data:
        builder.add_price(price, volume, time)
    builder.finalize()

    waves = builder.get_waves()
    df = pd.DataFrame([{
        "Direction": wave.direction.name,
        "Open": wave.open,
        "High": wave.high,
        "Low": wave.low,
        "Close": wave.close,
        "Start": wave.start_time,
        "End": wave.end_time,
        "Ticks": wave.tick_count,
        "Volume": wave.volume,
        "Speed": round(wave.speed(), 2),
    } for wave in waves])
    display_dataframe_to_user("Wave Summary with Volume", df)

test_wave_builder_with_volume()
