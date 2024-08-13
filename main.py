
import functions 
import pandas as pd

#Esta es nuestra función principal donde se ejecutan las funciones que se importan para poder hacer todo el proyecto
def main():

    print('Bienvenidos a Star Wars Metropedia ✨✨✨')
    print('\n')
    print("Cargando especies...")
    species = functions.load_species()
    print('Carga exitosa')
    print('\n')
    print("Cargando starships...")
    starships = functions.load_starships()
    print('Carga exitosa')
    print('\n')
    print("Cargando vehículos...")
    vehicles = functions.load_vehicles()
    print('Carga exitosa')
    print('\n')
    print("Cargando personajes...")
    characters = functions.load_characters(species, starships, vehicles)
    print('Carga exitosa')
    print('\n')
    print("Cargando planetas...")
    planets = functions.load_planets(characters)
    print('Carga exitosa')
    print('\n')

    misiones = []
    archivo_misiones = 'misiones.txt'
    exit = 1

    while exit != 0:

        #Menu inicial
        menu = input(
            "Porfavor seleccione una opcion: \n1.👁️ Lista de peliculas de la saga \n2.👁️ Lista de las especies de seres vivos de la saga \n3.👁️ Lista de planetas  \n4.👁️ Buscar personaje \n5.👁️ Gráfico de cantidad de personajes nacidos en cada planeta \n6.👁️ Gráficos de características de naves  \n7.👁️ Estadísticas sobre naves \n8.👁️ Misiones \n9. Salir \n ==> "
        )
        print('\n')
        while not (menu.isnumeric() and (0< int(menu) <= 9)):
            menu = input(
            "Error. Porfavor seleccione una opcion: \n1.👁️ Lista de peliculas de la saga \n2.👁️ Lista de las especies de seres vivos de la saga \n3.👁️ Lista de planetas  \n4.👁️ Buscar personaje \n5.👁️ Gráfico de cantidad de personajes nacidos en cada planeta \n6.👁️ Gráficos de características de naves  \n7.👁️ Estadísticas sobre naves \n8.👁️ Misiones \n9. Salir\n ==> "
            )

        menu = int(menu)

        #Opción para mostrar las películas
        if menu == 1:
            print('---A continuación se mostrará una lista de peliculas de la Saga---')
            movies = functions.get_movies()
            for movie in movies:
                print('-------------------------------------------------------')
                print(f"Título: {movie.title}\nEpisodio: {movie.episode_id} \nFecha de lanzamiento: {movie.release_date} \nDirector: {movie.director}")
                print(f"Opening crawl: {movie.opening_crawl}\n")
                print('-------------------------------------------------------')
                print('\n')
        #Opción para mostrar la lista de las especies de Seres Vivos de la Saga
        elif menu == 2:
            print('---A continuación se mostrará una lista de las especies de la Saga---')
            for specie in species.values():
                print('-------------------------------------------------------')
                print(f"Nombre: {specie.name}\nAltura: {specie.average_height} \nClasificación.: {specie.classification} \nNombre del planeta de origen:  {specie.homeworld} \nLengua materna: {specie.language} \nPersonajes: {specie.people} \nEpisodios: {specie.films}")
                print('-------------------------------------------------------')
                print('\n')
        #Opción para mostrar la lista de los planetas        
        elif menu == 3:
            for planet in planets.values():
                print(f"Nombre: {planet.name}")
                print(f"Período de órbita: {planet.orbital_period}")
                print(f"Período de rotación: {planet.rotation_period}")
                print(f"Cantidad de habitantes: {planet.population}")
                print(f"Tipo de clima: {planet.climate}")
                print(f"Episodios: {', '.join(planet.films)}")
                print(f"Residentes: {', '.join(planet.residents)}\n")
                print('\n')
        #Opción par a la busqueda de personajes
        elif menu == 4:
            name = input('Porfavor ingrese el nombre del personaje que quiere buscar: ')
            results = functions.search_character(characters, name)
            if results:
                for character in results:
                    print('-------------------------------------------------------')
                    print(f"Nombre: {character.name}")
                    print(f"Nombre del Planeta de origen: {character.homeworld}")
                    print(f"Títulos de los episodios: {', '.join(character.films)}")
                    print(f"Género: {character.gender}")
                    print(f"Especie: {character.species}")
                    print(f"Naves: {', '.join(character.starships) if isinstance(character.starships, list) else character.starships}")
                    print(f"Vehículos: {', '.join(character.vehicles) if isinstance(character.vehicles, list) else character.vehicles}")
                    print('-------------------------------------------------------')
                    print('\n')
            else:
                print("No se encontraron personajes que coincidan con la búsqueda.")
        #Opción para ver la gráfica de la cantidad de personajes nacidos en cada planeta
        elif menu == 5: 
            functions.graphic_planet_homeworld() 
        #Opción para ver graficas de las características de las naves
        elif menu == 6:
            exitMenu6 = 1 
            while exitMenu6 != 0:
                option = input("Seleccione una opción para comparar las naves \n1.Longitud \n2.Capacidad de carga \n3.Clasificación de hiperimpulsor \n4.MGLT \n5. Regresar al menú principal \n==> ")
                while not (option.isnumeric() and (0<int(option)<=5)):
                    option = input("Opción no valida. Seleccione una opción para comparar las naves \n1.Longitud \n2.Capacidad de carga \n3.Clasificación de hiperimpulsor \n4.MGLT \n==> ")
                option = int(option)
                print('\n')
                if(0< option <= 4):
                    functions.create_starship_charts(option) 
                else:
                    exitMenu6 = 0
        #Opción para ver las estadisticas de las naves
        elif menu == 7:
            functions.statistics_for_starship()


        #Opción para las misiones
        elif menu == 8:
            planets_df = pd.read_csv('csv/planets.csv')
            starships_df = pd.read_csv('csv/starships.csv')
            characters_df = pd.read_csv('csv/characters.csv')
            weapons_df = pd.read_csv('csv/weapons.csv')

            planetas = planets_df['name'].tolist()
            naves = starships_df['name'].tolist()
            personajes = characters_df['name'].tolist()
            armas = weapons_df['name'].tolist()
            exitMenu8 = 1
            while exitMenu8 != 0:
                option8 = input('Seleccione una opción: \n1.Crear Misión \n2.Modificar Misión \n3.Visualizar Misiones \n4.Guardar Misiones \n5.Cargar Misiones \n6.Volver al Menú Principal \n==>  ')
                while not (option8.isnumeric() and (0<int(option8)<=6)):
                    option8 = input('Opción Inválida. Seleccione una opción: \n1.Crear Misión \n2.Modificar Misión \n3.Visualizar Misiones \n4.Guardar Misiones \n5.Cargar Misiones \n6.Volver al Menú Principal \n==>  ')
                option8 = int(option8)
                if option8 == 1:
                    if len(misiones) < 5:
                        nueva_mision = functions.crear_mision(planetas, naves, armas, personajes)
                        misiones.append(nueva_mision)
                    else:
                        print("No se pueden crear más de 5 misiones.")
                elif option8 ==2: 
                    if misiones:
                        functions.visualizar_misiones(misiones)
                        seleccion = int(input("Seleccione el número de la misión que desea modificar: ")) - 1
                        if 0 <= seleccion < len(misiones):
                            functions.modificar_mision(misiones[seleccion], planetas, naves, armas, personajes)
                        else:
                            print("Selección inválida.")
                    else:
                        print("No hay misiones para modificar.")
                elif option8 == 3:
                    if len(misiones) > 0:
                        functions.visualizar_misiones(misiones)
                    else:
                        print("No hay misiones para visualizar.")                                        
                elif option8 == 4:
                    functions.guardar_misiones(misiones, archivo_misiones)
                    print("Misiones guardadas correctamente.")
                elif option8 == 5:
                    misiones = functions.cargar_misiones(archivo_misiones)
                    print("Misiones cargadas correctamente.")
                else:
                    exitMenu8 = 0                    
        # Opción de menú que nos permite salir y cerrar el programa 
        elif menu == 9:
            exit = 0

#Aqui hacemos el llamado a la función principal para poder correrla por la terminal
main()