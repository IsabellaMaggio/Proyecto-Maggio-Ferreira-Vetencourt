
# Con esta funcion traemos el llamado de todas las peliculas a través de la API, almacenamos en una lista que va a guardar nuestra Clase de pelicula con sus atributos
def get_movies():
    response = requests.get(f"{BASE_URL}/films")
    data = response.json()
    movies = [
        Movie(
            title=film['properties']['title'],
            episode_id=film['properties']['episode_id'],
            release_date=film['properties']['release_date'],
            director=film['properties']['director'],
            opening_crawl=film['properties']['opening_crawl'],
            characters = film['properties']['characters']
        ) for film in data['result']
    ]
    return movies


# #función que nos permite obtener los personajes por espcie
def get_character_name(url):
    response = requests.get(url)
    return response.json()['result']['properties']['name']


# #Funcion que nos permite obtener los episodios que se ha presentado un personaje
def get_episodes_for_characters(person_url):
    response = requests.get(f"{BASE_URL}/films")
    films = response.json()['result']
    episodes = []
    for film in films:
        for character_url in film['properties']['characters']:
            if character_url == person_url:
                episodes.append(film['properties']['title'])
    return episodes


# #Funcion que podemos el nombre del planeta de origen de la especie
def get_planet_name(url):
    response = requests.get(url)
    return response.json()['result']['properties']['name']

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
#Función que nos permite agarrar los planetas de cada episodio
def get_episodes_for_planets(planet_url):
    response = requests.get(f"{BASE_URL}/films")
    films = response.json()['result']
    episodes = []
    for film in films:
        for world_url in film['properties']['planets']:
            if world_url == planet_url:
                episodes.append(film['properties']['title'])
    return episodes


#agarramos todos los personajes de un planeta
def get_characters_from_planets(allCharacters, planetName):
    resident_names = []
    for person_url in allCharacters.values():
       
        if  person_url.homeworld == planetName:
            
            name = person_url.name
            resident_names.append(name)
    return resident_names


#Función que nos permite hacer la bsuqueda de un personaje

def search_character(characters, name):
    results = []
    name = name.lower()
    for character in characters.values():
        if name in character.name.lower():
            results.append(character)
    return results
