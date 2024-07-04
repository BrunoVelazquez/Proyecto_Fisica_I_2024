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
    
    ax2 = savgol_filter(ax,len(ax),0)
    ay2 = savgol_filter(ay,11,4)
    
    # Graficamos los datos
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    plot_with_shades(axs[0,0], t, x, 0)
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')

    plot_with_shades(axs[0,1], t, y, 1)
    axs[0, 1].set_xlabel('tiempo (s)')
    axs[0, 1].set_ylabel('$y (m)$')
    axs[0, 1].grid(True)
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_xlim([min(t), max(t)])
    axs[0, 1].set_ylim([min(y), max(y)])

    plot_with_shades(axs[1,0], t, vx, 2)
    axs[1, 0].set_xlabel('tiempo (s)')
    axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')

    plot_with_shades(axs[1,1], t, vy, 3)
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')

    plot_with_shades(axs[2,0], t, ax2, 4)
    axs[2, 0].set_xlabel('tiempo (s)')
    axs[2, 0].set_ylabel('$a_{x} (m/s^2)$')
    axs[2, 0].grid(True)
    axs[2, 0].grid(color='#2A3459')

    plot_with_shades(axs[2,1], t, ay2, 5)
    axs[2, 1].set_xlabel('tiempo (s)')
    axs[2, 1].set_ylabel('$a_{y} (m/s^2)$')
    axs[2, 1].grid(True)
    axs[2, 1].grid(color='#2A3459')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()