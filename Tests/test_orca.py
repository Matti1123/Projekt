

import plotly.graph_objects as go
import plotly.io as pio

# Aktualisieren der Orca-Konfiguration mit dem korrekten Pfad zur Orca-Executable
pio.orca.config.executable = "test_orca.py"  # Passen Sie diesen Pfad an

# Erstellen eines einfachen Balkendiagramms
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))

try:
    # Versuchen, das Bild mit orca zu speichern
    fig.write_image("test_plot_orca.png", engine='orca')
    print("Plot erfolgreich gespeichert.")
except Exception as e:
    # Wenn ein Fehler auftritt, wird dieser gedruckt
    print(f"Fehler beim Speichern des Plots: {e}")

# Konfiguration speichern
pio.orca.config.save()