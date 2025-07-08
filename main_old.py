import csv
from datetime import datetime
from wave_old.wave_builder import WaveBuilder

def load_csv(filepath):
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
            price = float(row['price'])
            yield time, price

# CSV 경로 설정 (예: 'data/sample.csv')
csv_path = 'data/sample.csv'

builder = WaveBuilder(threshold=5)

for time, price in load_csv(csv_path):
    wave = builder.feed(time, price)
    if wave:
        print("📡 Wave Detected:", wave)

print("\n📦 All Waves:")
for w in builder.get_all_waves():
    print(w)
