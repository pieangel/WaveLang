import duckdb
import os

# 기존 파일 백업
if os.path.exists("wave_data.duckdb"):
    os.rename("wave_data.duckdb", "wave_data_broken.duckdb")

# 새로 생성
conn = duckdb.connect("wave_data.duckdb")
conn.execute("CREATE TABLE test (x INT);")
conn.execute("INSERT INTO test VALUES (1), (2);")
print(conn.execute("SELECT * FROM test").fetchall())
