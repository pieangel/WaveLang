
import matplotlib.pyplot as plt
from .core import WaveBox, Direction

def plot_waves(waves: list[WaveBox]):
    fig, ax = plt.subplots(figsize=(14, 6))
    times = [wave.timestamp.strftime('%m-%d\n%H:%M') for wave in waves]
    x = list(range(len(waves)))

    for i, wave in enumerate(waves):
        color = 'red' if wave.direction == Direction.UP else 'blue'
        ax.plot([x[i], x[i]], [wave.low, wave.high], color='black', linewidth=1)
        ax.plot([x[i], x[i]], [wave.open, wave.close], color=color, linewidth=4)

    ax.set_title('Wave Chart (Equal Interval with Time Labels)')
    ax.set_xlabel('Wave Index / Time')
    ax.set_ylabel('Price')
    ax.set_xticks(x)
    ax.set_xticklabels(times, rotation=90, fontsize=8)
    ax.grid(True)
    plt.tight_layout()
    plt.show()
