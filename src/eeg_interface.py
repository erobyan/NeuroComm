import tkinter as tk
from tkinter import ttk
from signal_generator import generate_eeg_signal
from signal_analyzer import compute_fft, get_dominant_frequency
from state_classifier import classify_state
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

# Estilo para matplotlib
style.use("dark_background")

class EEGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 NeuroComm - Simulador EEG")
        self.root.configure(bg="#1e1e1e")

        self.states = {
            "Sueño (Delta)": (0.5, 4),
            "Relajación ligera (Theta)": (4, 8),
            "Relajado (Alpha)": (8, 13),
            "Concentración (Beta)": (13, 30),
            "Alta actividad (Gamma)": (30, 100)
        }

        self.selected_state = tk.StringVar()
        self.selected_state.set("Concentración (Beta)")

        # Dropdown personalizado
        self.dropdown = ttk.Combobox(root, textvariable=self.selected_state, values=list(self.states.keys()), font=("Helvetica", 12), width=30)
        self.dropdown.pack(pady=15)

        # Botón estilizado
        self.generate_button = tk.Button(root, text="🎬 Generar señal EEG", command=self.generate_signal, bg="#007acc", fg="white", font=("Helvetica", 12), relief="flat", padx=10, pady=5)
        self.generate_button.pack(pady=5)

        # Área gráfica
        self.figure, self.ax = plt.subplots(figsize=(7, 3), facecolor="#1e1e1e")
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors="white")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

        # Etiqueta de estado
        self.state_label = tk.Label(root, text="Estado mental: ---", font=("Helvetica", 14), fg="white", bg="#1e1e1e")
        self.state_label.pack(pady=10)

        # Luz virtual (círculo estilo LED)
        self.luz_canvas = tk.Canvas(root, width=60, height=60, bg="#1e1e1e", highlightthickness=0)
        self.luz = self.luz_canvas.create_oval(10, 10, 50, 50, fill="gray", outline="#444", width=2)
        self.luz_canvas.pack()

    def generate_signal(self):
        state = self.selected_state.get()
        freq_range = self.states[state]
        t, signal = generate_eeg_signal(freq_range=freq_range)

        freqs, power = compute_fft(signal, fs=256)
        dominant_freq = get_dominant_frequency(freqs, power)
        estado_detectado = classify_state(dominant_freq)

        # Actualizar gráfica
        self.ax.clear()
        self.ax.plot(t, signal, color="#4ec9b0")
        self.ax.set_title("Señal EEG simulada", color="white")
        self.ax.set_xlabel("Tiempo (s)", color="white")
        self.ax.set_ylabel("Amplitud", color="white")
        self.ax.grid(True, color="#333")
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors="white")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.canvas.draw()

        # Actualizar texto
        self.state_label.config(text=f"Estado mental detectado: {estado_detectado}")

        # Actualizar LED
        color = self.get_color_from_state(estado_detectado)
        self.luz_canvas.itemconfig(self.luz, fill=color)

    def get_color_from_state(self, estado):
        if "Beta" in estado:
            return "yellow"
        elif "Alpha" in estado:
            return "deepskyblue"
        elif "Delta" in estado:
            return "purple"
        elif "Theta" in estado:
            return "lime green"
        elif "Gamma" in estado:
            return "orange"
        else:
            return "gray"

if __name__ == "__main__":
    root = tk.Tk()
    app = EEGApp(root)
    root.mainloop()
