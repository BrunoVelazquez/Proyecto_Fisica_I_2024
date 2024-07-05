import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pandas as pd
from utils import plot_with_shades

for i in range(1,6):
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca/datos_marca_video_{i}.csv')
    torque = pd.read_csv(f'Torque/torque_{i}.csv')['torque']
    velocidad_angular = df_marca['velocidad_angular'].to_numpy()
    t = df_bici['tiempo']

    # Calcular velocidad angular del plato con la relación de transmisión
    velocidades_angulares_plato = np.multiply(velocidad_angular, 20)
    velocidades_angulares_plato = np.divide(velocidades_angulares_plato, 44)

    torque = np.multiply(torque,-1)
    potencia_a_entregar = np.multiply(torque,velocidades_angulares_plato[2:])

    with open(f'Potencia_a_Entregar\\potencia_a_entregar_{i}.txt', "w") as file:
        for item in potencia_a_entregar:
            file.write(f"{round(item,2)}\n")

    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(potencia_a_entregar)], potencia_a_entregar, 2)
    plt.title(f'Potencia a entregar en función del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Potencia a entregar (Watt)')
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(potencia_a_entregar)]), max(t[:len(potencia_a_entregar)])])
    plt.ylim([min(potencia_a_entregar)-3, max(potencia_a_entregar)+3])
    plt.tight_layout()
    plt.show()