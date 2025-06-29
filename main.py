from wave.wave_builder import WaveBuilder

data = [
    (0, 100), (1, 101), (2, 103),
    (3, 104), (4, 98), (5, 96), (6, 101)
]

builder = WaveBuilder(threshold=5)

for t, price in data:
    wave = builder.feed(t, price)
    if wave:
        print("Wave Detected:", wave)

print("\nAll waves:")
for w in builder.get_all_waves():
    print(w)
