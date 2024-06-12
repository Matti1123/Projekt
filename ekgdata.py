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
        self.sample_rate = self.calculate_sample_rate()

    def calculate_sample_rate(self):
        time_diff = self.df['Zeit in ms'].diff().mean()  # Durchschnittliche Zeitdifferenz zwischen aufeinanderfolgenden Samples
        sample_rate = 1000 / time_diff  # Abtastrate in Hz (1 Sekunde = 1000 Millisekunden)
        return sample_rate

    def peak_finder(self, df=None):
        if df is None:
            df = self.df
        peaks, _ = find_peaks(df["Messwerte in mV"], height=350)
        return peaks

    def make_plot(self, start=0, n_points=2000):
        # Berechnen Sie das Ende basierend auf dem Start und der Anzahl der Punkte
        end = min(start + n_points, len(self.df))
        df_to_plot = self.df.iloc[start:end]
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
        duration_seconds = duration_ms / 1000  # Umrechnung in Sekunden
        duration_minutes = duration_ms / 60000  # Umrechnung in Minuten
        return duration_seconds, duration_minutes
    
    def get_index_from_time(self, time_sec):
        '''Berechnen Sie den Index basierend auf der Zeit in Sekunden'''
        # Berechnen Sie den Index basierend auf der Zeit in Sekunden
        return int(time_sec * self.sample_rate)  # Annahme: sample_rate ist die Abtastrate des EKGs