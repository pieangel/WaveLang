import duckdb

db_path = "D:/project/WaveLang/tickdata.duckdb"
conn = duckdb.connect(db_path)

# 테이블 존재 확인
print("== 테이블 목록 ==")
print(conn.execute("SHOW TABLES").fetchall())

# row 개수 확인
print("== row 수 ==")
print(conn.execute("SELECT COUNT(*) FROM tick_NQ").fetchall())

# 샘플 출력
print("== 샘플 데이터 ==")
df = conn.execute("SELECT * FROM tick_NQ LIMIT 5").df()
print(df)
