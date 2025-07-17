from dataclasses import dataclass

@dataclass
class SymbolInfo:
    SymbolCode: str
    Name: str
    Decimal: int
    Seungsu: int
    CtrUnit: float
    TickSize: float
    TickValue: float
    RootCode: str
    MarketName: str
    NearMonth: int
    LastDate: str
