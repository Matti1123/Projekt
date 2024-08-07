# EKG Analyse App

Diese App ermöglicht die Analyse und Visualisierung von EKG-Daten sowie die Verwaltung von Benutzerdaten. Zusätzlich bietet sie die Möglichkeit, einen bestimmten Zeitraum eines EKGs zu bearbeiten, mithilfe von Tools zu modifizieren und das bearbeitete Bild zu speichern. Außerdem lassen sich verschiedene Farbmodifikationen einstellen, um sehbehinderten Personen zu helfen. Wir empfehlen diese App insbesondere Kardiologen, um die Daten verschiedener Patienten schnell zu visualisieren und ihnen mithilfe unserer Bearbeitungsfunktion mögliche Fehler klarer darzustellen.


## Setup

1. Klonen Sie das Repository in Ihre gewünschte Programmierumgebung:
    ```bash
    git clone <repository-url>
    ```
2. Navigieren Sie in das Projektverzeichnis:
    ```bash
    cd <repository-directory>
    ```
3. Erstellen Sie eine virtuelle Umgebung:
    ```bash
    python -m venv .venv
    ```
4. Aktivieren Sie die virtuelle Umgebung:
    - Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    - Linux/Mac:
        ```bash
        source .venv/bin/activate
        ```
    - Falls es hierbei zu einem Fehler kommt, führen Sie folgenden Befehl aus und aktivieren Sie die virtuelle Umgebung erneut:
        ```bash
        Set-ExecutionPolicy Unrestricted -Scope Process
        ```
5. Installieren Sie alle benötigten Pakete:
    ```bash
    pip install -r requirements.txt
    ```
6. Laden Sie Ihre eigenen Daten in die Applikation hoch. Als Beispiel wurde hier mit `activity.csv` gearbeitet.
7. Starten Sie die Anwendung:
    ```bash
    streamlit run main.py
    ```

## Funktionsweise der Anwendung

### Hauptfunktionen

1. **EKG Analyse**:
    - Wählen Sie eine Versuchsperson aus der Dropdown-Liste aus.
    - Wählen Sie einen spezifischen EKG-Test für die ausgewählte Person.
    - Visualisieren Sie die EKG-Daten und sehen Sie sich relevante Informationen wie die geschätzte Herzfrequenz und die Dauer des Tests an.
    - Nutzen Sie den Slider, um einen Startpunkt in den EKG-Daten auszuwählen.

2. **Neue Person hinzufügen**:
    - Geben Sie die Daten einer neuen Versuchsperson ein, einschließlich Vorname, Nachname, Geburtsjahr und einem Bild.
    - Laden Sie das Bild hoch und speichern Sie die Person in der Datenbank.

3. **Neuen EKG-Test hinzufügen**:
    - Wählen Sie eine Versuchsperson aus.
    - Geben Sie das Datum des EKG-Tests ein.
    - Laden Sie die EKG-Daten hoch und speichern Sie den Test für die ausgewählte Person.
4. **Neuen EKG-Test hinzufügen**:
    - Wählen Sie mithilfe des Sliders ein gewünschten Bereich des Ekg`s aus.
    - Drücken sie den "Erstellen sie ein Screenshot" button um von dem ausgewählten Bereich eine Abbildung zu erhalten.
    - Laden Sie die Abbildung in einen beschreibbaren Canvas hier kann der Diagnostiker auftretende Herzrhythmusstörungen einzeichnen.
          - hierbei kann zwischen dem freedraw und dem mess modus gewechselt werden.
    - Zuletzt können sie ihren beschriebenen Canvas noch per Button als Json-File abspeichern und zum Beispiel an Patienten versenden.
   



### Farbblindheitseinstellungen

Die Anwendung bietet Anpassungsmöglichkeiten für verschiedene Formen von Farbblindheit:
- **Normal**: Standard-Farbmodus.
- **Protanopie**: Anpassung für Rot-Grün-Farbblindheit.
- **Deuteranopie**: Anpassung für Rot-Grün-Farbblindheit.
- **Tritanopie**: Anpassung für Blau-Gelb-Farbblindheit.

Verwenden Sie die Dropdown-Liste in der Seitenleiste, um den gewünschten Farbblindmodus auszuwählen. Die Farben der EKG-Visualisierungen werden entsprechend angepasst.

## Verzeichnisstruktur

- `main.py`: Hauptskript zur Ausführung der Streamlit-Anwendung.
- `def_persons.py`: Skript zur Verwaltung der Personendaten.
- `ekgdata.py`: Skript zur Verarbeitung und Analyse der EKG-Daten.
- `make_plot.py`: Skript zur Erstellung der Plots für Leistungs- und Herzfrequenzdaten.
- `data/`: Verzeichnis zur Speicherung der JSON-Datei mit den Personendaten und der EKG-Daten.
- `requirements.txt`: Datei zur Installation der benötigten Python-Pakete.
- `canvas.py´: Skript zur ver/bearbeitung des EKG-Plots

## Beispiel-Dateien

- `data/person_db.json`: JSON-Datei zur Speicherung der Personendaten und EKG-Tests.
- `data/ekg_data/`: Verzeichnis zur Speicherung der hochgeladenen EKG-Daten.
- `data/pictures/`: Verzeichnis zur Speicherung der hochgeladenen Bilder der Versuchspersonen.

---

Es ist normal zwischen 3-5 Minuten die Requirements herunterzuladen.


Abschließend muss man sagen, dass Streamlit wirklich nicht die beste Lösung für dieses interaktive Problem ist. Ich hatte schon große Probleme nur den Screenshot auf der Webseite anzuzeigen, außerdem gibt es in Streamlit keine Events und somit muss alles per Button aufgezeichnet werden, auch die Messung des R-Peak Abstandes wäre mit anderen Programmiersprachen viel einfacher gewesen. Im Nachhinein würde ich empfehlen, solche Probleme mit Javascript/HTML zu lösen, um sich viel Arbeit zu ersparen. Mit Python Streamlit ist die Datenanalyse meiner Meinung nach deutlich einfacher und intelligenter.
