from symbol.symbol_loader import SymbolLoader

loader = SymbolLoader("symbol/symbol_data/futures_symbols.csv")
symbols = loader.load_symbols()

for sym in symbols:
    print(f"{sym.SymbolCode} → TickSize: {sym.TickSize}, TickValue: {sym.TickValue}")
