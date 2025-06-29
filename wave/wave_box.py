class WaveBox:
    def __init__(self, start_time, end_time, start_price, end_price, direction):
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.end_price = end_price
        self.direction = direction  # "up" or "down"

    def __repr__(self):
        return f"WaveBox({self.start_time}~{self.end_time}, {self.direction}, ΔP={self.end_price - self.start_price})"
