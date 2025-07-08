import duckdb
conn = duckdb.connect("wave_data.duckdb")
print(conn.execute("PRAGMA show_tables;").fetchall())
