import os
import duckdb

# DuckDB 연결
conn = duckdb.connect("D:/project/WaveLang/wave_data.duckdb")

# 테이블 초기화
conn.execute("DROP TABLE IF EXISTS tick_NQ")
conn.execute("CREATE TABLE tick_NQ (timestamp TIMESTAMP, price DOUBLE, volume BIGINT)")

# 데이터 경로
base_path = "D:/project/WaveLang/data/NQ_TickData"
files = sorted(f for f in os.listdir(base_path) if f.endswith('.csv'))

for fname in files:
    full_path = os.path.join(base_path, fname).replace('\\', '/')
    print(f"Inserting: {fname}")

    try:
        conn.execute(f"""
            INSERT INTO tick_NQ
            SELECT 
                strptime(column0 || ' ' || column1, '%m/%d/%Y %H:%M:%S') AS timestamp,
                column2::DOUBLE AS price,
                column3::BIGINT AS volume
            FROM read_csv_auto('{full_path}', header=False,
                    types={{'column0': 'VARCHAR', 'column1': 'VARCHAR', 'column2': 'VARCHAR', 'column3': 'VARCHAR'}}
                )
        """)
    except Exception as e:
        print(f"❌ 오류 발생: {fname}")
