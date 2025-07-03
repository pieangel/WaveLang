import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional
import csv


# --- 파동 관련 클래스 ---

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

    def add_price(self, price: float):
        if self.current_wave is None:
            self.current_wave = WaveBox(Direction.NONE, price, price, price, price)
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
            self.current_wave.close = price

            if price <= self.current_wave.high - self.reverse_size:
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(
                    direction=Direction.DOWN,
                    open=self.waves[-1].high,
                    high=self.waves[-1].high,
                    low=price,
                    close=price
                )
            return

        if self.current_wave.direction == Direction.DOWN:
            if price < self.current_wave.low:
                self.current_wave.low = price
            self.current_wave.close = price

            if price >= self.current_wave.low + self.reverse_size:
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(
                    direction=Direction.UP,
                    open=self.waves[-1].low,
                    high=price,
                    low=self.waves[-1].low,
                    close=price
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

    for i, wave in enumerate(waves):
        color = 'red' if wave.direction == Direction.UP else 'blue'
        ax.plot([i, i], [wave.open, wave.close], color=color, linewidth=4)
        ax.plot([i, i], [wave.low, wave.high], color='black', linewidth=1)

    ax.set_title('Wave Chart from Tick Data')
    ax.set_xlabel('Wave Index')
    ax.set_ylabel('Price')
    ax.grid(True)
    plt.tight_layout()
    plt.show()


# --- CSV 파일 로딩 ---

def load_prices_from_csv(file_path: str) -> List[float]:
    prices = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue  # 데이터 부족시 스킵
            try:
                price = float(row[2])
                prices.append(price)
            except ValueError:
                continue  # 첫 줄 등 문자열인 경우 무시
    return prices


# --- 메인 실행 ---

if __name__ == "__main__":
    file_path = 'data/NQ_TickData/NQ_2010_01.csv'
    prices = load_prices_from_csv(file_path)

    # 파동 생성
    builder = WaveBuilder(box_size=2.5, reverse_count=3)  # 박스 크기와 반전 개수 조정 가능
    for price in prices:
        builder.add_price(price)

    builder.finalize()
    waves = builder.get_waves()

    print(f"총 {len(waves)}개의 파동이 생성되었습니다.")
    for i, wave in enumerate(waves[:10]):
        print(f"Wave {i+1}: {wave.direction.name} - O:{wave.open} H:{wave.high} L:{wave.low} C:{wave.close}")

    plot_waves(waves)
