# ekgdata.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import find_peaks

class EKGdata:
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])

    @staticmethod
    def load_by_id(ekg_id, ekg_dict):
        for ekg_index in ekg_dict:
            if ekg_index['id'] == ekg_id:
                return EKGdata(ekg_index)
        return None

    def peak_finder(self, df=None):
        if df is None:
            df = self.df
        peaks, _ = find_peaks(df["Messwerte in mV"], height=350)
        return peaks

    def make_plot(self, n_points=None):
        df_to_plot = self.df if n_points is None else self.df.head(n_points)
        fig = px.line(df_to_plot, x="Zeit in ms", y="Messwerte in mV", title="EKG-Daten mit Peaks")

        peaks = self.peak_finder(df_to_plot)

        # Peaks als rote Punkte hinzufügen
        fig.add_trace(go.Scatter(
            x=df_to_plot["Zeit in ms"].iloc[peaks],
            y=df_to_plot["Messwerte in mV"].iloc[peaks],
            mode='markers',
            marker=dict(color='red', size=8),
            name='Peaks'
        ))
        return fig

    def estimate_hr(self):
        peaks = self.peak_finder()
        peak_count = len(peaks)
        time_max = self.df["Zeit in ms"].max()
        time_min = self.df["Zeit in ms"].min()
        time_duration = (time_max - time_min) / 60000  # Umrechnung in Minuten
        hr = peak_count / time_duration
        return hr

    def get_length_test(self):
        start_time = self.df['Zeit in ms'].iloc[0]
        end_time = self.df['Zeit in ms'].iloc[-1]
        duration_ms = end_time - start_time
        duration_minutes = duration_ms / 60000  # Umrechnung in Minuten
        return duration_minutes



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