import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from signal_generator import generate_eeg_signal
from signal_analyzer import compute_fft, get_dominant_frequency
import matplotlib.pyplot as plt

plt.switch_backend('TkAgg')

# Generar señal EEG
fs = 256  # Frecuencia de muestreo
t, signal = generate_eeg_signal(freq_range=(13, 30), fs=fs)

# Analizar señal en frecuencia
freqs, power = compute_fft(signal, fs)
dominant_freq = get_dominant_frequency(freqs, power)
print(f"🎯 Frecuencia dominante: {dominant_freq:.2f} Hz")


from state_classifier import classify_state

estado = classify_state(dominant_freq)
print(f"🧠 Estado mental detectado: {estado}")

from controller import perform_action

perform_action(estado)

# Graficar señal
plt.figure()
plt.plot(t, signal)
plt.title("Señal EEG simulada (Beta)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid(True)

# Graficar FFT
plt.figure()
plt.plot(freqs, power)
plt.title("Espectro de Frecuencia (FFT)")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.grid(True)

plt.show()

from visualizer import animate_signal

# Descomenta esta línea para probar visualización en tiempo real:
animate_signal(freq_range=(13, 30))
