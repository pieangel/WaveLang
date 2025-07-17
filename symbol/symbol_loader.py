import pandas as pd
from .symbol_info import SymbolInfo

class SymbolLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_symbols(self):
        df = pd.read_csv(self.csv_path)
        return [SymbolInfo(**row._asdict()) for row in df.itertuples(index=False)]
