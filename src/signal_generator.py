import numpy as np

def generate_eeg_signal(freq_range=(8, 13), duration=5, fs=256):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    freq = np.random.uniform(freq_range[0], freq_range[1])
    eeg = np.sin(2 * np.pi * freq * t)
    noise = np.random.normal(0, 0.5, size=t.shape)
    signal = eeg + noise
    return t, signal
