import pandas as pd
import os
import plotly.graph_objects as go


class OhlcvBuilder:
    def __init__(self, ticks_per_bar=300):
        self.ticks_per_bar = ticks_per_bar
        self.tick_df = None
        self.ohlcv_df = None

    def load_tick_data(self, file_path):
        # 절대 경로 확인
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Tick data file not found: {abs_path}")

        df = pd.read_csv(abs_path, header=None, names=['date', 'time', 'price', 'volume'])
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        df['date'] = df['datetime'].dt.date
        df = df[['datetime', 'date', 'price', 'volume']]
        self.tick_df = df

    def build_ohlcv(self):
        if self.tick_df is None:
            raise ValueError("Tick data is not loaded.")

        ohlcv_list = []

        for date, group in self.tick_df.groupby('date'):
            group = group.reset_index(drop=True)
            bars = [group.iloc[i:i + self.ticks_per_bar] for i in range(0, len(group), self.ticks_per_bar)]

            for bar in bars:
                if len(bar) == 0:
                    continue
                ohlcv = {
                    'datetime': bar['datetime'].iloc[-1],
                    'open': bar['price'].iloc[0],
                    'high': bar['price'].max(),
                    'low': bar['price'].min(),
                    'close': bar['price'].iloc[-1],
                    'volume': bar['volume'].sum(),
                    'date': bar['datetime'].iloc[-1].date()
                }
                ohlcv_list.append(ohlcv)

        self.ohlcv_df = pd.DataFrame(ohlcv_list)

    def get_ohlcv_df(self):
        if self.ohlcv_df is None:
            raise ValueError("OHLCV data is not built yet.")
        return self.ohlcv_df

    def save_ohlcv(self, output_path):
        if self.ohlcv_df is None:
            raise ValueError("No OHLCV data to save.")
        abs_path = os.path.abspath(output_path)
        self.ohlcv_df.to_csv(abs_path, index=False)
        print(f"Saved OHLCV to: {abs_path}")

    def plot(self):
        if self.ohlcv_df is None:
            raise ValueError("No OHLCV data to plot.")

        df = self.ohlcv_df.copy()

        # 봉 개수만큼 순서 부여 + 시간 문자열 포맷
        df['x_label'] = df['datetime'].dt.strftime('%m-%d %H:%M')

        fig = go.Figure(data=[go.Candlestick(
            x=df['x_label'],  # ← 시간 문자열을 카테고리로 사용
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='OHLCV',
            hovertext=df['datetime'].astype(str),
            hoverinfo='text'
        )])

        fig.update_layout(
            title="OHLCV Chart (Compact + Time Labels)",
            xaxis_title="Time",
            yaxis_title="Price",
            xaxis_type='category',  # category 유지
            xaxis_tickangle=-45  # 보기 좋게 기울이기
        )

        fig.show()



