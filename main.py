def main():
    exit = 1

    while exit != 0:


        menu = input(
            "Porfavor seleccione una opcion: \n1.👁️ Lista de peliculas de la saga \n2.👁️ Lista de las especies de seres vivos de la saga \n3.👁️ Lista de planetas  \n4.👁️ Buscar personaje \n5.👁️ Gráfico de cantidad de personajes nacidos en cada planeta \n6.👁️ Gráficos de características de naves  \n7.👁️ Estadísticas sobre naves \n8.👁️ Misiones \n9. Salir \n ==> "
        )

        while not (menu.isnumeric() and (0< int(menu) <= 9)):
            menu = input(
            "Error. Porfavor seleccione una opcion: \n1.👁️ Lista de peliculas de la saga \n2.👁️ Lista de las especies de seres vivos de la saga \n3.👁️ Lista de planetas  \n4.👁️ Buscar personaje \n5.👁️ Gráfico de cantidad de personajes nacidos en cada planeta \n6.👁️ Gráficos de características de naves  \n7.👁️ Estadísticas sobre naves \n8.👁️ Misiones \n9. Salir\n ==> "
            )

        menu = int(menu)

        #Opción para mostrar las películas
        if menu == 1:
            print('---A continuación se mostrará una lista de peliculas de la Saga---')
            # movies = api.get_movies()
            for movie in movies:
                print('-------------------------------------------------------')
                print(f"Título: {movie.title}\nEpisodio: {movie.episode_id} \nFecha de lanzamiento: {movie.release_date} \nDirector: {movie.director}")
                print(f"Opening crawl: {movie.opening_crawl}\n")
                print('-------------------------------------------------------')
        #Opción para mostrar la lista de las especies de Seres Vivos de la Saga
        elif menu == 2:
            print('---A continuación se mostrará una lista de las especies de la Saga---')
            for specie in species.values():
                print('-------------------------------------------------------')
                print(f"Nombre: {specie.name}\nAltura: {specie.average_height} \nClasificación.: {specie.classification} \nNombre del planeta de origen:  {specie.homeworld} \nLengua materna: {specie.language} \nPersonajes: {specie.people} \nEpisodios: {specie.films}")
                print('-------------------------------------------------------')
        elif menu == 3:
            for planet in planets.values():
                print(f"Nombre: {planet.name}")
                print(f"Período de órbita: {planet.orbital_period}")
                print(f"Período de rotación: {planet.rotation_period}")
                print(f"Cantidad de habitantes: {planet.population}")
                print(f"Tipo de clima: {planet.climate}")
                print(f"Episodios: {', '.join(planet.films)}")
                print(f"Residentes: {', '.join(planet.residents)}\n")
        elif menu == 4:
            name = input('Porfavor ingrese el nombre del personaje que quiere buscar: ')
            results = api.search_character(characters, name)
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
            else:
                print("No se encontraron personajes que coincidan con la búsqueda.")
        elif menu == 5: 
            api.grahpic_planet_homeworld ()
        # Opción de menú que nos permite salir y cerrar el programa 
        elif menu == 9:
            exit = 0

#Aqui hacemos el llamado a la función principal para poder correrla por la terminal
main()