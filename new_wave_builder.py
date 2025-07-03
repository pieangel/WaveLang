import csv
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- Tick 클래스 ---
class Tick:
    def __init__(self, time: datetime, price: float, volume: float):
        self.time = time
        self.price = price
        self.volume = volume


# --- WaveBox 클래스 ---
class WaveBox:
    def __init__(self, direction: str, start_tick: Tick):
        self.direction = direction  # 'up' or 'down'
        self.start_tick = start_tick
        self.end_tick = start_tick
        self.high = start_tick.price
        self.low = start_tick.price
        self.volume = start_tick.volume
        self.ticks = [start_tick]

    def update(self, tick: Tick):
        self.end_tick = tick
        self.ticks.append(tick)
        self.high = max(self.high, tick.price)
        self.low = min(self.low, tick.price)
        self.volume += tick.volume


# --- WaveBuilder 클래스 ---
class WaveBuilder:
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.current_wave = None
        self.waves = []

    def process_tick(self, tick: Tick):
        if self.current_wave is None:
            self.current_wave = WaveBox(direction='up', start_tick=tick)
            return

        price = tick.price
        start_price = self.current_wave.start_tick.price
        direction = self.current_wave.direction

        if direction == 'up':
            if price >= self.current_wave.high:
                self.current_wave.update(tick)
            elif price <= start_price - self.threshold:
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(direction='down', start_tick=tick)
        elif direction == 'down':
            if price <= self.current_wave.low:
                self.current_wave.update(tick)
            elif price >= start_price + self.threshold:
                self.waves.append(self.current_wave)
                self.current_wave = WaveBox(direction='up', start_tick=tick)

    def finalize(self):
        if self.current_wave:
            self.waves.append(self.current_wave)

    def build_from_csv(self, filepath: str):
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    date_str, time_str, price_str, volume_str = row
                    time = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")
                    price = float(price_str)
                    volume = float(volume_str)
                    tick = Tick(time, price, volume)
                    self.process_tick(tick)
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
        self.finalize()

    def plot_waves(self, title="Wave Chart"):
        fig, ax = plt.subplots()
        for idx, wave in enumerate(self.waves):
            x = [idx, idx]
            y = [wave.start_tick.price, wave.end_tick.price]
            color = 'red' if wave.direction == 'up' else 'blue'
            ax.plot(x, y, color=color, linewidth=2)
            ax.scatter(idx, wave.start_tick.price, color='gray', marker='o')

        ax.set_title(title)
        ax.set_xlabel('Wave Index')
        ax.set_ylabel('Price')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_waves_plotly(self, title="Wave Chart"):
        x_labels = []
        y_start = []
        y_end = []
        colors = []

        for wave in self.waves:
            label = wave.start_tick.time.strftime("%m-%d %H:%M")
            x_labels.append(label)
            y_start.append(wave.start_tick.price)
            y_end.append(wave.end_tick.price)
            colors.append("red" if wave.direction == "up" else "blue")

        fig = go.Figure()

        for i in range(len(self.waves)):
            fig.add_trace(go.Scatter(
                x=[x_labels[i], x_labels[i]],
                y=[y_start[i], y_end[i]],
                mode="lines+markers",
                marker=dict(color=colors[i]),
                line=dict(color=colors[i], width=2),
                name=f"Wave {i + 1}"
            ))

        fig.update_layout(
            title=title,
            xaxis_title="Wave Start Time",
            yaxis_title="Price",
            showlegend=False,
            xaxis=dict(tickangle=45),
            height=500
        )

        fig.show()


if __name__ == "__main__":
    builder = WaveBuilder(threshold=2.5)
    builder.build_from_csv("data/NQ_TickData/NQ_2009_09.csv")
    builder.plot_waves_plotly("Wave Chart: 2009-09-27")