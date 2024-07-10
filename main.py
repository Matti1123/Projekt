import streamlit as st
from PIL import Image
from io import BytesIO
from def_persons import Person
from ekgdata import EKGdata
import json
import plotly.graph_objects as go
import plotly.io as pio
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import base64
import os
from streamlit_drawable_canvas import st_canvas

# Seitenbreite festlegen
st.set_page_config(layout="wide")

# Initialisiere den Zustand für den Screenshot und das Canvas
if "background_image" not in st.session_state:
    st.session_state["background_image"] = None
if "show_canvas" not in st.session_state:
    st.session_state["show_canvas"] = False
if "stroke_width" not in st.session_state:
    st.session_state["stroke_width"] = 3
if "stroke_color" not in st.session_state:
    st.session_state["stroke_color"] = "#000000"
if "bg_color" not in st.session_state:
    st.session_state["bg_color"] = "#ffffff"

# Laden der Personendaten
person_data = Person.get_person_data()

# Tabs für die Navigation
tab1, tab2, tab3 = st.tabs(["EKG Analyse", "Neue Person hinzufügen", "Neuen EKG-Test hinzufügen"])

def create_screenshot(fig):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Convert the figure to an HTML string
    html_str = pio.to_html(fig, full_html=False)
    
    # Save the HTML string to a temporary file with UTF-8 encoding
    temp_file_path = os.path.abspath("temp_plot.html")
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    
    # Load the HTML file in the browser
    driver.get("file://" + temp_file_path)
    
    # Take a screenshot and get it as base64
    screenshot_base64 = driver.get_screenshot_as_base64()
    driver.quit()
    
    return screenshot_base64

def set_canvas_background(screenshot_base64):
    background_image = Image.open(BytesIO(base64.b64decode(screenshot_base64)))
    return background_image

with tab1:
    # Sidebar für Auswahlboxen
    st.sidebar.title('Auswahlmöglichkeiten')

    # Option zur Auswahl des Benutzers
    selected_user = st.sidebar.selectbox(
        "Versuchsperson",
        options=Person.get_names(person_data)
    )

    # Daten der ausgewählten Person finden
    person_dict = Person.find_person_data_by_name(selected_user)

    # Option zur Auswahl des Tests
    if person_dict and "ekg_tests" in person_dict:
        selected_test_id = st.sidebar.selectbox(
            "Wähle Test aus",
            options=[test["id"] for test in person_dict["ekg_tests"]],
            key="sbTest"
        )
        
        # Daten des ausgewählten Tests finden
        selected_test = next((test for test in person_dict["ekg_tests"] if test["id"] == selected_test_id), None)
        if selected_test:
            ekg = EKGdata(selected_test)

            # Slider für die EKG Daten
            start_point_sec = st.sidebar.slider("Startpunkt in Sekunden auswählen", 0.0, ekg.get_length_test()[0], 0.0, key="slider")
            start_point_idx = ekg.get_index_from_time(start_point_sec)  # Umrechnung in Index

            # Hauptinhaltbereich
            st.title('EKG Analyse App')

            # Informationen über die ausgewählte Person anzeigen
            st.write("Aktuell ausgewählte Person: " + selected_user)
            image = Image.open(person_dict["picture_path"])
            st.image(image, caption=selected_user)
            st.write("Geburtsjahr der Person:", person_dict["date_of_birth"])

            # Informationen über EKG-Tests anzeigen
            st.write("EKG Tests")
            if selected_test_id != "None":
                fig = ekg.make_plot(start=start_point_idx, n_points=2000)
                
                # Optional: Breite und Höhe des Plots anpassen
                fig.update_layout(
                    width=800,  # Breite nach Bedarf anpassen
                    height=400  # Höhe optional anpassen
                )
                
                st.plotly_chart(fig, use_container_width=False)

                hr = ekg.estimate_hr()
                st.write("Testdatum: ", selected_test["date"])
                st.write(f"Herzfrequenz von {selected_user} beträgt ca {hr:.2f} BPM")
                st.write("EKG ID: ", selected_test["id"])
                st.write("Wie viele Sekunden dauert der Test: ", ekg.get_length_test())

                # Button zum Erstellen und Anzeigen des Screenshots in der Sidebar
                if st.sidebar.button('Screenshot erstellen und anzeigen'):
                    try:
                        # Debugging-Nachricht: Start des Renderings
                        st.write("Starte das Rendern des Plots...")

                        # Screenshot erstellen
                        screenshot_base64 = create_screenshot(fig)
                        
                        # Debugging-Nachricht: Rendern erfolgreich
                        st.write("Plot erfolgreich gerendert.")

                        # Hintergrundbild festlegen
                        background_image = set_canvas_background(screenshot_base64)

                        # Screenshot anzeigen
                        st.image(background_image, caption='Screenshot des aktuellen Plots')
                        st.session_state["background_image"] = background_image  # Speichern des Screenshots im Session State
                        st.success("Screenshot erfolgreich erstellt und angezeigt.")
                    except Exception as e:
                        st.error(f"Fehler beim Erstellen des Screenshots: {e}")
                        st.error(f"Fehlerdetails: {str(e)}")

                # Button zum Erstellen und Anzeigen eines leeren Canvas in der Sidebar
                if st.sidebar.button('Canvas anzeigen'):
                    st.session_state["show_canvas"] = True

                # Canvas und Optionen anzeigen, wenn der Zustand aktiviert ist
                if st.session_state["show_canvas"]:
                    col1, col2 = st.columns([4, 1])  # Verteilung des Layouts zwischen Canvas und Optionen
                    with col1:
                        canvas_result = st_canvas(
                            fill_color=st.session_state["bg_color"],  # Hintergrundfarbe für Freihandzeichnung
                            stroke_width=st.session_state["stroke_width"],
                            stroke_color=st.session_state["stroke_color"],
                            background_image=st.session_state["background_image"],
                            update_streamlit=True,
                            height=400,
                            width=800,
                            drawing_mode="freedraw",
                            key="canvas"
                        )
                    with col2:
                        st.write("### Optionen")
                        st.session_state["stroke_width"] = st.slider("Strichstärke", 1, 25, st.session_state["stroke_width"])
                        st.session_state["stroke_color"] = st.color_picker("Strichfarbe", st.session_state["stroke_color"])
                        st.session_state["bg_color"] = st.color_picker("Hintergrundfarbe", st.session_state["bg_color"])

                    st.success("Canvas erfolgreich angezeigt.")
        else:
            st.sidebar.warning("Kein EKG-Test verfügbar. Bitte fügen Sie einen neuen Test hinzu.")
    else:
        st.sidebar.warning("Bitte wählen Sie eine gültige Versuchsperson aus.")

with tab2:
    st.title("Neue Person hinzufügen")
    with st.form(key='new_person_form'):
        firstname = st.text_input("Vorname")
        lastname = st.text_input("Nachname")
        date_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=2023, step=1)
        uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
        submit_button = st.form_submit_button(label='Hinzufügen')
        
        if submit_button and uploaded_file is not None:
            # Hochgeladene Datei im Bilderverzeichnis speichern
            pictures_dir = "data/pictures"
            if not os.path.exists(pictures_dir):
                os.makedirs(pictures_dir)
            
            # Generiere einen eindeutigen Dateinamen
            file_extension = os.path.splitext(uploaded_file.name)[1]
            picture_path = os.path.join(pictures_dir, f"{firstname}_{lastname}{file_extension}")
            
            # Datei speichern
            with open(picture_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Person zur Datenbank hinzufügen
            Person.add_person(firstname, lastname, date_of_birth, picture_path)
            st.success("Neue Person hinzugefügt!")

with tab3:
    st.title("Neuen EKG-Test hinzufügen")
    with st.form(key='new_ekg_test_form'):
        selected_user = st.selectbox(
            "Versuchsperson",
            options=Person.get_names(person_data)
        )
        ekg_date = st.date_input("Datum des EKG-Tests")
        ekg_file = st.file_uploader("EKG-Datei hochladen", type=["txt", "csv"])
        submit_button = st.form_submit_button(label='Hinzufügen')

        if submit_button and ekg_file is not None:
            person_dict = Person.find_person_data_by_name(selected_user)
            if person_dict:
                # Hochgeladene EKG-Datei im EKG-Datenverzeichnis speichern
                ekg_dir = "data/ekg_data"
                if not os.path.exists(ekg_dir):
                    os.makedirs(ekg_dir)
                
                # Generiere einen eindeutigen Dateinamen
                file_extension = os.path.splitext(ekg_file.name)[1]
                ekg_path = os.path.join(ekg_dir, f"{person_dict['id']}_{ekg_date}{file_extension}")
                
                # Datei speichern
                with open(ekg_path, "wb") as f:
                    f.write(ekg_file.getbuffer())
                
                # EKG-Test zu den Personendaten hinzufügen
                new_test_id = max([test["id"] for test in person_dict.get("ekg_tests", [])], default=0) + 1
                new_test = {
                    "id": new_test_id,
                    "date": ekg_date.strftime("%d.%m.%Y"),
                    "result_link": ekg_path
                }
                person_dict["ekg_tests"].append(new_test)
                
                # Aktualisierte Personendaten speichern
                for i, person in enumerate(person_data):
                    if person["id"] == person_dict["id"]:
                        person_data[i] = person_dict
                        break
                
                with open("data/person_db.json", 'w') as file:
                    json.dump(person_data, file, indent=4)

                st.success("Neuer EKG-Test hinzugefügt!")