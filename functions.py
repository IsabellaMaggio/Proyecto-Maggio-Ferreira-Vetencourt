
import requests
import pandas as pd
import matplotlib.pyplot as plt

from character import Character
from mission import Mision
from movie import Movie
from planet import Planet
from specie import Specie
from starship import Starship
from vehicle import Vehicle

#Vamos a declarar una base para utilizarla y a partir de aqui hacer las consultas a la SWAPI, para esto el equipo se guió de las clases y tambien de este video : https://youtu.be/gw8eS-7YRSc?si=mlM2d6T54CEz0Fx6 y consultas a CHATGPT openai.com
BASE_URL = "https://www.swapi.tech/api"

#Esta función nos permite agarrar toda la información de la data
def get_all_data(variable):
    data = []
    url = f"{BASE_URL}/{variable}"
    while url:
        response = requests.get(url)
        result = response.json()
        data.extend(result['results'])
        url = result['next']
    return data

#Esta función nos permite obtener la información de todos los personajes
def load_characters(species_data, starships_data,vehicles_data ):
    data = get_all_data('people')
    characters = {}
    for item in data:
        details = requests.get(item['url']).json()['result']['properties']
        species_name = find_species_for_character(details['name'], species_data)
        planet_name = get_planet_name(details['homeworld'])
        characters[item['uid']] = Character(
            name=details['name'],
            homeworld=planet_name,
            films=get_episodes_for_characters(item['url']),
            gender=details['gender'],
            species= species_name,
            starships= find_starships_for_character(item['url'], starships_data),
            vehicles=find_vehicles_for_character(item['url'], vehicles_data),
            url = details['url']
        )

    return characters

#Esta función nos permite obtner la specie de de los personajes
def find_species_for_character(character_url, species_data):
    for specie in species_data.values():
        if character_url in specie.people:
            return specie.name
    return ''


#Esta función nos permite obtener los vehiculos que maneja un personaje
def find_vehicles_for_character(character_url, vehicles_data):
    vehicles = []
    for vehicle in vehicles_data.values():
        if character_url in vehicle.pilots:
            vehicles.append(vehicle.name)
    if len(vehicles) == 0:
        return 'No vehicles for this character'
    return vehicles

#Esta función nos permite obtener las naves que maneja un personaje
def find_starships_for_character(character_url, starships_data):
    starships = []
    for starship in starships_data.values():
        if character_url in starship.pilots:
            starships.append(starship.name)
    if len(starships) == 0:
        return 'No starships for this character'
    return starships

#Funcioón que nos permite cargar todas las naves 
def load_starships():
    data = get_all_data('starships')
    starships = {}
    for item in data:
        details = requests.get(item['url']).json()['result']['properties']
        starships[item['uid']] = Starship(
            name=details['name'],
            model=details['model'],
            manufacturer=details['manufacturer'],
            passengers=details['passengers'],
            pilots=details['pilots'],
            url = item['url']
        )

    return starships

#Funcioón que nos permite cargar todos los vehículos 
def load_vehicles():
    data = get_all_data('vehicles')
    vehicles = {}
    for item in data:
        details = requests.get(item['url']).json()['result']['properties']
        vehicles[item['uid']] = Vehicle(
            name=details['name'],
            model=details['model'],
            manufacturer=details['manufacturer'],
            passengers=details['passengers'],
            pilots=details['pilots'],
            url = item['url']
        )

    return vehicles



#Función que permite cargar todos los planetas
def load_planets(characters):
    data = get_all_data('planets')
    planets = {}
    for item in data:
        details = requests.get(item['url']).json()['result']['properties']

        films_name = get_episodes_for_planets(item['url'])

        residents_name = get_characters_from_planets(characters, details['name'])
        planets[item['uid']] = Planet(
            name=details['name'],
            orbital_period=details['orbital_period'],
            rotation_period=details['rotation_period'],
            population=details['population'],
            climate=details['climate'],
            films=films_name,
            residents=residents_name,
            url = details['url']
        ) 
    return planets

#Función que permite cargar todas las especies
def load_species():
    data = get_all_data('species')
    species = {}
    for item in data:
        details = requests.get(item['url']).json()['result']['properties']
        people = []
        films = []
        for person in details['people']:
            name = get_character_name(person)
            film = get_episodes_for_characters(person)
            people.append(name)
            films.append(film)
        species[item['uid']] = Specie(
            name=details['name'],
            classification=details['classification'],
            average_height=details['average_height'],
            language=details['language'],
            homeworld=details['homeworld'],
            people=people,
            films=films,
            url = details['url']
        )
    return species
