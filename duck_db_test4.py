import duckdb

conn = duckdb.connect("D:/project/WaveLang/tickdata.duckdb")


# 데이터 확인
print("== row 수 ==")
print(conn.execute("SELECT COUNT(*) FROM tick_NQ").fetchall())


df = conn.execute("SELECT * FROM tick_NQ LIMIT 5").df()
print(df)


conn.close()
