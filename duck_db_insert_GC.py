import os
import duckdb

# DuckDB 연결
conn = duckdb.connect("D:/project/WaveLang/wave_data.duckdb")

# ✅ 1. 테이블 초기화
conn.execute("DROP TABLE IF EXISTS tick_GC")
conn.execute("""
    CREATE TABLE tick_GC (
        timestamp TIMESTAMP,
        price DOUBLE,
        volume BIGINT,
        symbol TEXT
    )
""")

# ✅ 2. CSV 데이터 삽입
base_path = "D:/project/WaveLang/data/GC_TickData"
files = sorted(f for f in os.listdir(base_path) if f.endswith('.csv'))

for fname in files:
    full_path = os.path.join(base_path, fname).replace('\\', '/')
    symbol = fname.split('_')[0]  # 예: "NQ_2025_05.csv" → "NQ"

    print(f"📥 Inserting: {fname} (symbol: {symbol})")

    try:
        conn.execute(f"""
            INSERT INTO tick_GC
            SELECT 
                strptime(column0 || ' ' || column1, '%m/%d/%Y %H:%M:%S') AS timestamp,
                column2::DOUBLE AS price,
                column3::BIGINT AS volume,
                '{symbol}' AS symbol
            FROM read_csv_auto('{full_path}', header=False,
                types={{
                    'column0': 'VARCHAR',
                    'column1': 'VARCHAR',
                    'column2': 'VARCHAR',
                    'column3': 'VARCHAR'
                }}
            )
        """)
    except Exception as e:
        print(f"❌ 오류 발생: {fname} | {e}")
