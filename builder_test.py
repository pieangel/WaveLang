from builders.ohlcv_builder import OhlcvBuilder

builder = OhlcvBuilder(ticks_per_bar=300)
builder.load_tick_data("data/NQ_TickData/NQ_2009_09.csv")
builder.build_ohlcv()
builder.save_ohlcv("output/nq_ohlcv_2009-09.csv")
builder.plot()