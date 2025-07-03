import csv
from datetime import datetime
from wave.wave_builder import WaveBuilder
import plotly.graph_objs as go

builder = WaveBuilder(threshold=2.5)
builder.build_from_csv("data/NQ_TickData/NQ_2009_09.csv")

# 기존 개별 파동 출력
builder.plot_waves("Original Waves")

# 새로운 병합된 파동 출력
merged = builder.merge_directional_waves()

# 시각화
def plot_merged_waves(waves, title="Merged Directional Waves"):
    fig = go.Figure()
    x_values = list(range(len(waves)))
    x_labels = [wave.start_tick.time.strftime('%Y-%m-%d %H:%M:%S') for wave in waves]

    for i, wave in enumerate(waves):
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
        xaxis_title='Merged Wave Start Time',
        yaxis_title='Price',
        xaxis=dict(
            tickmode='array',
            tickvals=x_values,
            ticktext=x_labels,
            tickangle=45,
            type='category'
        ),
        margin=dict(l=40, r=40, t=40, b=80),
        height=600
    )

    fig.show()

# 출력
plot_merged_waves(merged)
