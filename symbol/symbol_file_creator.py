import pandas as pd

# 데이터 구성
data = [
    ["JY", "Japanese Yen Futures", 6, 12500000, 12.5, 0.0000005, 6.25, "JY", "CME FX", "", ""],
    ["TY", "10-Year T-Note Futures", 3, 100000, 1000, 0.015625, 15.625, "TY", "CBOT Rates", "", ""],
    ["FV", "5-Year T-Note Futures", 3, 100000, 1000, 0.0078125, 7.8125, "FV", "CBOT Rates", "", ""],
    ["ES", "E-mini S&P 500 Futures", 2, 50, 50, 0.25, 12.5, "ES", "CME Equity Index", "", ""],
    ["EU", "Euro FX Futures", 4, 125000, 125000, 0.0001, 12.5, "6E", "CME FX", "", ""],
    ["US", "30-Year T-Bond Futures", 3, 100000, 1000, 0.015625, 15.625, "US", "CBOT Rates", "", ""],
    ["NQ", "E-mini NASDAQ-100 Futures", 2, 20, 20, 0.25, 5.0, "NQ", "CME Equity Index", "", ""],
    ["GC", "Gold Futures", 1, 100, 100, 0.1, 10.0, "GC", "COMEX Metals", "", ""],
    ["CL", "Crude Oil Futures", 2, 1000, 1000, 0.01, 10.0, "CL", "NYMEX Energy", "", ""],
    ["BP", "British Pound Futures", 4, 62500, 62500, 0.0001, 6.25, "6B", "CME FX", "", ""],
]

# 컬럼 정의
columns = [
    "_SymbolCode", "_Name", "_Decimal", "_Seungsu", "_CtrUnit",
    "_TickSize", "_TickValue", "_RootCode", "_MarketName",
    "_NearMonth", "_LastDate"
]

# 데이터프레임 생성
df = pd.DataFrame(data, columns=columns)

# CSV 파일로 저장
csv_path = "/data/us_futures_symbols.csv"
df.to_csv(csv_path, index=False)

