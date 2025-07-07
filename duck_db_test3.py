import duckdb

conn = duckdb.connect("D:/project/WaveLang/tickdata.duckdb")

# 테이블 삭제 후 재생성
conn.execute("DROP TABLE IF EXISTS tick_NQ")
conn.execute("""
    CREATE TABLE tick_NQ AS 
    SELECT * FROM read_csv_auto('D:/project/WaveLang/data/NQ_TickData/NQ_2009_09.csv')
""")

# 데이터 확인
print("== row 수 ==")
print(conn.execute("SELECT COUNT(*) FROM tick_NQ").fetchall())


df = conn.execute("SELECT * FROM tick_NQ LIMIT 5").df()
print(df)


conn.close()
