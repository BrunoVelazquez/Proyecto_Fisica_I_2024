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

# Lista para almacenar todos los valores de todas las iteraciones
todos_valores = []

for i in range(1,6):
    torque = []
    velocidad_angular = []
    t = []

    # Abrir el archivo en modo lectura
    with open(f'Torque\\torque_{i}.txt', 'r') as file:
        for line in file:
            valores_linea = line.split()
             # Convertir cada valor a tipo float y agregarlo a la lista
            for valor in valores_linea:
                torque.append(float(valor))

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidades_angulares_{i}.txt', 'r') as f:
            for linea in f:
                    valor = linea.strip()
                    velocidad_angular.append(float(valor))

    with open(f'Datos_Extraidos_Bici/Datos_Video_{i}/tiempo_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        t = [float(numero.strip()) for numero in numeros]

    # Calcular velocidad angular del plato con la relación de transmisión
    velocidades_angulares_plato = np.multiply(velocidad_angular, 20)
    velocidades_angulares_plato = np.divide(velocidades_angulares_plato, 44)

    torque = np.multiply(torque,-1)
    potencia_a_entregar = np.multiply(torque,velocidades_angulares_plato[1:])

    with open(f'Potencia_a_Entregar\\potencia_a_entregar_{i}.txt', "w") as file:
        for item in potencia_a_entregar:
            file.write(f"{item.round(2)}\n")

    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(potencia_a_entregar)], potencia_a_entregar, colors[2])
    plt.title(f'Potencia a entregar en función del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Potencia a entregar (Watt)')
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(potencia_a_entregar)]), max(t[:len(potencia_a_entregar)])])
    plt.ylim([min(potencia_a_entregar)-3, max(potencia_a_entregar)+3])
    plt.tight_layout()
    plt.show()        