import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from utils import plot_with_shades
import pandas as pd

for i in range(1, 6):
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    posicion = df_bici['posicion']
    velocidad = df_bici['velocidad']
    t = df_bici['tiempo']

    with open(f'Energia\\Datos_Video_{i}\\trabajo_total_instantaneo_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')[:-1]
            variacion_energia_cinetica = [float(numero.strip()) for numero in numeros]

    variacion_posicion = np.diff(posicion)

    #Calculo de coeficiente viscoso con formula Variacion Energia Cinetica = -k * v * Variacion Posicion

    coeficiente_viscoso = np.divide(variacion_energia_cinetica,-1)
    coeficiente_viscoso = np.divide(coeficiente_viscoso,velocidad[1:])

    variacion_posicion = savgol_filter(variacion_posicion,len(variacion_posicion),3)
    coeficiente_viscoso = np.divide(coeficiente_viscoso, variacion_posicion)

    df_coeficiente_viscoso = pd.DataFrame({'coeficiente_viscoso': coeficiente_viscoso})
    df_coeficiente_viscoso.to_csv(f'Coeficiente_Viscoso\\k_{i}.csv', index=False)

    # Graficar coeficiente viscoso en función del tiempo para cada video
    
    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(coeficiente_viscoso)], coeficiente_viscoso, 3)
    plt.title(f'Coeficiente viscoso k en función del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Coeficiente Viscoso (Pa*s)')
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(coeficiente_viscoso)]), max(t[:len(coeficiente_viscoso)])])
    plt.ylim([min(coeficiente_viscoso)-3, max(coeficiente_viscoso)+3])
    plt.tight_layout()
    plt.show()