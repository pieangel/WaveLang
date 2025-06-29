import csv
from datetime import datetime
from .tick import Tick
from .wave_box import WaveBox

class WaveBuilder:
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.current_wave = None
        self.waves = []

    def process_tick(self, tick: Tick):
        if self.current_wave is None:
            self.current_wave = WaveBox(tick)
            return

        price_diff = tick.price - self.current_wave.start_tick.price

        if abs(price_diff) >= self.threshold:
            self.waves.append(self.current_wave)
            self.current_wave = WaveBox(tick)
        else:
            self.current_wave.update(tick)

    def finalize(self):
        if self.current_wave is not None:
            self.waves.append(self.current_wave)
            self.current_wave = None

    def build_from_csv(self, csv_path: str):
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                date_str, time_str, price_str, volume_str = row
                dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")
                price = float(price_str)
                volume = float(volume_str)
                tick = Tick(dt, price, volume)
                self.process_tick(tick)
        self.finalize()
        return self.waves
