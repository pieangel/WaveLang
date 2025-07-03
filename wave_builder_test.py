import csv
from datetime import datetime
from wave.wave_builder import WaveBuilder

if __name__ == "__main__":
    builder = WaveBuilder(threshold=2.5)
    builder.build_from_csv("data/NQ_TickData/NQ_2009_09.csv")
    builder.plot_waves("Wave Chart: 2009-09-27")
