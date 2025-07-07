import duckdb
import pandas as pd

# === 설정 ===
DB_PATH = "D:/project/WaveLang/wave_data.duckdb"
TARGET_DATE = "2020-02-27"  # ← 여기서 원하는 날짜로 변경하세요 (YYYY-MM-DD)

# === DuckDB 연결 ===
conn = duckdb.connect(DB_PATH)

# === 쿼리 실행 ===
query = f"""
    SELECT timestamp, price, volume
    FROM tick_NQ
    WHERE DATE(timestamp) = '{TARGET_DATE}'
    ORDER BY timestamp
"""

df = conn.execute(query).df()

# === 결과 출력 ===
print(f"✅ {TARGET_DATE} 데이터 추출 완료!")
print(f"총 row 수: {len(df):,}")
print(df.head())

# === (선택) 저장하기 ===
OUTPUT_PATH = f"D:/project/WaveLang/extracted/NQ_{TARGET_DATE.replace('-', '_')}.csv"
df.to_csv(OUTPUT_PATH, index=False)
print(f"💾 저장 완료: {OUTPUT_PATH}")

conn.close()
