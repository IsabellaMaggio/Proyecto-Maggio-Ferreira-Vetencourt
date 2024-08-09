import pandas as pd
import matplotlib.pyplot as plt

#Función para graficar la relación de los planetas con las personas que han nacido ahí
def grahpic_planet_homeworld ():
    
    characters_df = pd.read_csv('csv/characters.csv')

    homeworld_counts = characters_df['homeworld'].value_counts()

    plt.figure(figsize=(10, 6))
    homeworld_counts.plot(kind='bar', color='skyblue')
    plt.title('Cantidad de personajes nacidos en cada planeta')
    plt.xlabel('Planeta')
    plt.ylabel('Cantidad de personajes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
