import json
from datetime import date
class Person:
    @staticmethod
    def get_person_data():
        """Returns the person_data dictionary."""
        file = open("data/person_db.json")

        # Loading the JSON File in a dictionary
        person_data = json.load(file)
        
        return person_data
    
    def __init__(self, person_data) -> None:
        '''Initialisiert die Person mit einem Dictionary, das die Personendaten enthält.'''
        self.date_of_birth = person_data["date_of_birth"]
        self.firstname = person_data["firstname"]
        self.lastname = person_data["lastname"]
        self.picture_path = person_data["picture_path"]
        self.id = person_data["id"]

    @staticmethod
    def get_names(person_data):
        '''Returns a list of names from the person_data dictionary.'''
        List_of_names = []
        
        for person in person_data:
            List_of_names.append(person["firstname"]+" "+person["lastname"])
        """Returns a list of names from the person_data dictionary."""
        return List_of_names


    @staticmethod
    def find_person_data_by_name(suchstring):
        '''Returns the person data for a given name.'''
        
        two_names = suchstring.split(" ")
        vorname = two_names[0]
        nachname = two_names[1]

        person_data = Person.get_person_data()

        for eintrag in person_data:
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                #print(eintrag)
                return eintrag
            
    @staticmethod
    def get_EKG_tests_by_name(name):
        '''Returns the EKG tests for a given name.'''
        person_data = Person.find_person_data_by_name(name)
        return person_data["ekg_tests"] if person_data else []
    
    
    def calc_age(self):
        '''Calculates the age of the person based on the date of birth.'''
        current_date = date.today()
        # Access the year attribute to get the current year
        current_year = current_date.year
        age = current_year - self.date_of_birth
        return age

        
    # hier wird angenommen dass die maximale Herzfrequenz 220 - Lebensalter ist für beide Geschlechter
    def estimate_max_hr(self):
        '''Estimates the maximum heart rate based on the age of the person.The gender of the person is not considered.'''
        max_hr_bpm = 220 - self.calc_age()
        return max_hr_bpm

    def load_by_id(person_id, person_data):
        '''Returns a person object with the given person_id.'''
        for person_dict in person_data:
            if person_dict['id'] == person_id:
                person = Person(
                    person_dict
                )
                return person
        return None
        


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    current_user = Person.find_person_data_by_name("Julian Huber")
    print(current_user)
    print(current_user["picture_path"])
    tobi = Person(current_user)
    print(tobi.estimate_max_hr())
    print(tobi.calc_age())
    person_id_to_test = 1
    person = Person.load_by_id(person_id_to_test,person_data=Person.get_person_data())
    print(person.firstname)



