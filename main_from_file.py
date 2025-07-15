
from wave.core import WaveBuilder
from wave.loader import load_prices_with_time
from wave.visualizer import plot_waves

file_path = 'data/NQ_TickData/NQ_2025_05.csv'
print("🔄 데이터를 불러오는 중...")
data = load_prices_with_time(file_path)
print(f"✅ {len(data):,}개의 틱 데이터를 불러왔습니다.")

builder = WaveBuilder(box_size=5.0, reverse_count=5)
for timestamp, price in data:
    builder.add_price(price, timestamp)
builder.finalize()

waves = builder.get_waves()
print(f"📈 총 {len(waves)}개의 파동이 생성되었습니다.")
for i, wave in enumerate(waves[:10]):
    print(f"{i+1}: {wave.direction.name} {wave.timestamp} O:{wave.open} H:{wave.high} L:{wave.low} C:{wave.close}")

plot_waves(waves)
