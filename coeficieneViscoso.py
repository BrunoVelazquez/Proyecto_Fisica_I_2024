import numpy as np
import matplotlib.pyplot as plt
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
    variacion_energia_cinetica = []
    posicion = []
    velocidad = []
    variacion_posicion = []
    coeficiente_viscoso = []
    t = []

    with open(f'Datos_Extraidos_Bici/Datos_Video_{i}/tiempo_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        t = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_total_instantaneo_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            variacion_energia_cinetica = [float(numero.strip()) for numero in numeros]    

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\velocidad_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            velocidad = [float(numero.strip()) for numero in numeros]         

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\posicion_{i}.txt', 'r') as f:
            numeros = f.readline().split(',')
            posicion = [float(numero.strip()) for numero in numeros]      

    variacion_posicion = np.diff(posicion)

    #Calculo de coeficiente viscoso con formula Variacion Energia Cinetica = -k * v * Variacion Posicion

    coeficiente_viscoso = np.divide(variacion_energia_cinetica,-1)
    coeficiente_viscoso = np.divide(coeficiente_viscoso,velocidad[1:])

    variacion_posicion= savgol_filter(variacion_posicion,len(variacion_posicion),3)
    coeficiente_viscoso = np.divide(coeficiente_viscoso, variacion_posicion[1:])

    with open(f'Coeficiente_Viscoso\\k_{i}.txt', 'w') as f:
        f.write(f"{coeficiente_viscoso}\n")

    # Graficar coeficiente viscoso en función del tiempo para cada video


    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(coeficiente_viscoso)], coeficiente_viscoso, colors[3])
    plt.title(f'Coeficiente viscoso en función del tiempo - Video {i}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Coeficiente Viscoso (Pas)')
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(coeficiente_viscoso)]), max(t[:len(coeficiente_viscoso)])])
    plt.ylim([min(coeficiente_viscoso)-3, max(coeficiente_viscoso)+3])
    plt.tight_layout()
    plt.show()

    """
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    # Gráfico 1
    plot_with_shades(plt.gca(), t[:len(coeficiente_viscoso)], coeficiente_viscoso, colors[3])
    axs[0, 0].set_title('Coeficiente Viscoso')
    axs[0, 0].set_xlabel('Tiempo (s)')
    axs[0, 0].set_ylabel('Coeficiente Viscoso (Pas)')
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(t[:len(coeficiente_viscoso)]), max(t[:len(coeficiente_viscoso)])])
    axs[0, 0].set_ylim([min(coeficiente_viscoso)-3, max(coeficiente_viscoso)+3])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.7)
    plt.show()

    """