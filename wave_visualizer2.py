import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple
from datetime import datetime
import csv


# --- 파동 관련 정의 ---

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
    timestamp: datetime  # 시가 기준 시간

    def update(self, price: float):
        self.close = price
        if self.direction == Direction.UP and price > self.high:
            self.high = price
        elif self.direction == Direction.DOWN and price < self.low:
            self.low = price


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
                self.current_wave = WaveBox(
                    direction=Direction.DOWN,
                    open=self.current_wave.high,
                    high=self.current_wave.high,
                    low=price,
                    close=price,
                    timestamp=time
                )
            return

        if self.current_wave.direction == Direction.DOWN:
            if price < self.current_wave.low:
                self.current_wave.low = price


            if price >= self.current_wave.low + self.reverse_size:
                self.current_wave.close = self.current_wave.low
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(
                    direction=Direction.UP,
                    open=self.current_wave.low,
                    high=price,
                    low=self.current_wave.low,
                    close=price,
                    timestamp=time
                )
            return

    def finalize(self):
        if self.current_wave:
            self.waves.append(self.current_wave)
            self.current_wave = None

    def get_waves(self) -> List[WaveBox]:
        return self.waves


# --- 시각화 ---

def plot_waves(waves: List[WaveBox]):
    fig, ax = plt.subplots(figsize=(14, 6))

    times = [wave.timestamp.strftime('%m-%d\n%H:%M') for wave in waves]
    x = list(range(len(waves)))

    for i, wave in enumerate(waves):
        color = 'red' if wave.direction == Direction.UP else 'blue'
        ax.plot([x[i], x[i]], [wave.low, wave.high], color='black', linewidth=1)
        ax.plot([x[i], x[i]], [wave.open, wave.close], color=color, linewidth=4)

    ax.set_title('Wave Chart (Equal Interval with Time Labels)')
    ax.set_xlabel('Wave Index / Time')
    ax.set_ylabel('Price')
    ax.set_xticks(x)
    ax.set_xticklabels(times, rotation=90, fontsize=8)
    ax.grid(True)
    plt.tight_layout()
    plt.show()


# --- CSV 로더 ---

def load_prices_with_time(file_path: str) -> List[Tuple[datetime, float]]:
    result = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            try:
                timestamp = datetime.strptime(f"{row[0]} {row[1]}", "%m/%d/%Y %H:%M:%S")
                price = float(row[2])
                result.append((timestamp, price))
            except ValueError:
                continue
    return result


# --- 메인 실행 ---

if __name__ == "__main__":
    file_path = 'data/NQ_TickData/NQ_2025_05.csv'

    print("🔄 데이터를 불러오는 중...")
    data = load_prices_with_time(file_path)

    print(f"✅ {len(data):,}개의 틱 데이터를 불러왔습니다.")

    builder = WaveBuilder(box_size=5.0, reverse_count=5)

    for timestamp, price in data:
        builder.add_price(price, timestamp)

    builder.finalize()
    waves = builder.get_waves()

    print(f"📈 총 {len(waves)}개의 파동이 생성되었습니다.")
    for i, wave in enumerate(waves[:10]):
        print(f"{i+1}: {wave.direction.name} {wave.timestamp} O:{wave.open} H:{wave.high} L:{wave.low} C:{wave.close}")

    plot_waves(waves)
