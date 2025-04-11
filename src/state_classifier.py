def classify_state(freq):
    """
    Clasifica el estado mental en base a la frecuencia dominante.
    """
    if 0.5 <= freq < 4:
        return "Delta (sueño profundo)"
    elif 4 <= freq < 8:
        return "Theta (relajación ligera)"
    elif 8 <= freq < 13:
        return "Alpha (relajado)"
    elif 13 <= freq < 30:
        return "Beta (concentración)"
    elif 30 <= freq <= 100:
        return "Gamma (alta actividad)"
    else:
        return "Fuera de rango EEG"
