import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from signal_generator import generate_eeg_signal
from signal_analyzer import compute_fft, get_dominant_frequency
from state_classifier import classify_state

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "NeuroComm - EEG"

# Estados simulables
states = {
    "Sueño (Delta)": (0.5, 4),
    "Relajación ligera (Theta)": (4, 8),
    "Relajado (Alpha)": (8, 13),
    "Concentración (Beta)": (13, 30),
    "Alta actividad (Gamma)": (30, 100)
}

state_colors = {
    "Delta": "#a64dff",
    "Theta": "#00ff88",
    "Alpha": "#00ccff",
    "Beta":  "#ffe600",
    "Gamma": "#ff6600",
}

# Layout
app.layout = dbc.Container([
    html.H1("NeuroComm - Simulador EEG", className="text-center", style={
        "color": "white", "fontWeight": "bold", "marginTop": "10px", "marginBottom": "5px"
    }),

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona el estado mental:", style={
                "color": "white", "fontWeight": "bold", "fontSize": "18px", "marginBottom": "8px"
            }),
            dcc.Dropdown(
                id="estado-dropdown",
                options=[{"label": k, "value": k} for k in states],
                value="Concentración (Beta)",
                clearable=False,
                style={"color": "#000"}
            )
        ], md=6)
    ], justify="center", className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="graph-tabs", value="eeg", children=[
                dcc.Tab(label="Señal EEG", value="eeg", style={
                    "backgroundColor": "#111", "color": "white", "padding": "4px", "height": "30px", "fontSize": "14px", "border": "none"
                }, selected_style={
                    "backgroundColor": "#333", "color": "white", "padding": "4px", "height": "30px", "fontSize": "14px", "border": "none"
                }),
                dcc.Tab(label="FFT (Frecuencia)", value="fft", style={
                    "backgroundColor": "#111", "color": "white", "padding": "4px", "height": "30px", "fontSize": "14px", "border": "none"
                }, selected_style={
                    "backgroundColor": "#333", "color": "white", "padding": "4px", "height": "30px", "fontSize": "14px", "border": "none"
                })
            ]),
            dcc.Graph(
                id="graph-output",
                config={
                    "displayModeBar": True,
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": "eeg_plot",
                        "height": 500,
                        "width": 900,
                        "scale": 1
                    }
                }
            ),
            dbc.Button("Mostrar datos EEG", id="open-modal", className="mt-3", style={
                "backgroundColor": "black",
                "color": "white",
                "border": "1px solid white",
                "fontWeight": "bold",
                "padding": "6px 16px"
            }),
        ])
    ]),

    # Estado mental y barras más arriba
    dbc.Row([
        dbc.Col(html.Div(id="barra-izquierda"), width=4),
        dbc.Col([
            html.Div(id="estado-detectado", className="h4", style={
                "color": "white", "textAlign": "center", "marginBottom": "0px"
            }),
            html.Div(id="frecuencia-detectada", className="h5", style={
                "color": "white", "textAlign": "center", "marginBottom": "20px"
            })
        ], width=4),
        dbc.Col(html.Div(id="barra-derecha"), width=4),
    ], align="center", justify="center", className="mt-1"),

    dcc.Interval(id="intervalo", interval=2000, n_intervals=0),

    dbc.Modal(
        id="modal",
        size="xl",
        centered=True,
        is_open=False,
        scrollable=True,
        style={"color": "white"},
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Datos de la señal EEG"), close_button=True),
            dbc.ModalBody(id="modal-table-body"),
            dbc.ModalFooter(
                dbc.Button("Cerrar", id="close-modal", className="ms-auto", color="secondary")
            )
        ]
    )
], fluid=True, style={"backgroundColor": "black", "minHeight": "100vh", "padding": "20px"})


# Callback principal
@app.callback(
    Output("graph-output", "figure"),
    Output("estado-detectado", "children"),
    Output("frecuencia-detectada", "children"),
    Output("barra-izquierda", "style"),
    Output("barra-derecha", "style"),
    Input("estado-dropdown", "value"),
    Input("intervalo", "n_intervals"),
    Input("graph-tabs", "value")
)
def actualizar_senal(estado_seleccionado, _, tipo_tab):
    freq_range = states[estado_seleccionado]
    t, signal = generate_eeg_signal(freq_range=freq_range)
    freqs, power = compute_fft(signal, fs=256)
    dominant_freq = get_dominant_frequency(freqs, power)
    estado = classify_state(dominant_freq)

    tipo_onda = next((k for k in state_colors if k in estado), "white")
    onda_color = state_colors.get(tipo_onda, "#ffffff")

    barra_style = {
        "height": "15px",
        "width": "100%",
        "backgroundColor": onda_color,
        "borderRadius": "10px",
        "boxShadow": f"0 0 25px {onda_color}88",
        "margin": "10px"
    }

    if tipo_tab == "eeg":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=signal, mode="lines", line=dict(color=onda_color, width=2.5), hoverinfo="skip"))
        fig.update_layout(template="plotly_dark", title="Señal EEG simulada",
                          xaxis_title="Tiempo (s)", yaxis_title="Amplitud",
                          margin=dict(t=40, r=20, l=20, b=20), font=dict(color="white"))
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=freqs, y=power, mode="lines", line=dict(color=onda_color, width=2.5), hoverinfo="skip"))
        fig.update_layout(template="plotly_dark", title="Espectro de Frecuencia (FFT)",
                          xaxis_title="Frecuencia (Hz)", yaxis_title="Magnitud",
                          margin=dict(t=40, r=20, l=20, b=20), font=dict(color="white"))

    return fig, f"Estado mental detectado: {estado}", f"Frecuencia dominante: {dominant_freq:.2f} Hz", barra_style, barra_style


# Modal open/cerrar
@app.callback(
    Output("modal", "is_open"),
    Input("open-modal", "n_clicks"),
    Input("close-modal", "n_clicks"),
    State("modal", "is_open")
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Cargar tabla
@app.callback(
    Output("modal-table-body", "children"),
    Input("open-modal", "n_clicks"),
    State("estado-dropdown", "value")
)
def cargar_tabla(n, estado):
    if not n:
        return None
    t, signal = generate_eeg_signal(freq_range=states[estado])
    df = pd.DataFrame({"Tiempo (s)": t, "Señal": signal})

    return dash_table.DataTable(
        data=df.round(4).to_dict("records"),
        columns=[{"name": col, "id": col} for col in df.columns],
        style_table={"maxHeight": "400px", "overflowY": "auto"},
        style_cell={"backgroundColor": "#111", "color": "white", "padding": "5px"},
        style_header={"backgroundColor": "#222", "fontWeight": "bold"},
        page_size=10
    )


if __name__ == "__main__":
    app.run(debug=True)
