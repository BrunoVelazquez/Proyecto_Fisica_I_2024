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
    velocidades_angulares = []
    aceleraciones_angulares = []

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\datosRuedaX_{i}.txt', 'r') as f:
            for linea in f:
                partes = linea.split()
                t.append(float(partes[0].replace(',', '.')))

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidades_angulares_{i}.txt', 'r') as f:
            for linea in f:
                    valor = linea.strip()
                    velocidades_angulares.append(float(valor))
            

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleraciones_angulares_{i}.txt', 'r') as f:
            for linea in f:
                    valor = linea.strip()
                    aceleraciones_angulares.append(float(valor))

   
    velocidad_angular_suavizada = savgol_filter(velocidades_angulares,len(velocidades_angulares),3)
    aceleracion_angular_suavizada = savgol_filter(aceleraciones_angulares,len(aceleraciones_angulares),3)

    fig, axs = plt.subplots(2, 1, figsize=(14, 10))
    # Gráfico 1
    plot_with_shades(axs[0], t[1:], velocidad_angular_suavizada, colors[1])
    axs[0].set_title('Velocidad Angular')
    axs[0].set_xlabel('Tiempo (s)')
    axs[0].set_ylabel('$ω (rad/s)$')
    axs[0].grid(color='#2A3459')
    axs[0].grid(True)

    # Gráfico 2
    plot_with_shades(axs[1], t[2:], aceleracion_angular_suavizada, colors[3])
    axs[1].set_title('Aceleración Angular')
    axs[1].set_xlabel('Tiempo(s)')
    axs[1].set_ylabel('$α (rad/s^2)$')
    axs[1].grid(color='#2A3459')
    axs[1].grid(True)

    # Ajustar espacios entre subplots
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.5)

    # Mostrar la figura
    plt.show()