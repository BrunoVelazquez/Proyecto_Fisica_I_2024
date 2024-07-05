import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import plot_with_shades

# Iterar sobre los diferentes archivos de datos
for i in range(1, 6):
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca/datos_marca_video_{i}.csv')
    t = df_bici['tiempo']
    vx = df_bici['velocidad']
    viscous_force = df_bici['fuerza_viscosa']
    velocidades_angulares = df_marca['velocidad_angular']
    velocidades_angulares_plato = []
    torque = []

    # Calcular velocidad angular del plato con la relación de transmisión
    velocidades_angulares_plato = np.multiply(velocidades_angulares, 20)
    velocidades_angulares_plato = np.divide(velocidades_angulares_plato, 44)

    # Calcular potencia disipada y torque
    potencia_disipada = np.multiply(viscous_force, vx[1:])
    torque = np.divide(potencia_disipada, velocidades_angulares_plato[1:])

    # Graficar torque en función del tiempo para cada video
    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(torque)], torque, 1)
    plt.title(f'Torque en función del tiempo - Video {i}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Torque (Nm)')
    plt.grid(color='#2A3459')
    plt.tight_layout()
    plt.show()