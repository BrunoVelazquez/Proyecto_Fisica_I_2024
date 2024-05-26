import numpy as np
import matplotlib.pyplot as plt
import cv2
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
    t = []
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []

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

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleracionX_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            ax = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleracionY_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            ay = [float(numero.strip()) for numero in numeros]               

   
    
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

    plot_with_shades(axs[1,0], t[1:], vx, colors[2])
    axs[1, 0].set_xlabel('tiempo (s)')
    axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    axs[1, 0].grid(True)
    axs[1, 0].grid(color='#2A3459')

    plot_with_shades(axs[1,1], t[1:], vy, colors[3])
    axs[1, 1].set_xlabel('tiempo (s)')
    axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    axs[1, 1].grid(True)
    axs[1, 1].grid(color='#2A3459')

    plot_with_shades(axs[2,0], t[2:], ax, colors[4])
    axs[2, 0].set_xlabel('tiempo (s)')
    axs[2, 0].set_ylabel('$a_{x} (m/s^2)$')
    axs[2, 0].grid(True)
    axs[2, 0].grid(color='#2A3459')

    plot_with_shades(axs[2,1], t[2:], ay, colors[5])
    axs[2, 1].set_xlabel('tiempo (s)')
    axs[2, 1].set_ylabel('$a_{y} (m/s^2)$')
    axs[2, 1].grid(True)
    axs[2, 1].grid(color='#2A3459')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()