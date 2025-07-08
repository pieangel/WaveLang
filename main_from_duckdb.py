import duckdb
from wave.db import build_waves_from_month
from wave.visualizer import plot_waves

# DuckDB 연결
conn = duckdb.connect("wave_data.duckdb")

# 한 달치 파동 생성
waves_by_day = build_waves_from_month(
    conn=conn,
    table_name="tick_NQ",
    symbol="NQ",
    year=2009,
    month=9,
    box_size=0.25,
    reverse_count=5
)

# 결과 요약 출력
print(f"📅 {len(waves_by_day)}일치 파동이 생성되었습니다.")

# 첫 번째 날 시각화
if waves_by_day:
    first_day = sorted(waves_by_day.keys())[0]
    print(f"📊 {first_day}의 파동 시각화 중...")
    plot_waves(waves_by_day[first_day])
else:
    print("❌ 해당 월에 생성된 파동이 없습니다.")
