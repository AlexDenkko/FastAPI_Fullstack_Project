import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
 # tämät testit tarkistavat, ovatko luvut yhtä suuret tai eivät

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)
 # Tämä testi tarkistaa, onko objekti luokan instanssi vai ei
def test_boolean():
    validated = True
    assert validated is True
    assert ( "hello" == "world" ) is False
 # Tämä testi tarkistaa boolean-arvot ja -lausekkeet
def test_type():
    assert type("Hello") is str
    assert type("World") is not int
 # Tämä testi tarkistaa objektin tyypin
def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10
    assert not (5 < 3)
    assert not (2 > 4)
 # Tämä testi tarkistaa suuremmat kuin ja pienemmät kuin vertailut

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)
 # Tämä testi tarkistaa listan operaatioita, kuten jäsenyyttä, all ja any


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
 # Tämä luokka edustaa opiskelijaa, jolla on attribuutit etunimelle, sukunimelle, pääaineelle ja opiskeluvuosille
@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)
 # Tämä fixture luo oletusopiskelija-olion testamista varten

def test_person_intialization(default_employee):
    assert default_employee.first_name == "John" ,"First name should be John"
    assert default_employee.last_name == "Doe" ,   "Last name should be Doe"
    assert default_employee.major == "Computer Science" , "Major should be Computer Science"
    assert default_employee.years == 3 , "Years should be 3"
 # Tämä testi tarkistaa opiskelijaluokan attribuuttien alustamisen