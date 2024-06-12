import streamlit as st
import json
from PIL import Image
from def_persons import Person
from ekgdata import EKGdata
from make_plot import make_plot, get_zone_times, power_mean, power_max

tab_Person_EKG, tab_test = st.tabs(["Person EKG", "test"])

with tab_Person_EKG:
    st.title('EKG Analyse App')

    person_data = Person.get_person_data()

    # Auswahl der Versuchsperson
    selected_user = st.selectbox(
        "Versuchsperson",
        options=Person.get_names(person_data)
    )

    st.write("Currently selected user: " + selected_user)
    person_dict = Person.find_person_data_by_name(selected_user)
    image = Image.open(person_dict["picture_path"])
    st.image(image, caption=selected_user)
    st.write("Geburtsjahr der Person:", person_dict["date_of_birth"])

    # EKG Tests
    st.write("EKG Tests")

    if "current_test" not in st.session_state:
        st.session_state.current_test = "None"

    person_ekg_tests = person_dict["ekg_tests"]

    st.session_state.current_test = st.selectbox(
        "Wähle Test aus",
        options=[test["id"] for test in person_ekg_tests],
        key="sbTest"
    )

    if st.session_state.current_test != "None":
        selected_test = next(test for test in person_ekg_tests if test["id"] == st.session_state.current_test)
        ekg = EKGdata(selected_test)

        fig = ekg.make_plot()
        st.plotly_chart(fig)

        hr = ekg.estimate_hr()
        st.write(f" Herzfrequenz von {selected_user} beträgt ca {hr:.2f} BPM")
        st.write("Datum des Tests: ", selected_test["date"])
        st.write("EKG ID: ", selected_test["id"])
        st.write("Wie viele Sekunden dauert der Test: ", ekg.get_length_test())
