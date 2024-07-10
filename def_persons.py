import json
from datetime import date

class Person:
    @staticmethod
    def get_person_data():
        """
        Gibt das person_data Dictionary zurück.
        """
        # Öffnen der JSON-Datei
        file = open("data/person_db.json")
        # Laden der JSON-Datei in ein Dictionary
        person_data = json.load(file)
        return person_data

    @staticmethod
    def save_person_data(person_data):
        """
        Speichert das person_data Dictionary in die JSON-Datei.
        """

        with open("data/person_db.json", 'w') as file:
            json.dump(person_data, file, indent=4)
    
    def __init__(self, person_data) -> None:
        """
        Initialisiert die Person mit einem Dictionary, das die Personendaten enthält.
        """
        self.date_of_birth = person_data["date_of_birth"]
        self.firstname = person_data["firstname"]
        self.lastname = person_data["lastname"]
        self.picture_path = person_data["picture_path"]
        self.id = person_data["id"]

    @staticmethod
    def get_names(person_data):
        """
        Gibt eine Liste von Namen aus dem person_data Dictionary zurück.
        """
        return [f"{person['firstname']} {person['lastname']}" for person in person_data]

    @staticmethod
    def find_person_data_by_name(suchstring):
        """
        Gibt die Personendaten für einen gegebenen Namen zurück.
        """
        
        vorname, nachname = suchstring.split(" ")
        person_data = Person.get_person_data()
        
        # Durchsuchen der Personendaten nach dem gegebenen Namen
        for eintrag in person_data:
            if eintrag["lastname"] == nachname and eintrag["firstname"] == vorname:
                return eintrag

    @staticmethod
    def get_EKG_tests_by_name(name):
        """
        Gibt die EKG-Tests für einen gegebenen Namen zurück.
        """
        person_data = Person.find_person_data_by_name(name)
        return person_data["ekg_tests"] if person_data else []

    def calc_age(self):
        """
        Berechnet das Alter der Person basierend auf dem Geburtsjahr.
        """
        current_year = date.today().year
        age = current_year - self.date_of_birth
        return age

    def estimate_max_hr(self):
        """
        Berechnet die maximale Herzfrequenz basierend auf dem Alter der Person.
        """
        max_hr_bpm = 220 - self.calc_age()
        return max_hr_bpm

    @staticmethod
    def load_by_id(person_id, person_data):
        """
        Gibt ein Personenobjekt mit der gegebenen person_id zurück.
        """
        for person_dict in person_data:
            if person_dict['id'] == person_id:
                return Person(person_dict)
        return None

    @staticmethod
    def add_person(firstname, lastname, date_of_birth, picture_path):
        """
        Fügt eine neue Person in die person_db.json Datei hinzu.
        """
        # Laden der Personendaten
        person_data = Person.get_person_data()
        
        # Generieren einer neuen ID für die Person
        new_id = max([person["id"] for person in person_data]) + 1
        
        # Erstellen eines neuen Personeneintrags
        new_person = {
            "id": new_id,
            "date_of_birth": date_of_birth,
            "firstname": firstname,
            "lastname": lastname,
            "picture_path": picture_path,
            "ekg_tests": []
        }
        # Hinzufügen der neuen Person zum person_data Dictionary
        person_data.append(new_person)
        # Speichern der aktualisierten Personendaten
        Person.save_person_data(person_data)
