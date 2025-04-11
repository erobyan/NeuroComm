# NeuroComm - Simulador de señales EEG

**NeuroComm** es un simulador de señales EEG desarrollado en Python con Dash. El sistema genera ondas cerebrales artificiales (delta, theta, alpha, beta y gamma), analiza su contenido frecuencial y clasifica el estado mental simulado en función de la frecuencia dominante. Además, ofrece una interfaz web interactiva para la visualización en tiempo real de las señales y su espectro.

## Objetivos

- Simular señales EEG con ruido blanco.
- Detectar la frecuencia dominante mediante análisis espectral (FFT).
- Clasificar el estado mental: relajado, concentrado, somnoliento, etc.
- Representar visualmente las señales EEG y su transformada.
- Proporcionar una interfaz interactiva con visualización de estado.

## Tecnologías utilizadas

- Python 3
- Dash y Plotly
- NumPy, pandas
- Dash Bootstrap Components (estilo oscuro)

## Características principales

- Simulación en tiempo real de señales EEG sintéticas.
- Análisis de frecuencia con transformada rápida de Fourier (FFT).
- Clasificación automática del estado mental por frecuencia dominante.
- Interfaz web responsiva con pestañas de visualización.
- Representación visual del estado mediante barras iluminadas.
- Modal interactivo para visualizar los datos y exportarlos como CSV.

## Estructura del proyecto

```
NeuroComm/
├── dash_app.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── signal_generator.py
│   ├── signal_analyzer.py
│   └── state_classifier.py
```

## Instalación local

```bash
git clone https://github.com/erobyan/NeuroComm.git
cd NeuroComm
python3 -m venv venv
source venv/bin/activate      # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python dash_app.py
```

## Uso

1. Ejecutar el archivo `dash_app.py`.
2. Abrir el navegador en `http://127.0.0.1:8050`.
3. Seleccionar un estado mental para simular.
4. Visualizar la señal, su FFT y el estado detectado.
5. Exportar los datos simulados desde el modal.

## Licencia

Este proyecto está licenciado bajo la MIT License.

