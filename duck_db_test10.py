import duckdb

conn = duckdb.connect("wave_data_broken.duckdb")
print(conn.execute("PRAGMA show_tables").fetchall())
print(conn.execute("SELECT COUNT(*) FROM tick_NQ").fetchone())
print(conn.execute("SELECT * FROM tick_NQ LIMIT 5").fetchall())
