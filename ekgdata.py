import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import find_peaks
import json
class EKGdata:
    def __init__(self, ekg_dict):
        '''Initialisiert die EKG-Daten mit einem Dictionary, das die EKG-Daten enthält.'''
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])

    @staticmethod
    def load_by_id(ekg_id, ekg_dict):
        '''Lädt die EKG-Daten anhand der ID aus einem Dictionary, das die EKG-Daten enthält.'''
        for ekg_index in ekg_dict:
            if ekg_index['id'] == ekg_id:
                return EKGdata(ekg_index)
        return None

    def peak_finder(self):
        '''Findet die Peaks in den EKG-Daten und gibt die Indizes zurück.'''
        df_subset = self.df.head(2000)
        peaks, _ = find_peaks(df_subset["Messwerte in mV"], height=350)
        return peaks

    def make_plot(self):
        '''Erstellt einen Plot der EKG-Daten und markiert die Peaks.'''
        df_subset = self.df.head(2000)
        fig = px.line(df_subset, x="Zeit in ms", y="Messwerte in mV", title="EKG-Daten mit Peaks (Erste 2000 Datenpunkte)")

        peaks = self.peak_finder()

        # Peaks als rote Punkte hinzufügen
        fig.add_trace(go.Scatter(
            x=df_subset["Zeit in ms"].iloc[peaks],
            y=df_subset["Messwerte in mV"].iloc[peaks],
            mode='markers',
            marker=dict(color='red', size=8),
            name='Peaks'
        ))
        return fig

    def estimate_hr(self):
        '''Berrechnet die Herzfrequenz anhand der Peaks in den EKG-Daten.'''
        df_subset = self.df.head(2000)
        peaks = self.peak_finder()
        peak_count = len(peaks)
        time_max = df_subset["Zeit in ms"].max()
        time_min = df_subset["Zeit in ms"].min()
        time_duration = (time_max - time_min) / 60000  # Umrechnung in Minuten
        hr = peak_count / time_duration
        return hr

    def show_head(self):
        '''Zeigt den Head der EKG-Daten an (Erste 2000 Datenpunkte).'''
        print(self.df.head(2000))
    
    def get_length_test(self):
        # Assuming 'data' is a list of timestamps in milliseconds
        start_time = self.ekg_dict['data'][0]
        end_time = self.ekg_dict['data'][-1]
        duration_ms = end_time - start_time
        duration_s = duration_ms / 1000  # Convert milliseconds to seconds
        return duration_s



if __name__ == "__main__":
    # JSON-Datei und EKG-Daten laden
    with open("data/person_db.json", 'r') as file:
        persons_data = json.load(file)
    
    ekg_dicts = persons_data[0]["ekg_tests"]
    ekg = EKGdata.load_by_id(1, ekg_dicts)
    
    # Zeige den Head der ersten 2000 Daten an
    ekg.show_head()

    # Plot mit markierten Peaks erstellen und anzeigen (erste 2000 Datenpunkte)
    fig = ekg.make_plot()
    fig.show()
    
    peak_array = ekg.peak_finder()
    print("Um die Rechenzeit zu verkürzen, wurden nur die ersten 2000 Datenpunkte betrachtet.")
    print("Number of Peaks:", peak_array.size)
    print("Estimated Heart Rate:", ekg.estimate_hr())