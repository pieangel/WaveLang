# config.py
import os

# 프로젝트 루트 기준 상대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "tick_data.duckdb")
