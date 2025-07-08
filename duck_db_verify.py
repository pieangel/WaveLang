import os
import duckdb

def verify_duckdb_file(db_path: str):
    if not os.path.exists(db_path):
        print("❌ 파일이 존재하지 않습니다.")
        return False
    try:
        conn = duckdb.connect(db_path)
        conn.execute("PRAGMA show_tables").fetchall()
        conn.close()
        print("✅ DuckDB 파일이 정상입니다.")
        return True
    except Exception as e:
        print(f"⚠️ DuckDB 파일이 손상되었을 가능성 있음: {e}")
        return False

verify_duckdb_file("wave_data_broken.duckdb")
