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

    st.session_state.current_test = st.selectbox(
         "Wähle Test aus",
         options= Person.get_EKG_tests(Person.get_person_data())
         , key="sbTest")
    
    
    ekg_dict = person_dict["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)
    ekg.make_plot()
    st.plotly_chart(ekg.fig)
    st.write("EKG ID: ", ekg_dict["id"])
    


