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

    # EKG-Daten laden
    ekg_dict = person_dict["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)

    fig = ekg.make_plot()
    st.plotly_chart(fig)

    hr = ekg.estimate_hr()
    st.write(f" Herzfrequenz von {selected_user} beträgt ca {hr:.2f} BPM")

    st.write("EKG ID: ", ekg_dict["id"])

