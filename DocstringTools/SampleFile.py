class SampleFile:

    VALID_AGE = 18

    def __init__(self, name, age, phone_number, zip_code) -> None:
        self.name = name
        self.age = age
        self.phone_number = phone_number
        self.zip_code = zip_code

    def is_valid(self, name, age) -> bool:
        """
        Method to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular person
        
        :param name: Name of the personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular personMethod to check if age is valid for a particular person

        :return: true or false
        :raises ValueError: if age is wrong
        """
        if age < 0:
            raise ValueError("Wrong age value!")
        elif age >= self.VALID_AGE:
            print(f"{name} is {age} years old and is valid!")
            return True
        else:
            print(f"{name} is {age} years old and is in-valid!")
            return False
    
    def print_values(self):
        print(f"NAME: {self.name}\nAGE: {self.age}\nPHONE_NUMBER: {self.phone_number}\nZIP_CODE: {self.zip_code}")
    
    def _protected_is_valid(self, name, age):
        print(f"This does nothing {name}, {age}")
    
    def __private_is_valid(self, name):
        print(f"This does nothing as well {name}")
