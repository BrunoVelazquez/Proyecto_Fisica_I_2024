import numpy as np
import matplotlib.pyplot as plt

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

# Iterar sobre los diferentes archivos de datos
for i in range(1, 6):
    t = []
    vx = []
    viscous_force = []
    velocidades_angulares = []
    velocidades_angulares_plato = []
    torque = []
    
    # Leer datos de velocidad y tiempo
    with open(f'Datos_Extraidos_Bici/Datos_Video_{i}/velocidad_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        vx = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Bici/Datos_Video_{i}/tiempo_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        t = [float(numero.strip()) for numero in numeros]

    # Leer datos de fuerza viscosa
    with open(f'Datos_Extraidos_Bici/Datos_Video_{i}/fuerza_viscosa_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        viscous_force = [float(numero.strip()) for numero in numeros]

    # Leer datos de velocidades angulares
    with open(f'Datos_Extraidos_Marca/Datos_Video_{i}/velocidades_angulares_{i}.txt', 'r') as f:
        for linea in f:
            valor = linea.strip()
            velocidades_angulares.append(float(valor))

    # Calcular velocidad angular del plato con la relación de transmisión
    velocidades_angulares_plato = np.multiply(velocidades_angulares, 20)
    velocidades_angulares_plato = np.divide(velocidades_angulares_plato, 44)

    # Calcular potencia disipada y torque
    potencia_disipada = np.multiply(viscous_force, vx[1:])
    torque = np.divide(potencia_disipada, velocidades_angulares_plato[1:])

    # Graficar torque en función del tiempo para cada video
    plt.figure(figsize=(8, 6))
    plot_with_shades(plt.gca(), t[:len(torque)], torque, colors[1])
    plt.title(f'Torque en función del tiempo - Video {i}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Torque (Nm)')
    plt.grid(color='#2A3459')
    plt.tight_layout()
    plt.show()