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
    potencia_entregada = np.multiply(torque,velocidades_angulares_plato[2:])

    df_potencia = pd.DataFrame({
        'potencia_entregada': potencia_entregada
    })
    df_potencia.to_csv(f'Potencia_Entregada\\potencia_entregada_{i}.csv', index=False)

    #fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    #plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(potencia_entregada)], potencia_entregada, 2)
    plt.title('Potencia entregada en función del tiempo', fontsize=16)
    plt.xlabel('Tiempo (s)', fontsize=14)
    plt.ylabel('Potencia entregada (Watt)', fontsize=14)
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(potencia_entregada)]), max(t[:len(potencia_entregada)])])
    plt.ylim([min(potencia_entregada)-3, max(potencia_entregada)+3])
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()
    plt.show()