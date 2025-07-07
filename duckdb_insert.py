import duckdb
import os
import glob

conn = duckdb.connect("tickdata.duckdb")

conn.execute("DROP TABLE IF EXISTS tick_NQ")


# 테이블 생성 (1회만)
conn.execute("""
    CREATE TABLE IF NOT EXISTS tick_NQ (
        timestamp TIMESTAMP,
        price DOUBLE,
        volume BIGINT
    )
""")

# 데이터 디렉토리 설정
data_dir = "data/NQ_TickData"
file_list = sorted(glob.glob(os.path.join(data_dir, "NQ_*.csv")))

for path in file_list:
    print(f"📥 Loading {os.path.basename(path)}...")
    conn.execute(f"""
            COPY (
                SELECT 
                    strptime(column0 || ' ' || column1, '%m/%d/%Y %H:%M:%S') AS timestamp,
                    CAST(column2 AS DOUBLE) AS price,
                    CAST(column3 AS BIGINT) AS volume
                FROM read_csv_auto('{path}', header=False,
                    types={{'column0': 'VARCHAR', 'column1': 'VARCHAR', 'column2': 'VARCHAR', 'column3': 'VARCHAR'}}
                )
            ) TO tick_NQ;
        """)

