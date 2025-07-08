import csv
from datetime import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

    def plot_waves(self, title: str = "WaveBox Chart"):
        if not self.waves:
            print("No waves to display.")
            return

        fig = go.Figure()

        x_values = list(range(len(self.waves)))  # 0, 1, 2, ...
        x_labels = [wave.start_tick.time.strftime('%Y-%m-%d %H:%M:%S') for wave in self.waves]

        for i, wave in enumerate(self.waves):
            color = 'red' if wave.end_tick.price >= wave.start_tick.price else 'blue'

            fig.add_trace(go.Candlestick(
                x=[x_values[i]],
                open=[wave.start_tick.price],
                close=[wave.end_tick.price],
                high=[wave.high],
                low=[wave.low],
                increasing_line_color='red',
                decreasing_line_color='blue',
                showlegend=False
            ))

        fig.update_layout(
            title=title,
            xaxis_title='Wave Start Time',
            yaxis_title='Price',
            xaxis=dict(
                tickmode='array',
                tickvals=x_values,
                ticktext=x_labels,
                tickangle=45,
                type='category'  # ✅ 시간 간격을 무시하고 붙여서 출력
            ),
            margin=dict(l=40, r=40, t=40, b=80),
            height=600
        )

        fig.show()

