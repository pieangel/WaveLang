import pandas as pd
import plotly.express as px
import random
import numpy as np

# 샘플 Wave 데이터 생성 (상승/하락 파동 포함)
random.seed(42)
n = 50
wave_data = pd.DataFrame({
    'size': [random.gauss(mu=10, sigma=3) if i % 2 == 0 else random.gauss(mu=-8, sigma=2) for i in range(n)],
    'duration': [random.randint(10, 100) for _ in range(n)],
    'direction': ['up' if i % 2 == 0 else 'down' for i in range(n)]
})

# Box Plot (크기 기준)
fig = px.box(
    wave_data,
    y='size',
    color='direction',
    title='Wave Size Distribution by Direction',
    labels={'size': 'Wave Size'}
)

fig.show()
