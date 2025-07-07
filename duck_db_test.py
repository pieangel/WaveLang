import duckdb
import pandas as pd

# DuckDB 연결
conn = duckdb.connect("D:/project/WaveLang/tickdata.duckdb")  # DB 파일 경로

# 날짜 구간 설정 (예: 2022년 1월 10일부터 2022년 1월 12일)
start_date = "2022-01-10"
end_date = "2022-01-12"

# 쿼리 실행 (timestamp 컬럼이 DATETIME 타입이라고 가정)
query = f"""
    SELECT * FROM tick_NQ
    WHERE DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY timestamp
"""

# Pandas DataFrame으로 가져오기
df = conn.execute(query).df()

# 결과 확인
print(df.head())
print(f"Total rows: {len(df)}")
