from .wave_box import WaveBox

class WaveBuilder:
    def __init__(self, threshold):
        self.threshold = threshold
        self.reset()

    def reset(self):
        self.current_wave = None
        self.waves = []

    def feed(self, time, price):
        if self.current_wave is None:
            self.current_wave = {'start_time': time, 'start_price': price}
            return None

        price_change = price - self.current_wave['start_price']
        direction = 'up' if price_change > 0 else 'down'

        if abs(price_change) >= self.threshold:
            wave = WaveBox(
                start_time=self.current_wave['start_time'],
                end_time=time,
                start_price=self.current_wave['start_price'],
                end_price=price,
                direction=direction
            )
            self.waves.append(wave)
            self.current_wave = {'start_time': time, 'start_price': price}
            return wave
        return None

    def get_all_waves(self):
        return self.waves
