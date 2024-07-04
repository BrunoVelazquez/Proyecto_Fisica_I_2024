import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from scipy.signal import savgol_filter
from utils import plot_with_shades

def ajuste_x(t):
    return 2.65 * t - 0.35 * np.sin(8.46 * t + 7.75) + 3.01

def ajuste_y(t):
    return 0.28 * np.sin(9.01 * t - 3.58) + 4.45

def ajuste_vx(t):
    return 4.3 * np.exp(-0.18 * t) * np.sin(9.03 * t + 0.03) + (-0.31 * t + 3.5)

def ajuste_vy(t):
    return 3.5 * np.exp(-0.12 * t) * np.sin(9.03 * t - 2.01) + 0.1

for i in range(1, 2):
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv')
    t = df_marca['tiempo']
    x = df_marca['posicion_x']
    y = df_marca['posicion_y']
    vx = df_marca['velocidad_x']
    vy = df_marca['velocidad_y']

    # Graficamos los datos
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    plot_with_shades(axs[0,0], t, x, 0)
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')

    plot_with_shades(axs[0,0], t, ajuste_x(np.array(t)), 4)
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(t), max(t)])
    axs[0, 0].set_ylim([min(x), max(x)])

    plot_with_shades(axs[0,1], t, y, 5)
    axs[0, 1].set_xlabel('tiempo (s)')
    axs[0, 1].set_ylabel('$y (m)$')
    axs[0, 1].grid(True)
    axs[0, 1].grid(color='#2A3459')

    plot_with_shades(axs[0,1], t, ajuste_y(np.array(t)), 4)
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

    plot_with_shades(axs[1,0], t, ajuste_vx(np.array(t)), 4)
    axs[1, 0].set_xlabel('tiempo (s)')
    axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(t), max(t)])
    axs[1, 0].set_ylim([min(vx), max(vx)])

    plot_with_shades(axs[1,1], t, vy, 3)
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')

    plot_with_shades(axs[1,1], t, ajuste_vy(np.array(t)), 4)
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(t), max(t)])
    axs[1, 1].set_ylim([min(vy), max(vy)])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()