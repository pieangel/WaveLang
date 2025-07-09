import duckdb
import pandas as pd
import plotly.graph_objects as go


class OhlcvBuilder2:
    def __init__(self, db_path, table_name='tick_NQ', ticks_per_bar=300):
        self.db_path = db_path
        self.table_name = table_name
        self.ticks_per_bar = ticks_per_bar
        self.conn = duckdb.connect(database=db_path, read_only=True)
        self.tick_df = None
        self.ohlcv_df = None

    def load_month_data(self, year: int, month: int):
        query = f"""
        SELECT *, 
               strptime(date || ' ' || time, '%Y-%m-%d %H:%M:%S') AS datetime
        FROM {self.table_name}
        WHERE extract('year' FROM strptime(date, '%Y-%m-%d')) = {year}
          AND extract('month' FROM strptime(date, '%Y-%m-%d')) = {month}
        ORDER BY datetime
        """
        df = self.conn.execute(query).fetch_df()

        if df.empty:
            raise ValueError(f"No data found for {year}-{month:02d}.")

        df['date'] = pd.to_datetime(df['datetime']).dt.date
        self.tick_df = df[['datetime', 'date', 'price', 'volume']]

    def build_ohlcv(self):
        if self.tick_df is None:
            raise ValueError("Tick data is not loaded.")

        ohlcv_list = []

        for date, group in self.tick_df.groupby('date'):
            group = group.reset_index(drop=True)
            bars = [group.iloc[i:i + self.ticks_per_bar] for i in range(0, len(group), self.ticks_per_bar)]

            for bar in bars:
                if bar.empty:
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

    def plot(self):
        if self.ohlcv_df is None:
            raise ValueError("No OHLCV data to plot.")

        df = self.ohlcv_df.copy()
        df['x_label'] = df['datetime'].dt.strftime('%m-%d %H:%M')

        fig = go.Figure(data=[go.Candlestick(
            x=df['x_label'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='OHLCV',
            hovertext=df['datetime'].astype(str),
            hoverinfo='text'
        )])

        fig.update_layout(
            title="OHLCV Chart from DuckDB",
            xaxis_title="Time",
            yaxis_title="Price",
            xaxis_type='category',
            xaxis_tickangle=-45
        )

        fig.show()
