
#Función para mostrar las opciones de personajes, planetas, armas  y naves para que un usuario cree la clase
from mission import Mision
import matplotlib.pyplot as plt
import pandas as pd
# Gráfico de cantidad de personajes nacidos en cada planeta. Utilizamos pandas para leer el archivo .csv (https://youtu.be/_8onVOY2j4E?si=da5NtHjuFwfq604p, https://youtu.be/7WU3QixV_-s?si=PFO8BV7mt5sIucRQ)
def graphic_planet_homeworld():
    characters_df = pd.read_csv('csv\characters.csv')

    characters_by_homeworld = characters_df['homeworld'].value_counts()

    plt.figure(figsize=(10, 6))
    characters_by_homeworld.plot(kind='bar', color='skyblue')
    plt.title('Cantidad de personajes nacidos en cada planeta')
    plt.xlabel('Planeta')
    plt.ylabel('Cantidad de personajes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def mostrar_opciones(lista, tipo):
    print(f"\nOpciones de {tipo}:")
    for idx, item in enumerate(lista):
        print(f"{idx + 1}. {item}")
    print("Escriba 'fin' para terminar la selección.")
    seleccion = input(f"Seleccione el número correspondiente al {tipo} que desea: ")
    while not( seleccion.isnumeric()):
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