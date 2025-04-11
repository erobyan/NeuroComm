def perform_action(state):
    """
    Ejecuta una acción simulada en función del estado mental.
    """
    if "Beta" in state:
        print("💡 Acción: Encendiendo luz virtual (concentración)")
    elif "Alpha" in state:
        print("🌿 Acción: Mostrando mensaje de relajación")
    elif "Delta" in state:
        print("😴 Acción: Entrando en modo sueño")
    elif "Theta" in state:
        print("🧘 Acción: Activando ambiente relajado")
    elif "Gamma" in state:
        print("⚡ Acción: Alta actividad cerebral detectada")
    else:
        print("🤖 Acción: Estado desconocido, sin respuesta")
