from .tick import Tick


class WaveBox:
    def __init__(self, start_tick: Tick):
        self.start_tick = start_tick
        self.end_tick = start_tick
        self.high = start_tick.price
        self.low = start_tick.price
        self.volume = start_tick.volume
        self.ticks = [start_tick]

    def update(self, tick: Tick):
        self.end_tick = tick
        self.high = max(self.high, tick.price)
        self.low = min(self.low, tick.price)
        self.volume += tick.volume
        self.ticks.append(tick)

    def __str__(self):
        return f"[{self.start_tick.time} ~ {self.end_tick.time}] Start: {self.start_tick.price}, End: {self.end_tick.price}, High: {self.high}, Low: {self.low}, Vol: {self.volume}"
