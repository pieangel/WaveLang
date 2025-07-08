
import csv
from datetime import datetime
from typing import List, Tuple

def load_prices_with_time(file_path: str) -> List[Tuple[datetime, float]]:
    result = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            try:
                timestamp = datetime.strptime(f"{row[0]} {row[1]}", "%m/%d/%Y %H:%M:%S")
                price = float(row[2])
                result.append((timestamp, price))
            except ValueError:
                continue
    return result
