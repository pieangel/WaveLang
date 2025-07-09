from builders.ohlcv_builder import OhlcvBuilder

builder = OhlcvBuilder(ticks_per_bar=300)
builder.load_tick_data("data/GC_TickData/GC_2009_11.csv")
builder.build_ohlcv()
builder.save_ohlcv("output/gc_ohlcv_2009-11.csv")
builder.plot()