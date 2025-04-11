import numpy as np

def compute_fft(signal, fs):
    """
    Aplica FFT a la señal y devuelve las frecuencias y su espectro.
    
    Parámetros:
    - signal: señal EEG (numpy array)
    - fs: frecuencia de muestreo

    Retorna:
    - freqs: frecuencias correspondientes (Hz)
    - power: magnitud del espectro
    """
    n = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(n, 1/fs)
    
    # Nos quedamos solo con la parte positiva del espectro
    pos_mask = fft_freqs >= 0
    freqs = fft_freqs[pos_mask]
    power = np.abs(fft_vals[pos_mask])  # Magnitud

    return freqs, power

def get_dominant_frequency(freqs, power):
    """
    Devuelve la frecuencia con mayor potencia.
    """
    idx = np.argmax(power)
    return freqs[idx]
