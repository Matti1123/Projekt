import streamlit as st
from PIL import Image
from def_persons import Person
from ekgdata import EKGdata

# Set the page width
st.set_page_config(layout="wide")

# Sidebar for select boxes
st.sidebar.title('Select Options')

# Load person data
person_data = Person.get_person_data()

# option for selecting user
selected_user = st.sidebar.selectbox(
    "Versuchsperson",
    options=Person.get_names(person_data)
)

# Find selected person's data
person_dict = Person.find_person_data_by_name(selected_user)

# option for selecting test
selected_test_id = st.sidebar.selectbox(
    "Wähle Test aus",
    options=[test["id"] for test in person_dict["ekg_tests"]],
    key="sbTest"
)

# Find selected test data
selected_test = next(test for test in person_dict["ekg_tests"] if test["id"] == selected_test_id)
ekg = EKGdata(selected_test)
#Slider für die EKG Daten

start_point_sec = st.sidebar.slider("Startpunkt in Sekunden auswählen", 0.0, ekg.get_length_test()[0], 0.0, key="slider")
start_point_idx = ekg.get_index_from_time(start_point_sec)  # Umrechnung in Index


# Main content area
st.title('EKG Analyse App')

# Display selected user's information
st.write("Currently selected user: " + selected_user)
image = Image.open(person_dict["picture_path"])
st.image(image, caption=selected_user)
st.write("Geburtsjahr der Person:", person_dict["date_of_birth"])

# Display EKG Tests information
st.write("EKG Tests")
if selected_test_id != "None":
    fig = ekg.make_plot(start=start_point_idx, n_points=2000)
    
    #Optional: Adjust the width and height of the plot
    fig.update_layout(
        width=800,  # Adjust the width as needed
        height=400  # Optionally adjust the height
    )
    
    st.plotly_chart(fig, use_container_width=False)  

    hr = ekg.estimate_hr()
    st.write(f"Herzfrequenz von {selected_user} beträgt ca {hr:.2f} BPM")
    st.write("EKG ID: ", selected_test["id"])
    st.write("Wie viele Sekunden dauert der Test: ", ekg.get_length_test())
