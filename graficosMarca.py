import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from scipy.signal import savgol_filter


# Configuración del estilo
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#FF073A',
    '#FFE4C4',
]

# Función para aplicar el efecto de sombreado
def plot_with_shades(ax, x, y, color):
    n_shades = 5
    diff_linewidth = 0.5
    alpha_value = 0.3 / n_shades
    for n in range(1, n_shades + 1):
        ax.plot(x, y,
                linewidth=1 + (diff_linewidth * n),
                alpha=alpha_value,
                color=color)
    ax.plot(x, y, marker='', color=color, linewidth=1)
    min_value = min(0,min(y))
    ax.fill_between(x, y, y2=[min_value]*len(x), color=color, alpha=0.1)


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

    plot_with_shades(axs[0,0], t, x, colors[0])
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')

    plot_with_shades(axs[0,1], t, y, colors[1])
    axs[0, 1].set_xlabel('tiempo (s)')
    axs[0, 1].set_ylabel('$y (m)$')
    axs[0, 1].grid(True)
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_xlim([min(t), max(t)])
    axs[0, 1].set_ylim([min(y), max(y)])

    plot_with_shades(axs[1,0], t, vx, colors[2])
    axs[1, 0].set_xlabel('tiempo (s)')
    axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')

    plot_with_shades(axs[1,1], t, vy, colors[3])
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')

    plot_with_shades(axs[2,0], t, ax, colors[4])
    axs[2, 0].set_xlabel('tiempo (s)')
    axs[2, 0].set_ylabel('$a_{x} (m/s^2)$')
    axs[2, 0].grid(True)
    axs[2, 0].grid(color='#2A3459')

    plot_with_shades(axs[2,1], t, ay, colors[5])
    axs[2, 1].set_xlabel('tiempo (s)')
    axs[2, 1].set_ylabel('$a_{y} (m/s^2)$')
    axs[2, 1].grid(True)
    axs[2, 1].grid(color='#2A3459')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()