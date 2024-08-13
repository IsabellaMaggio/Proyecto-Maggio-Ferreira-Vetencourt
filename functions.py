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

#Esta función nos permite obtner la specie  de los personajes
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

#Función que nos permite cargar todas las naves 
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

#Función que nos permite cargar todos los vehículos 
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
            homeworld = get_planet_name(details['homeworld'])
        species[item['uid']] = Specie(
            name=details['name'],
            classification=details['classification'],
            average_height=details['average_height'],
            language=details['language'],
            homeworld=homeworld,
            people=people,
            films=films,
            url = details['url']
        )
    return species

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


# Gráfico de cantidad de personajes nacidos en cada planeta. Utilizamos pandas para leer el archivo .csv (https://youtu.be/_8onVOY2j4E?si=da5NtHjuFwfq604p, https://youtu.be/7WU3QixV_-s?si=PFO8BV7mt5sIucRQ)
def graphic_planet_homeworld():
    characters_df = pd.read_csv('csv/characters.csv')

    characters_by_homeworld = characters_df['homeworld'].value_counts()

    plt.figure(figsize=(10, 6))
    characters_by_homeworld.plot(kind='bar', color='skyblue')
    plt.title('Cantidad de personajes nacidos en cada planeta')
    plt.xlabel('Planeta')
    plt.ylabel('Cantidad de personajes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Gráfico de las características de una nave. Utilizamos pandas para leer el archivo .csv (https://youtu.be/_8onVOY2j4E?si=da5NtHjuFwfq604p, https://youtu.be/7WU3QixV_-s?si=PFO8BV7mt5sIucRQ)
def create_starship_charts(option):
    starships_df = pd.read_csv('csv/starships.csv')
    if option == 1:
        # Gráfico de Longitud de la nave
        starships_df['length'] = pd.to_numeric(starships_df['length'], errors='coerce')
        starships_df = starships_df.dropna(subset=['length'])
        starships_df = starships_df.sort_values(by='length', ascending=False)
        plt.figure(figsize=(12, 8))
        plt.bar(starships_df['name'], starships_df['length'], color='skyblue')
        plt.title('Longitud de las Naves')
        plt.xlabel('Nave')
        plt.ylabel('Longitud')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    
    elif option == 2:
        # Gráfico de Capacidad de carga
        starships_df['cargo_capacity'] = pd.to_numeric(starships_df['cargo_capacity'], errors='coerce')
        starships_df = starships_df.dropna(subset=['cargo_capacity'])
        starships_df = starships_df.sort_values(by='cargo_capacity', ascending=False)
        plt.figure(figsize=(12, 8))
        plt.bar(starships_df['name'], starships_df['cargo_capacity'], color='skyblue')
        plt.title('Capacidad de Carga de las Naves')
        plt.xlabel('Nave')
        plt.ylabel('Capacidad de Carga')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    elif option == 3:
        # Gráfico de Clasificación de hiperimpulsor
        starships_df['hyperdrive_rating'] = pd.to_numeric(starships_df['hyperdrive_rating'], errors='coerce')
        starships_df = starships_df.dropna(subset=['hyperdrive_rating'])
        starships_df = starships_df.sort_values(by='hyperdrive_rating', ascending=False)
        plt.figure(figsize=(12, 8))
        plt.bar(starships_df['name'], starships_df['hyperdrive_rating'], color='skyblue')
        plt.title('Clasificación de Hiperimpulsor de las Naves')
        plt.xlabel('Nave')
        plt.ylabel('Clasificación de Hiperimpulsor')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    elif option == 4:
        # Gráfico de MGLT (Modern Galactic Light Time)
        starships_df['MGLT'] = pd.to_numeric(starships_df['MGLT'], errors='coerce')
        starships_df = starships_df.dropna(subset=['MGLT'])
        starships_df = starships_df.sort_values(by='MGLT', ascending=False)
        plt.figure(figsize=(12, 8))
        plt.bar(starships_df['name'], starships_df['MGLT'], color='skyblue')
        plt.title('MGLT de las Naves')
        plt.xlabel('Nave')
        plt.ylabel('MGLT')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    else:
        print("Opción no válida.")

# Calcuylos estadisticos sobre las características de la nave. Fuentes de autoaprendizaje: (https://youtu.be/_vPO2hoQedM?si=Hf4TfZFA4bZxLiDv, https://youtu.be/TqfnmNUSjRs?si=b7kfjPb0G8TfFCWV, https://youtu.be/zC4ogU9zXoo?si=vrfH-uCpWZIJfJYF, https://youtu.be/kwIfw4AmeE0?si=3d9UoAKCAF56Ipa1)
def statistics_for_starship():
    starships_df = pd.read_csv('csv/starships.csv')

# Calcula la media de la velocidad de la nave
    starships_df['hyperdrive_rating'] = pd.to_numeric(starships_df['hyperdrive_rating'], errors='coerce')
    starships_df['MGLT'] = pd.to_numeric(starships_df['MGLT'], errors='coerce')
    starships_df['max_atmosphering_speed'] = pd.to_numeric(starships_df['max_atmosphering_speed'], errors='coerce')
    starships_df['cost_in_credits'] = pd.to_numeric(starships_df['cost_in_credits'], errors='coerce')

    # Calcular y mostrar estadísticas básicas
    print("Clasificación de Hiperimpulsor:")
    print("Promedio:", starships_df['hyperdrive_rating'].mean())
    print("Moda:", starships_df['hyperdrive_rating'].mode()[0])
    print("Máximo:", starships_df['hyperdrive_rating'].max())
    print("Mínimo:", starships_df['hyperdrive_rating'].min())

    print("\nMGLT:")
    print("Promedio:", starships_df['MGLT'].mean())
    print("Moda:", starships_df['MGLT'].mode()[0])
    print("Máximo:", starships_df['MGLT'].max())
    print("Mínimo:", starships_df['MGLT'].min())

    print("\nVelocidad Máxima en Atmósfera:")
    print("Promedio:", starships_df['max_atmosphering_speed'].mean())
    print("Moda:", starships_df['max_atmosphering_speed'].mode()[0])
    print("Máximo:", starships_df['max_atmosphering_speed'].max())
    print("Mínimo:", starships_df['max_atmosphering_speed'].min())

    print("\nCosto (en créditos):")
    print("Promedio:", starships_df['cost_in_credits'].mean())
    print("Moda:", starships_df['cost_in_credits'].mode()[0])
    print("Máximo:", starships_df['cost_in_credits'].max())
    print("Mínimo:", starships_df['cost_in_credits'].min())

#Función para mostrar las opciones de personajes, planetas, armas  y naves para que un usuario cree la clase
def mostrar_opciones(lista, tipo):
    print(f"\nOpciones de {tipo}:")
    for idx, item in enumerate(lista):
        print(f"{idx + 1}. {item}")
    print("Escriba 'fin' para terminar la selección.")
    seleccion = input(f"Seleccione el número correspondiente al {tipo} que desea: ")
    while not( seleccion=="fin" or seleccion.isnumeric()):
        seleccion = input(f"Error. Seleccione el número correspondiente al {tipo} que desea: ")
    if seleccion.lower() == 'fin':
        return 'fin'
    else:
        try:
            return lista[int(seleccion) - 1]
        except (IndexError, ValueError):
            print("Selección inválida. Intente nuevamente.")
            return mostrar_opciones(lista, tipo)

#Función para crear misión
def crear_mision(planetas, naves, armas, personajes):
    nombre = input("Ingrese el nombre de la misión: ")

    # Mostrar opciones de planetas
    planeta_destino = mostrar_opciones(planetas, "planeta destino")

    # Mostrar opciones de naves
    nave = mostrar_opciones(naves, "nave a utilizar")

    # Seleccionar armas
    seleccion_arma = []
    print("Ingrese hasta 7 armas (Escriba 'fin' para terminar):")
    while len(seleccion_arma) < 7:
        arma = mostrar_opciones(armas, "arma")
        if arma == 'fin':
            break
        seleccion_arma.append(arma)

    # Seleccionar integrantes
    seleccion_integrante = []
    print("Ingrese hasta 7 integrantes (Escriba 'fin' para terminar):")
    while len(seleccion_integrante) < 7:
        integrante = mostrar_opciones(personajes, "integrante")
        if integrante == 'fin':
            break
        seleccion_integrante.append(integrante)

    return Mision(nombre, planeta_destino, nave, seleccion_arma, seleccion_integrante)

#Función modificar misión
def modificar_mision(mision, planetas, naves, armas, personajes):
    print("\nModificar misión:")
    nuevo_nombre = input(f"Nombre actual: {mision.nombre}. Ingrese nuevo nombre o deje en blanco para mantener: ")
    
    modificar_planeta = input("Modificar planeta? (s/n): ").lower()
    while not(modificar_planeta.isalpha() and (modificar_planeta == 's' or modificar_planeta == 'n')):
        modificar_planeta = input("Opción no valida. Modificar planeta? (s/n): ").lower()
    if modificar_planeta == 's':
        nuevo_planeta = mostrar_opciones(planetas, "planeta destino")
    else:
        nuevo_planeta = None
    
    modificar_nave = input("Modificar nave? (s/n): ").lower()
    while not(modificar_nave.isalpha() and (modificar_nave == 's' or modificar_nave == 'n')):
        modificar_nave = input("Opción no valida. Modificar nave? (s/n): ").lower()
    if modificar_nave == 's':
        nueva_nave = mostrar_opciones(naves, "nave a utilizar")
    else:
        nueva_nave = None

    nuevas_armas = []
    modificar_armas = input("Modificar armas? (s/n): ").lower()
    while not(modificar_armas.isalpha() and (modificar_armas == 's' or modificar_armas == 'n')):
        modificar_armas = input("Opción no valida. Modificar armas? (s/n): ").lower()
    if modificar_armas == 's':
        print("Modificar armas (Escriba 'fin' para terminar o deje en blanco para mantener):")
        while len(nuevas_armas) < 7:
            arma = mostrar_opciones(armas, "arma")
            if arma == 'fin':
                break
            nuevas_armas.append(arma)

    nuevos_integrantes = []
    modificar_integrantes = input("Modificar integrantes? (s/n): ").lower()
    while not(modificar_integrantes.isalpha() and (modificar_integrantes == 's' or modificar_integrantes == 'n')):
        modificar_integrantes = input("Opción no valida. Modificar integrantes? (s/n): ").lower()
    if modificar_integrantes == 's':
        print("Modificar integrantes (Escriba 'fin' para terminar o deje en blanco para mantener):")
        while len(nuevos_integrantes) < 7:
            integrante = mostrar_opciones(personajes, "integrante")
            if integrante == 'fin':
                break
            nuevos_integrantes.append(integrante)

    mision.modificar_mision(
        nuevo_nombre=nuevo_nombre if nuevo_nombre else None,
        nuevo_planeta=nuevo_planeta if nuevo_planeta else None,
        nueva_nave=nueva_nave if nueva_nave else None,
        nuevas_armas=nuevas_armas if nuevas_armas else None,
        nuevos_integrantes=nuevos_integrantes if nuevos_integrantes else None
    )

#Función visualizacion de las misiones
def visualizar_misiones(misiones):
    for idx, mision in enumerate(misiones):
        print(f"\nMisión {idx + 1}:")
        mision.visualizar_mision()

#Funcion para guardar las misiones en nuestro archivo .txt, usando la función open()
def guardar_misiones(misiones, archivo):
    with open(archivo, 'w') as file:
        for mision in misiones:
            mision.guardar_mision(archivo)

#Función para cargar las misiones
def cargar_misiones(archivo):
    return Mision.cargar_misiones(archivo)