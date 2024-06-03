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
    velocidades_angulares = []

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

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidades_angulares_{i}.txt', 'r') as f:
            for linea in f:
                    valor = linea.strip()
                    velocidades_angulares.append(float(valor))    


    # Calculo de energia cinetica de traslacion
    velocidades_bici = np.square(velocidades_bici)

    producto_parcial = np.multiply(velocidades_bici,79)

    energia_cinetica_traslacion = np.multiply(producto_parcial,0.5)

    # Calculo de energia cinetica de rotacion
    radio = np.square(0.3683)

    momento_inercia = np.multiply(radio,1) # Masa de rueda estimada: 1kg, no es necesario hacerlo al ser 1

    velocidades_angulares = np.square(velocidades_angulares)

    producto_parcial = np.multiply(momento_inercia, velocidades_angulares)

    energia_cinetica_rotacion = np.multiply(producto_parcial,0.5)

    energia_cinetica_total = np.add(energia_cinetica_traslacion, energia_cinetica_rotacion)
    
    #Calculo de trabajo como variacion de la energia cinetica para cada caso
    trabajo_rotacion = calculate_work_deltaEc(energia_cinetica_rotacion)
    trabajo_traslacion = calculate_work_deltaEc(energia_cinetica_traslacion)
    trabajo_total = calculate_work_deltaEc(energia_cinetica_total)

    """
    posiciones_bici = np.diff(posiciones_bici)

    trabajo_fd = calculate_work_fd(fuerza_viscosa, posiciones_bici)
    """

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\energiaCinetica_traslacion_{i}.txt', "w") as file:
        for item in energia_cinetica_traslacion:
            file.write(f"{item.round(2)},")

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\energiaCinetica_rotacion_{i}.txt', "w") as file:
        for item in energia_cinetica_rotacion:
            file.write(f"{item.round(2)},")        
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\energiaCinetica_total_{i}.txt', "w") as file:
        for item in energia_cinetica_total:
            file.write(f"{item.round(2)},")

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_traslacion_{i}.txt', "w") as file:
        valor = energia_cinetica_traslacion[len(energia_cinetica_traslacion)-1] - energia_cinetica_traslacion[0]
        file.write(f"{valor.round(2)}")

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_rotacion_{i}.txt', "w") as file:
        valor = energia_cinetica_rotacion[len(energia_cinetica_rotacion)-1] - energia_cinetica_rotacion[0]
        file.write(f"{valor.round(2)}")

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_total_{i}.txt', "w") as file:
        valor = energia_cinetica_total[len(energia_cinetica_total)-1] - energia_cinetica_total[0]
        file.write(f"{valor.round(2)}")        

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_traslacion_instantaneo_{i}.txt', "w") as file:
        for item in trabajo_traslacion:
            file.write(f"{item.round(2)},") 

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_rotacion_instantaneo_{i}.txt', "w") as file:
        for item in trabajo_rotacion:
            file.write(f"{item.round(2)},")          
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_total_instantaneo_{i}.txt', "w") as file:
        for item in trabajo_total:
            file.write(f"{item.round(2)},") 

    """
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_fuerza_distancia_{i}.txt', "w") as file:
        for item in trabajo_fd:
            file.write(f"{item.round(2)},")
    """   

    #Calculo de potencia como variacion del trabajo con respecto al tiempo para cada caso
    potencia_traslacion = calculate_power(trabajo_traslacion,tiempo[2:])
    potencia_rotacion = calculate_power(trabajo_rotacion,tiempo[2:])
    potencia_total = calculate_power(trabajo_total,tiempo[2:])
    #potencia_fd = calculate_power(trabajo_fd,tiempo[2:])

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_traslacion_{i}.txt', "w") as file:
        for item in potencia_traslacion:
            file.write(f"{item.round(2)},") 

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_rotacion_{i}.txt', "w") as file:
        for item in potencia_rotacion:
            file.write(f"{item.round(2)},") 

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_total_{i}.txt', "w") as file:
        for item in potencia_total:
            file.write(f"{item.round(2)},") 
    """
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_fuerza_distancia_{i}.txt', "w") as file:
        for item in potencia_fd:
            file.write(f"{item.round(2)},") 
    """
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))

    # Gráfico 1
    plot_with_shades(axs[0, 0], tiempo[1:], energia_cinetica_rotacion, colors[0])
    axs[0, 0].set_title('Energía Cinética de Rotación')
    axs[0, 0].set_xlabel('Tiempo (s)')
    axs[0, 0].set_ylabel('$Ec_rot (J)$')
    axs[0, 0].grid(color='#2A3459')

    # Gráfico 2
    plot_with_shades(axs[0, 1], tiempo[2:], trabajo_rotacion, colors[1])
    axs[0, 1].set_title('Trabajo de Rotación')
    axs[0, 1].set_xlabel('Tiempo (s)')
    axs[0, 1].set_ylabel('$W_rot (J)$')
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_ylim([min(trabajo_rotacion)-0.01, max(trabajo_rotacion)+0.01])

    # Gráfico 3
    plot_with_shades(axs[0, 2], tiempo[3:], potencia_rotacion, colors[2])
    axs[0, 2].set_title('Potencia de Rotación')
    axs[0, 2].set_xlabel('Tiempo (s)')
    axs[0, 2].set_ylabel('$P_rot (Watt)$')
    axs[0, 2].grid(color='#2A3459')

    # Gráfico 4
    plot_with_shades(axs[1, 0], tiempo[1:], energia_cinetica_traslacion, colors[3])
    axs[1, 0].set_title('Energía Cinética de Traslación')
    axs[1, 0].set_xlabel('Tiempo (s)')
    axs[1, 0].set_ylabel('$Ec_tras (J)$')
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(tiempo[1:]), max(tiempo[1:])])
    axs[1, 0].set_ylim([min(energia_cinetica_traslacion), max(energia_cinetica_traslacion)])

    # Gráfico 5
    plot_with_shades(axs[1, 1], tiempo[2:], trabajo_traslacion, colors[4])
    axs[1, 1].set_title('Trabajo de Traslación')
    axs[1, 1].set_xlabel('Tiempo (s)')
    axs[1, 1].set_ylabel('$W_tras (J)$')
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(tiempo[2:]), max(tiempo[2:])])
    axs[1, 1].set_ylim([min(trabajo_traslacion), max(trabajo_traslacion)])

    # Gráfico 6
    plot_with_shades(axs[1, 2], tiempo[3:], potencia_traslacion, colors[5])
    axs[1, 2].set_title('Potencia de Traslación')
    axs[1, 2].set_xlabel('Tiempo (s)')
    axs[1, 2].set_ylabel('$P_tras (Watt)$')
    axs[1, 2].grid(color='#2A3459')
    axs[1, 2].set_xlim([min(tiempo[3:]), max(tiempo[3:])])
    axs[1, 2].set_ylim([min(potencia_traslacion), max(potencia_traslacion)])

    # Gráfico 7
    plot_with_shades(axs[2, 0], tiempo[1:], energia_cinetica_total, colors[0])
    axs[2, 0].set_title('Energía Cinética Total')
    axs[2, 0].set_xlabel('Tiempo (s)')
    axs[2, 0].set_ylabel('$Ec_tot (J)$')
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_xlim([min(tiempo[1:]), max(tiempo[1:])])
    axs[2, 0].set_ylim([min(energia_cinetica_traslacion), max(energia_cinetica_traslacion)])

    # Gráfico 8
    plot_with_shades(axs[2, 1], tiempo[2:], trabajo_total, colors[1])
    axs[2, 1].set_title('Trabajo Total')
    axs[2, 1].set_xlabel('Tiempo (s)')
    axs[2, 1].set_ylabel('$W_tot (J)$')
    axs[2, 1].grid(color='#2A3459')
    axs[2, 1].set_xlim([min(tiempo[2:]), max(tiempo[2:])])
    axs[2, 1].set_ylim([min(trabajo_total), max(trabajo_total)])

    # Gráfico 9
    plot_with_shades(axs[2, 2], tiempo[3:], potencia_total, colors[2])
    axs[2, 2].set_title('Potencia Total')
    axs[2, 2].set_xlabel('Tiempo (s)')
    axs[2, 2].set_ylabel('$P_tot (Watt)$')
    axs[2, 2].grid(color='#2A3459')
    axs[2, 2].set_xlim([min(tiempo[3:]), max(tiempo[3:])])
    axs[2, 2].set_ylim([min(potencia_total), max(potencia_total)])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.7)
    plt.show()
