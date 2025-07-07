import duckdb

# DB 연결
conn = duckdb.connect("D:/project/WaveLang/wave_data.duckdb")

print("== 테이블 존재 여부 확인 ==")
tables = conn.execute("SHOW TABLES").fetchall()
print([t[0] for t in tables])

if 'tick_NQ' not in [t[0] for t in tables]:
    print("❌ 'tick_NQ' 테이블이 존재하지 않습니다.")
else:
    print("✅ 'tick_NQ' 테이블 존재 확인")

    print("\n== 전체 row 수 ==")
    count = conn.execute("SELECT COUNT(*) FROM tick_NQ").fetchone()[0]
    print(f"{count:,} rows")

    print("\n== 날짜 범위 확인 ==")
    date_range = conn.execute("""
        SELECT MIN(timestamp), MAX(timestamp)
        FROM tick_NQ
    """).fetchone()
    print(f"시작일: {date_range[0]}\n종료일: {date_range[1]}")

    print("\n== 일별 row 수 상위 5일 ==")
    top_days = conn.execute("""
        SELECT DATE(timestamp) AS day, COUNT(*) AS count
        FROM tick_NQ
        GROUP BY day
        ORDER BY count DESC
        LIMIT 5
    """).df()
    print(top_days)

    print("\n== 샘플 5개 행 ==")
    print(conn.execute("""
        SELECT *
        FROM tick_NQ
        ORDER BY timestamp
        LIMIT 5
    """).df())

conn.close()
