import duckdb

conn = duckdb.connect("wave_data.duckdb")
conn.execute("CREATE TABLE test (id INT, value DOUBLE);")
conn.execute("INSERT INTO test VALUES (1, 100.0), (2, 200.0);")
print(conn.execute("SELECT * FROM test").fetchall())
