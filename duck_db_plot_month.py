import duckdb
import plotly.graph_objects as go
from wave.db import build_waves_from_month
from wave.core import Direction
import plotly.io as pio

# DuckDB 연결
conn = duckdb.connect("wave_data.duckdb")

# 파라미터 설정
symbol = "CL"
year = 2009
month = 11
box_size = 0.05
reverse_count = 5

# 한 달치 파동 생성
waves_by_day = build_waves_from_month(
    conn=conn,
    table_name="tick_CL",
    symbol=symbol,
    year=year,
    month=month,
    box_size=box_size,
    reverse_count=reverse_count
)

# 날짜 정렬
dates = sorted(waves_by_day.keys())

# 전체 파동 리스트 생성
all_waves = []
for date in dates:
    all_waves.extend(waves_by_day[date])

# 전체 파동 시각화
fig = go.Figure()

min_price = min(wave.low for wave in all_waves)
max_price = max(wave.high for wave in all_waves)
y_padding = (max_price - min_price) * 0.1

# 파동 시퀀스별로 그림
for i, wave in enumerate(all_waves):
    color = 'red' if wave.direction == Direction.UP else 'blue'

    # 전체 파동 막대
    fig.add_trace(go.Scatter(
        x=[i, i],
        y=[wave.low, wave.high],
        mode='lines',
        line=dict(color='black', width=1),
        showlegend=False
    ))

    # 시가-종가 굵은 막대
    fig.add_trace(go.Scatter(
        x=[i, i],
        y=[wave.open, wave.close],
        mode='lines',
        line=dict(color=color, width=4),
        showlegend=False
    ))

# 레이아웃 설정
fig.update_layout(
    title=f"{year}년 {month}월 전체 파동 시각화",
    xaxis_title="Wave Index",
    yaxis_title="Price",
    yaxis=dict(range=[min_price - y_padding, max_price + y_padding]),
    height=800,
)

# 시각화
fig.show()

# 이미지 저장
fig.write_image(f"wave_{year}_{month:02d}.png", width=1200, height=800)
