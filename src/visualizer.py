import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from signal_generator import generate_eeg_signal

def animate_signal(freq_range=(13, 30), duration=5, fs=256):
    t, signal = generate_eeg_signal(freq_range=freq_range, duration=duration, fs=fs)

    fig, ax = plt.subplots()
    line, = ax.plot(t, signal)
    ax.set_xlim(0, duration)
    ax.set_ylim(-3, 3)
    ax.set_title("Señal EEG en tiempo real")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")

    def update(frame):
        _, new_signal = generate_eeg_signal(freq_range=freq_range, duration=duration, fs=fs)
        line.set_ydata(new_signal)
        return line,

    ani = animation.FuncAnimation(fig, update, interval=1000, blit=True)
    plt.show()
