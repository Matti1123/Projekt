import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from make_plot import make_plot
from make_plot import get_zone_times
from make_plot import power_mean
from make_plot import power_max
from def_persons import Person
from ekgdata import EKGdata
tab_Person_EKG,tab_test = st.tabs(["Person_EKG","test"])

with tab_Person_EKG:


    if "current_user" not in st.session_state:
        st.session_state.current_user = "None"

    st.header("Person")


    st.session_state.current_user = st.selectbox(
         "Wähle Versuchsperson",
         options= Person.get_names(Person.get_person_data())
         , key="sbVersuchsperson")


    person_data = Person.get_person_data()
    # Paket zum anzeigen der Bilder
    from PIL import Image
    person_dict = Person.find_person_data_by_name(st.session_state.current_user)
    # Laden eines Bilds
    image = Image.open(person_dict["picture_path"])
    # Anzeigen eines Bilds mit Caption
    st.image(image, caption=st.session_state.current_user)
    #Geburtsjahr der Person anzeigen lassen
    current_year = Person.find_person_data_by_name(st.session_state.current_user)["date_of_birth"]
    st.write("Geburtsjahr der Person" ":", current_year)
    
    #Wahl der Tests einer Person ermöglichen
    st.write("EKG Tests")
    if "current_test" not in st.session_state:
        st.session_state.current_test = "None"

    person_ekg_tests = Person.get_EKG_tests_by_name(st.session_state.current_user)  # Update this line to get EKG tests for the selected person

    st.session_state.current_test = st.selectbox(
        "Wähle Test aus",
        options=[test["id"] for test in person_ekg_tests],  # Only show tests for the selected person
        key="sbTest"
    )

    if st.session_state.current_test != "None":
        selected_test = next(test for test in person_ekg_tests if test["id"] == st.session_state.current_test)
        ekg = EKGdata(selected_test)
        ekg.make_plot()
        st.plotly_chart(ekg.fig)
        st.write("EKG ID: ", selected_test["id"])
        st.write("Datum: ", selected_test["date"])
        duration = selected_test["duration"]
        st.write("Duration (in seconds): ", duration)
    


