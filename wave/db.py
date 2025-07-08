import duckdb
import json
from datetime import datetime
from typing import Dict
from .core import WaveBuilder, WaveBox

def save_wave_data(conn, symbol: str, wave_size: float, waves: list[WaveBox]):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS waves (
        symbol TEXT,
        wave_size DOUBLE,
        reverse_count INTEGER,
        date DATE,
        waves TEXT
    )
    """)
    for wave in waves:
        data = {
            "direction": wave.direction.name,
            "open": wave.open,
            "high": wave.high,
            "low": wave.low,
            "close": wave.close,
            "timestamp": wave.timestamp.isoformat()
        }
        conn.execute("""
        INSERT INTO waves VALUES (?, ?, ?, ?, ?)
        """, (
            symbol,
            wave_size,
            5,
            wave.timestamp.date(),
            json.dumps([data])
        ))
def build_waves_from_month(
    conn: duckdb.DuckDBPyConnection,
    table_name: str,
    symbol: str,
    year: int,
    month: int,
    box_size: float,
    reverse_count: int
) -> Dict[datetime.date, list[WaveBox]]:
    """
    DuckDB에서 특정 월의 Tick 데이터를 불러와 파동을 생성합니다.
    날짜별로 WaveBox 리스트를 반환합니다.
    """
    start = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end = f"{year+1:04d}-01-01"
    else:
        end = f"{year:04d}-{month+1:02d}-01"

    query = f"""
    SELECT timestamp, price
    FROM {table_name}
    WHERE symbol = '{symbol}'
      AND timestamp >= '{start}' AND timestamp < '{end}'
    ORDER BY timestamp
    """
    df = conn.execute(query).df()

    if df.empty:
        return {}

    # 날짜별로 파동 생성
    waves_by_day = {}
    df['date'] = df['timestamp'].dt.date
    for date, group in df.groupby('date'):
        builder = WaveBuilder(box_size=box_size, reverse_count=reverse_count)
        for _, row in group.iterrows():
            builder.add_price(row['price'], row['timestamp'])
        builder.finalize()
        waves_by_day[date] = builder.get_waves()

    return waves_by_day
