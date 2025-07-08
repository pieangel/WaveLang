import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import duckdb
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wave.db import build_waves_from_month
from wave.core import WaveBox, Direction

# Dash 앱 초기화
app = dash.Dash(__name__)

# UI 레이아웃 구성
app.layout = html.Div([
    html.H1("📊 월별 파동 대시보드"),
    html.Div([
        html.Label("연도 선택"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(y), 'value': y} for y in range(2009, 2026)],
            value=2009
        ),
        html.Label("월 선택"),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': f"{m:02d}", 'value': m} for m in range(1, 13)],
            value=9
        ),
    ], style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'top'}),

    dcc.Loading(
        id="loading-graph",
        children=[dcc.Graph(id='wave-graph')],
        type="default"
    )
])

# DuckDB 연결
conn = duckdb.connect("wave_data_broken.duckdb")
conn.execute("PRAGMA show_tables").fetchall()
#conn.close()

# 콜백: 연도/월 선택 시 파동 차트 갱신
@app.callback(
    Output('wave-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_wave_chart(year, month):
    waves_by_day = build_waves_from_month(
        conn=conn,
        table_name="tick_NQ",
        symbol="NQ",
        year=year,
        month=month,
        box_size=0.25,
        reverse_count=5
    )

    if not waves_by_day:
        fig = go.Figure()
        fig.update_layout(title="❌ 데이터 없음")
        return fig

    dates = sorted(waves_by_day.keys())
    fig = make_subplots(
        rows=len(dates), cols=1,
        shared_xaxes=False,
        vertical_spacing=0.03,
        subplot_titles=[str(d) for d in dates]
    )

    for i, date in enumerate(dates):
        waves = waves_by_day[date]
        x = list(range(len(waves)))
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

    fig.update_layout(height=250*len(dates), title=f"{year}년 {month}월 파동 시각화", showlegend=False)
    return fig

# 실행
if __name__ == '__main__':
    app.run(debug=True)

