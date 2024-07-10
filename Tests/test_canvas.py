import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Seitenbreite festlegen
st.set_page_config(layout="wide")

# Sidebar für Optionen
st.sidebar.title('Canvas Optionen')

# Leeren Canvas anzeigen Button
if st.sidebar.button('Canvas anzeigen'):
    # Canvas anzeigen
    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Farbe für Freihandzeichnung
        stroke_width=2,
        update_streamlit=True,
        height=600,  # Höhe des Canvas
        width=1000,  # Breite des Canvas
        drawing_mode="freedraw",
        key="canvas"
    )
    st.success("Canvas erfolgreich angezeigt.")

# Hauptinhaltbereich
st.title('Großes Canvas zum Malen')
st.write("Klicken Sie auf den Button in der Sidebar, um das Canvas anzuzeigen.")