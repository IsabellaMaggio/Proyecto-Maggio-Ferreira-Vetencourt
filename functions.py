BASE_URL = "https://www.swapi.tech/api"
import requests

def get_all_data(variable):
    data = []
    url = f"{BASE_URL}/{variable}"
    while url:
        response = requests.get(url)
        result = response.json()
        data.extend(result['results'])
        url = result['next']
    return data


def find_species_for_character(character_url, species_data):
    for specie in species_data.values():
        if character_url in specie.people:
            return specie.name
    return ''

def find_vehicles_for_character(character_url, vehicles_data):
    vehicles = []
    for vehicle in vehicles_data.values():
        if character_url in vehicle.pilots:
            vehicles.append(vehicle.name)
    if len(vehicles) == 0:
        return 'No vehicles for this character'
    return vehicles