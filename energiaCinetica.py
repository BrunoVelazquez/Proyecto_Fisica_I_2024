import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import savgol_filter

def calculate_work_fd(fuerza_viscosa, posiciones_bici):
    posiciones_bici = posiciones_bici[1:]
    return fuerza_viscosa * posiciones_bici

def calculate_work_deltaEc(energia_cinetica):
    return np.diff(energia_cinetica)

def calculate_power(trabajo, tiempo):
    return np.diff(trabajo)/np.diff(tiempo)

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

for i in range(1, 6):
    velociades_bici = []
    posiciones_bici = []
    fuerza_viscosa = []
    tiempo = []

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\velocidad_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        velocidades_bici = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\fuerza_viscosa_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        fuerza_viscosa = [float(numero.strip()) for numero in numeros]    
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\posicion_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        posiciones_bici = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\tiempo_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        tiempo = [float(numero.strip()) for numero in numeros]    

    velocidades_bici = np.square(velocidades_bici)

    producto_parcial = np.multiply(velocidades_bici,79)

    energia_cinetica = np.multiply(producto_parcial,0.5)

    trabajo_deltaEc = calculate_work_deltaEc(energia_cinetica)

    posiciones_bici = np.diff(posiciones_bici)

    trabajo_fd = calculate_work_fd(fuerza_viscosa, posiciones_bici)

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\energiaCinetica_{i}.txt', "w") as file:
        for item in energia_cinetica:
            file.write(f"{item.round(2)},")
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\variacion_energiaCinetica_{i}.txt', "w") as file:
        valor = energia_cinetica[len(energia_cinetica)-1] - energia_cinetica[0]
        file.write(f"{valor.round(2)}")

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_variacion_energiaCinetica_{i}.txt', "w") as file:
        for item in trabajo_deltaEc:
            file.write(f"{item.round(2)},") 
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_fuerza_distancia_{i}.txt', "w") as file:
        for item in trabajo_fd:
            file.write(f"{item.round(2)},")
       

    potencia_deltaEc = calculate_power(trabajo_deltaEc,tiempo[2:])
    potencia_fd = calculate_power(trabajo_fd,tiempo[2:])

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_variacion_energiaCinetica_{i}.txt', "w") as file:
        for item in potencia_deltaEc:
            file.write(f"{item.round(2)},") 
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_fuerza_distancia_{i}.txt', "w") as file:
        for item in potencia_fd:
            file.write(f"{item.round(2)},") 

    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    # Gráfico 1
    plot_with_shades(axs[0, 0], tiempo[1:], energia_cinetica, colors[0])
    axs[0, 0].set_title('Energía Cinética')
    axs[0, 0].set_xlabel('Tiempo (s)')
    axs[0, 0].set_ylabel('$Ec (J)$')
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(tiempo[1:]), max(tiempo[1:])])
    axs[0, 0].set_ylim([min(energia_cinetica), max(energia_cinetica)])

    # Gráfico 3
    plot_with_shades(axs[1, 0], tiempo[2:], trabajo_deltaEc, colors[1])
    axs[1, 0].set_title('Trabajo')
    axs[1, 0].set_xlabel('Tiempo (s)')
    axs[1, 0].set_ylabel('$W (J)$')
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(tiempo[2:]), max(tiempo[2:])])
    axs[1, 0].set_ylim([min(trabajo_deltaEc), max(trabajo_deltaEc)])

    # Gráfico 4
    plot_with_shades(axs[1, 1], tiempo[2:], trabajo_fd, colors[2])
    axs[1, 1].set_title('Trabajo')
    axs[1, 1].set_xlabel('Tiempo(s)')
    axs[1, 1].set_ylabel('$W (J)$')
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(tiempo[2:]), max(tiempo[2:])])
    axs[1, 1].set_ylim([min(trabajo_fd), max(trabajo_fd)])

    # Gráfico 5
    plot_with_shades(axs[2, 0], tiempo[3:], potencia_deltaEc, colors[3])
    axs[2, 0].set_title('Potencia')
    axs[2, 0].set_xlabel('Tiempo (s)')
    axs[2, 0].set_ylabel('$P (Watt)$')
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_xlim([min(tiempo[3:]), max(tiempo[3:])])
    axs[2, 0].set_ylim([min(potencia_deltaEc), max(potencia_deltaEc)])

     # Gráfico 6
    plot_with_shades(axs[2, 1], tiempo[3:], potencia_fd, colors[4])
    axs[2, 1].set_title('Potencia')
    axs[2, 1].set_xlabel('Tiempo (s)')
    axs[2, 1].set_ylabel('$P (Watt)$')
    axs[2, 1].grid(color='#2A3459')
    axs[2, 1].set_xlim([min(tiempo[3:]), max(tiempo[3:])])
    axs[2, 1].set_ylim([min(potencia_fd), max(potencia_fd)])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.7)
    plt.show()
