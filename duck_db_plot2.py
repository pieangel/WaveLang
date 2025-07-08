import duckdb
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wave.db import build_waves_from_month
from wave.core import Direction
import plotly.io as pio

# DuckDB 연결
conn = duckdb.connect("wave_data.duckdb")

# 파라미터 설정
symbol = "GC"
year = 2009
month = 10
box_size = 0.2
reverse_count = 3

# 한 달치 파동 생성
waves_by_day = build_waves_from_month(
    conn=conn,
    table_name="tick_GC",
    symbol=symbol,
    year=year,
    month=month,
    box_size=box_size,
    reverse_count=reverse_count
)

# 날짜 정렬
dates = sorted(waves_by_day.keys())

# 서브플롯 생성
fig = make_subplots(
    rows=len(dates),
    cols=1,
    shared_xaxes=False,
    vertical_spacing=0.005,  # ✅ 거의 붙게
    subplot_titles=[str(d) for d in dates]
)

# 각 날짜별 서브차트 추가
for i, date in enumerate(dates):
    waves = waves_by_day[date]
    if not waves:
        continue

    # Y축 범위 계산
    min_price = min(wave.low for wave in waves)
    max_price = max(wave.high for wave in waves)
    y_padding = (max_price - min_price) * 0.01  # 10% 여유

    for j, wave in enumerate(waves):
        color = 'red' if wave.direction == Direction.UP else 'blue'

        fig.add_trace(go.Scatter(
            x=[j, j],
            y=[wave.low, wave.high],
            mode='lines',
            line=dict(color='black', width=1),
            showlegend=False
        ), row=i+1, col=1)

        fig.add_trace(go.Scatter(
            x=[j, j],
            y=[wave.open, wave.close],
            mode='lines',
            line=dict(color=color, width=4),
            showlegend=False
        ), row=i+1, col=1)

    # 🟡 Y축 여유 공간 설정
    fig.update_layout(
        height=1000 * len(dates),  # 각 일에 대해 500픽셀씩 할당
        title=f"{year}년 {month}월 파동 시각화",
        showlegend=False
    )


fig.show()



fig.write_image("wave_2009_10.png", width=1200, height=3000)  # 크기는 필요에 따라 조절

