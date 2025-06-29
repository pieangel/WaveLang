from wave.wave_builder import WaveBuilder

builder = WaveBuilder(threshold=10)
waves = builder.build_from_csv("data/NQ_TickData/NQ_2009_09.csv")

for i, wave in enumerate(waves):
    print(f"Wave {i+1}: {wave}")
