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

def ajuste_x(t):
    return 2.65 * t - 0.35 * np.sin(8.46 * t + 7.75) + 3.01

def ajuste_y(t):
    return 0.28 * np.sin(9.01 * t - 3.58) + 4.45

def ajuste_vx(t):
    return 4.3 * np.exp(-0.18 * t) * np.sin(9.03 * t + 0.03) + (-0.31 * t + 3.5)

def ajuste_vy(t):
    return 3.5 * np.exp(-0.12 * t) * np.sin(9.03 * t - 2.01) + 0.1


# Función para aplicar el efecto de sombreado
def plot_with_shades(ax, x, y, color):
    ax.plot(x, y, marker='', color=color, linewidth=1)



for i in range(1, 2):
    t = []
    x = []
    y = []
    vx = []
    vy = []

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\datosRuedaX_{i}.txt', 'r') as f:
            for linea in f:
                partes = linea.split()
                t.append(float(partes[0].replace(',', '.')))

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionX_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            x = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionY_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            y = [float(numero.strip()) for numero in numeros]       

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadX_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            vx = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadY_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            vy = [float(numero.strip()) for numero in numeros]
   

    # Graficamos los datos
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    plot_with_shades(axs[0,0], t, x, colors[0])
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')

    plot_with_shades(axs[0,0], t, ajuste_x(np.array(t)), colors[4])
    axs[0, 0].set_xlabel('tiempo (s)')
    axs[0, 0].set_ylabel('$x (m)$')
    axs[0, 0].grid(True)
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(t), max(t)])
    axs[0, 0].set_ylim([min(x), max(x)])

    print(y)

    plot_with_shades(axs[0,1], t, y, colors[5])
    axs[0, 1].set_xlabel('tiempo (s)')
    axs[0, 1].set_ylabel('$y (m)$')
    axs[0, 1].grid(True)
    axs[0, 1].grid(color='#2A3459')

    plot_with_shades(axs[0,1], t, ajuste_y(np.array(t)), colors[4])
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

    plot_with_shades(axs[1,0], t, ajuste_vx(np.array(t)), colors[4])
    axs[1, 0].set_xlabel('tiempo (s)')
    axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(t), max(t)])
    axs[1, 0].set_ylim([min(vx), max(vx)])

    plot_with_shades(axs[1,1], t, vy, colors[3])
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')

    plot_with_shades(axs[1,1], t, ajuste_vy(np.array(t)), colors[4])
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(t), max(t)])
    axs[1, 1].set_ylim([min(vy), max(vy)])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()