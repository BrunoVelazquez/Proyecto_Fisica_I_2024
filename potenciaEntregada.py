import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pandas as pd

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
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca/datos_marca_video_{i}.csv')
    torque = []
    velocidad_angular = df_marca['velocidad_angular'].to_numpy()
    t = df_bici['tiempo']

    # Abrir el archivo en modo lectura
    with open(f'Torque\\torque_{i}.txt', 'r') as file:
        for line in file:
            valores_linea = line.split()
             # Convertir cada valor a tipo float y agregarlo a la lista
            for valor in valores_linea:
                torque.append(float(valor))

    # Calcular velocidad angular del plato con la relación de transmisión
    velocidades_angulares_plato = np.multiply(velocidad_angular, 20)
    velocidades_angulares_plato = np.divide(velocidades_angulares_plato, 44)

    torque = np.multiply(torque,-1)
    potencia_entregada = np.multiply(torque,velocidades_angulares_plato[2:])

    df_potencia = pd.DataFrame({
        'potencia_entregada': potencia_entregada
    })
    df_potencia.to_csv(f'Potencia_Entregada\\potencia_entregada_{i}.csv', index=False)

    #fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    #plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(potencia_entregada)], potencia_entregada, colors[2])
    plt.title('Potencia entregada en función del tiempo', fontsize=16)
    plt.xlabel('Tiempo (s)', fontsize=14)
    plt.ylabel('Potencia entregada (Watt)', fontsize=14)
    plt.grid(color='#2A3459')
    plt.xlim([min(t[:len(potencia_entregada)]), max(t[:len(potencia_entregada)])])
    plt.ylim([min(potencia_entregada)-3, max(potencia_entregada)+3])
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()
    plt.show()