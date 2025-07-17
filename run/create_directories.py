import os

# 생성할 디렉토리 목록
directories = [
    "wave_lang/wave",                 # 파동 로직 관련 모듈
    "wave_lang/io",                   # 입출력 모듈
    "wave_lang/symbol",              # 종목 정보 모듈
    "wave_lang/symbol/symbol_data"   # 종목 정보 CSV 저장 디렉토리
]

def create_directories():
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

if __name__ == "__main__":
    create_directories()
