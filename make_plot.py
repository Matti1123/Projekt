import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
def power_mean():
    ''''''
    df = pd.read_csv("activity.csv", sep=',',header = 0)
    power_mean = df["PowerOriginal"].mean()
    return power_mean
def power_max():    
    df = pd.read_csv("activity.csv", sep=',',header = 0)
    power_max = df["PowerOriginal"].max()
    return power_max
def make_plot(input_heart_rate):
    df = pd.read_csv("activity.csv", sep=',',header = 0)
    df.head()
    max_heart_rate = input_heart_rate
    power_mean = df["PowerOriginal"].mean()
    power_max = df["PowerOriginal"].max()
    time = np.arange(len(df))
    print("Mean power: ", power_mean)
    print("Max power: ", power_max)


    fig = go.Figure()

    # Hinzufügen der PowerOriginal-Linie
    fig.add_trace(go.Scatter(x=time, y=df['PowerOriginal'], mode='lines', name='PowerOriginal',
                            yaxis='y1'))

    # Hinzufügen der HeartRate-Linie
    fig.add_trace(go.Scatter(x=time, y=df['HeartRate'], mode='lines', name='HeartRate',
                            yaxis='y2'))

    # Layout aktualisieren, um die sekundäre y-Achse zu unterstützen
    fig.update_layout(
        title='Power and Heart Rate over Time',
        xaxis_title='Time',
        yaxis_title='PowerOriginal',
        yaxis2=dict(
            title='HeartRate',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    heart_rate_zones = [0.5 * max_heart_rate, 0.6 * max_heart_rate, 0.7 * max_heart_rate, 0.8 * max_heart_rate, 0.9*max_heart_rate, max_heart_rate]
    color = ['green', 'yellow', 'orange', 'red', 'purple']



    # Zonen
    zone_times = []

    for i in range(len(heart_rate_zones)-1):
        zone_time = ((df["HeartRate"] >= heart_rate_zones[i]) & (df["HeartRate"] < heart_rate_zones[i+1])).sum()
        zone_times.append(zone_time)
        fig.add_shape(type="rect",
            xref="paper",
            yref="y2",
            x0=0,
            y0=heart_rate_zones[i],
            x1=1,
            y1=heart_rate_zones[i+1],
            fillcolor=color[i],
            opacity=0.3,
            layer="below")
    #Plot anzeigen
    return fig
print("Plot wird erstellt...")

def get_zone_times(input_heart_rate):
    df = pd.read_csv("activity.csv", sep=',', header=0)

    max_heart_rate = input_heart_rate

    heart_rate_zones = [0.5 * max_heart_rate, 0.6 * max_heart_rate, 0.7 * max_heart_rate, 0.8 * max_heart_rate, 0.9 * max_heart_rate, max_heart_rate]

    zone_times = []
    average_powers = []

    for i in range(len(heart_rate_zones)-1):
        zone_time = ((df["HeartRate"] >= heart_rate_zones[i]) & (df["HeartRate"] < heart_rate_zones[i+1])).sum()
        zone_time_minutes = zone_time / 60
        zone_times.append(zone_time_minutes)

        zone_power = df["PowerOriginal"][(df["HeartRate"] >= heart_rate_zones[i]) & (df["HeartRate"] < heart_rate_zones[i+1])]
        average_power = zone_power.mean()
        average_powers.append(average_power)

    # Create a DataFrame to return
    result_df = pd.DataFrame({
        'Zone': [f'Zone {i+1}' for i in range(len(zone_times))],
        'Zone Time in Minutes': zone_times,
        'Average Power': average_powers
    })

    return result_df
    #Wieviel in welche zone