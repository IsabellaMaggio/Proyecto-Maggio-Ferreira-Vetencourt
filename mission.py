#Clase de las misiones
class Mision():
    def __init__(self, nombre, planeta_destino, nave, armas, integrantes):
        self.nombre = nombre
        self.planeta_destino = planeta_destino
        self.nave = nave
        self.armas = armas  
        self.integrantes = integrantes  

    #Funcion para modificar una misión 
    def modificar_mision(self, nuevo_nombre=None, nuevo_planeta=None, nueva_nave=None, nuevas_armas=None, nuevos_integrantes=None):
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nuevo_planeta:
            self.planeta_destino = nuevo_planeta
        if nueva_nave:
            self.nave = nueva_nave
        if nuevas_armas:
            self.armas = nuevas_armas[:7]  # Limitar a 7 armas
        if nuevos_integrantes:
            self.integrantes = nuevos_integrantes[:7]  # Limitar a 7 integrantes
    #Función para visualizar una mision
    def visualizar_mision(self):
        print(f"\nNombre de la misión: {self.nombre}")
        print(f"Planeta destino: {self.planeta_destino}")
        print(f"Nave: {self.nave}")
        print("Armas:", ", ".join(self.armas))
        print("Integrantes:", ", ".join(self.integrantes))
        print("\n")

    #Función para guardar una misión utilizando open()
    def guardar_mision(self, archivo):
        with open(archivo, 'a') as file:
            file.write(f"{self.nombre},{self.planeta_destino},{self.nave},{'|'.join(self.armas)},{'|'.join(self.integrantes)}\n")

    #Función para cargar una misión utilizando open()
    def cargar_misiones(archivo):
        misiones = []
        with open(archivo, 'r') as file:
            for linea in file:
                nombre, planeta_destino, nave, armas, integrantes = linea.strip().split(',')
                armas = armas.split('|')
                integrantes = integrantes.split('|')
                misiones.append(Mision(nombre, planeta_destino, nave, armas, integrantes))
        return misiones