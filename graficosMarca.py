import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from scipy.signal import savgol_filter
from utils import plot_with_shades

for i in range(1, 6):
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv')
    t = df_marca['tiempo']
    x = df_marca['posicion_x']
    y = df_marca['posicion_y']
    vx = df_marca['velocidad_x']
    vy = df_marca['velocidad_y']
    ax = df_marca['aceleracion_x']
    ay = df_marca['aceleracion_y']           

    # Graficamos los datos
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    plot_with_shades(axs[0,0], t, x, 0)
    axs[0, 0].set_xlabel('tiempo (s)', fontsize=12)
    axs[0, 0].set_ylabel('$x (m)$', fontsize=12)
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_title('Posición en X', fontsize=14)

    plot_with_shades(axs[0,1], t, y, 1)
    axs[0, 1].set_xlabel('tiempo (s)', fontsize=12)
    axs[0, 1].set_ylabel('$y (m)$', fontsize=12)
    axs[0, 1].grid(True)
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_xlim([min(t), max(t)])
    axs[0, 1].set_ylim([min(y), max(y)])
    axs[0, 1].set_title('Posición en Y', fontsize=14)

    plot_with_shades(axs[1,0], t, vx, 2)
    axs[1, 0].set_xlabel('tiempo (s)', fontsize=12)
    axs[1, 0].set_ylabel('$v_{x} (m/s)$', fontsize=12)
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_title('Velocidad en X', fontsize=14)

    plot_with_shades(axs[1,1], t, vy, 3)
    axs[1, 1].set_xlabel('tiempo (s)', fontsize=12)
    axs[1, 1].set_ylabel('$v_{y} (m/s)$', fontsize=12)
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_title('Velocidad en Y', fontsize=14)

    plot_with_shades(axs[2,0], t, ax, 4)
    axs[2, 0].set_xlabel('tiempo (s)', fontsize=12)
    axs[2, 0].set_ylabel('$a_{x} (m/s^2)$', fontsize=12)
    axs[2, 0].grid(True)
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_title('Aceleración en X', fontsize=14)

    plot_with_shades(axs[2,1], t, ay, 5)
    axs[2, 1].set_xlabel('tiempo (s)', fontsize=12)
    axs[2, 1].set_ylabel('$a_{y} (m/s^2)$', fontsize=12)
    axs[2, 1].grid(True)
    axs[2, 1].grid(color='#2A3459')
    axs[2, 1].set_title('Aceleración en Y', fontsize=14)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()