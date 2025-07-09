from builders.ohlcv_builder_duckdb import OhlcvBuilder2

# 🟡 초기화: DuckDB 경로 및 테이블명 지정
builder = OhlcvBuilder2(
    db_path='wave_data.duckdb',       # ← 실제 DB 파일 경로
    table_name='tick_GC',           # ← DuckDB에 저장된 테이블명
    ticks_per_bar=300               # ← 한 봉에 몇 틱을 묶을지
)

# 🟡 월별 Tick 데이터 불러오기 (예: 2009년 9월)
builder.load_month_data(2009, 10)

# 🟡 OHLCV 데이터 생성
builder.build_ohlcv()

# 🟡 결과 DataFrame 확인
ohlcv_df = builder.get_ohlcv_df()
print(ohlcv_df.head())

# 🟡 차트 시각화
builder.plot()
