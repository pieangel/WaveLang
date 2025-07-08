import duckdb

# DuckDB 파일에 연결
conn = duckdb.connect("wave_data.duckdb")

# symbol 컬럼 추가 및 값 설정
conn.execute("ALTER TABLE tick_NQ ADD COLUMN symbol TEXT;")
conn.execute("UPDATE tick_NQ SET symbol = 'NQ';")

# 결과 확인 (선택)
rows = conn.execute("SELECT symbol, COUNT(*) FROM tick_NQ GROUP BY symbol").fetchall()
print(rows)
