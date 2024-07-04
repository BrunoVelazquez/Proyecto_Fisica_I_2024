import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from utils import fill
from scipy.signal import savgol_filter

def calculate_angular_aceleration(w_values, t_values):
    """
    Calcula la aceleración angular según la velocidad angular y los valores de tiempo.

    Parametros:
    w_values (array): Arreglo de valores de velocidad angular.
    t_values (array): Arreglos de valores de tiempo.

    Retorna:
    array: Valores de aceleración angular.
    """
    dw_dt = np.diff(w_values) / np.diff(t_values)

    return dw_dt.round(2)


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
    velocidades_angulares = df_marca['velocidad_angular']
    aceleraciones_angulares = df_marca['aceleracion_angular']

    max_length = max(len(t), len(velocidades_angulares), len(aceleraciones_angulares))
    velocidad_angular_suavizada = savgol_filter(velocidades_angulares,len(velocidades_angulares),3)
    aceleraciones_angulares = calculate_angular_aceleration(velocidad_angular_suavizada,t)
    aceleraciones_angulares = savgol_filter(aceleraciones_angulares,len(aceleraciones_angulares),3)
    aceleraciones_angulares = fill(aceleraciones_angulares, max_length)

    df_marca['velocidad_angular'] = velocidad_angular_suavizada
    df_marca['aceleracion_angular'] = aceleraciones_angulares
    
    df_marca.to_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv', index=False)
    fig, axs = plt.subplots(2, 1, figsize=(14, 10))
    # Gráfico 1
    plot_with_shades(axs[0], t, velocidad_angular_suavizada, colors[1])
    axs[0].set_title('Velocidad Angular')
    axs[0].set_xlabel('Tiempo (s)')
    axs[0].set_ylabel('$ω (rad/s)$')
    axs[0].grid(color='#2A3459')
    axs[0].grid(True)

    # Gráfico 2
    plot_with_shades(axs[1], t, aceleraciones_angulares, colors[3])
    axs[1].set_title('Aceleración Angular')
    axs[1].set_xlabel('Tiempo(s)')
    axs[1].set_ylabel('$α (rad/s^2)$')
    axs[1].grid(color='#2A3459')
    axs[1].grid(True)

    # Ajustar espacios entre subplots
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.5)

    # Mostrar la figura
    plt.show()