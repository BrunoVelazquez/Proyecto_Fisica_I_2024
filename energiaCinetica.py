import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import savgol_filter
import pandas as pd
from utils import plot_with_shades, colors

def calculate_work_deltaEc(energia_cinetica):
    return np.diff(energia_cinetica)

def calculate_power(trabajo, tiempo):
    return np.diff(trabajo)/np.diff(tiempo)

for i in range(1, 6):
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici\\datos_bici_video_{i}.csv')
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv')
    velocidades_bici = df_bici['velocidad']
    posiciones_bici = df_bici['posicion']
    fuerza_viscosa = df_bici['fuerza_viscosa']
    tiempo = df_bici['tiempo']
    velocidades_angulares = df_marca['velocidad_angular']

    # Calculo de energia cinetica de bicicleta
    velocidades_bici = np.square(velocidades_bici)

    producto_parcial = np.multiply(velocidades_bici,79-2)

    energia_cinetica_bici = np.multiply(producto_parcial,0.5)

    # Calculo de energia cinetica de ruedas

    # Calculo de energia cinetica de traslacion de rueda
    producto_parcial_2 = np.multiply(velocidades_bici,1)

    energia_cinetica_traslacion = np.multiply(producto_parcial_2,0.5)

    # Calculo de energia cinetica de rotacion
    radio = np.square(0.3683)

    momento_inercia = np.multiply(radio,1) # Masa de rueda estimada: 1kg, no es necesario hacerlo al ser 1

    velocidades_angulares = np.square(velocidades_angulares)

    producto_parcial_3 = np.multiply(momento_inercia, velocidades_angulares)

    energia_cinetica_rotacion = np.multiply(producto_parcial_3,0.5)

    energia_cinetica_rueda = np.add(energia_cinetica_rotacion, energia_cinetica_traslacion)
    #La bicicleta tiene dos ruedas por lo tanto tiene el doble de energia cinetica 
   
    energia_cinetica_rueda = np.add(energia_cinetica_rueda,energia_cinetica_rueda)

    energia_cinetica_total = np.add(energia_cinetica_bici, energia_cinetica_rueda)

    #Calculo de trabajo como variacion de la energia cinetica para cada caso
    trabajo_rueda = calculate_work_deltaEc(energia_cinetica_rueda[::4])
    trabajo_bici = calculate_work_deltaEc(energia_cinetica_bici)
    trabajo_total = calculate_work_deltaEc(energia_cinetica_total)

    trabajo_total = savgol_filter(trabajo_total,len(trabajo_total),3)
    trabajo_rueda = savgol_filter(trabajo_rueda,len(trabajo_rueda),3)

    """
    posiciones_bici = np.diff(posiciones_bici)

    trabajo_fd = calculate_work_fd(fuerza_viscosa, posiciones_bici)
    """

    with open(f'Energia\\Datos_Video_{i}\\energiaCinetica_bici_{i}.txt', "w") as file:
        for item in energia_cinetica_bici:
            file.write(f"{item.round(2)},")

    with open(f'Energia\\Datos_Video_{i}\\energiaCinetica_ruedas_{i}.txt', "w") as file:
        for item in energia_cinetica_rueda:
            file.write(f"{item.round(2)},")        
    
    with open(f'Energia\\Datos_Video_{i}\\energiaCinetica_total_{i}.txt', "w") as file:
        for item in energia_cinetica_total:
            file.write(f"{item.round(2)},")

    with open(f'Energia\\Datos_Video_{i}\\trabajo_bici_{i}.txt', "w") as file:
        valor = energia_cinetica_traslacion[len(energia_cinetica_bici)-1] - energia_cinetica_bici[0]
        file.write(f"{valor.round(2)}")

    with open(f'Energia\\Datos_Video_{i}\\trabajo_rueda_{i}.txt', "w") as file:
        valor = energia_cinetica_rotacion[len(energia_cinetica_rueda)-1] - energia_cinetica_rueda[0]
        file.write(f"{valor.round(2)}")

    with open(f'Energia\\Datos_Video_{i}\\trabajo_total_{i}.txt', "w") as file:
        valor = energia_cinetica_total[len(energia_cinetica_total)-1] - energia_cinetica_total[0]
        file.write(f"{valor.round(2)}")        

    with open(f'Energia\\Datos_Video_{i}\\trabajo_bici_instantaneo_{i}.txt', "w") as file:
        for item in trabajo_bici:
            file.write(f"{item.round(2)},") 

    with open(f'Energia\\Datos_Video_{i}\\trabajo_rueda_{i}.txt', "w") as file:
        for item in trabajo_rueda:
            file.write(f"{item.round(2)},")          
    
    with open(f'Energia\\Datos_Video_{i}\\trabajo_total_instantaneo_{i}.txt', "w") as file:
        for item in trabajo_total:
            file.write(f"{item.round(2)},") 

    """
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\trabajo_fuerza_distancia_{i}.txt', "w") as file:
        for item in trabajo_fd:
            file.write(f"{item.round(2)},")
    """   

    #Calculo de potencia como variacion del trabajo con respecto al tiempo para cada caso
    potencia_bici = calculate_power(trabajo_bici,tiempo[2:])
    
    tiempo_2 = tiempo[::4]

    potencia_rueda = calculate_power(trabajo_rueda,tiempo_2[1:])
    potencia_total = calculate_power(trabajo_total,tiempo[2:])
    #potencia_fd = calculate_power(trabajo_fd,tiempo[2:])

    with open(f'Energia\\Datos_Video_{i}\\potencia_bici_{i}.txt', "w") as file:
        for item in potencia_bici:
            file.write(f"{item.round(2)},") 

    with open(f'Energia\\Datos_Video_{i}\\potencia_rueda_{i}.txt', "w") as file:
        for item in potencia_rueda:
            file.write(f"{item.round(2)},") 

    with open(f'Energia\\Datos_Video_{i}\\potencia_total_{i}.txt', "w") as file:
        for item in potencia_total:
            file.write(f"{item.round(2)},") 
    """
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\potencia_fuerza_distancia_{i}.txt', "w") as file:
        for item in potencia_fd:
            file.write(f"{item.round(2)},") 
    """
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))

    # Gráfico 1
    plot_with_shades(axs[0, 0], tiempo[1:], energia_cinetica_rueda, colors[0])
    axs[0, 0].set_title('Energía Cinética de Ruedas')
    axs[0, 0].set_xlabel('Tiempo (s)')
    axs[0, 0].set_ylabel('$Ec_ruedas (J)$')
    axs[0, 0].grid(color='#2A3459')

    tiempo_3 = tiempo[::4]
    # Gráfico 2
    plot_with_shades(axs[0, 1], tiempo_3[1:], trabajo_rueda, colors[1])
    axs[0, 1].set_title('Trabajo de Ruedas')
    axs[0, 1].set_xlabel('Tiempo (s)')
    axs[0, 1].set_ylabel('$W_ruedas (J)$')
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_ylim([min(trabajo_rueda)-0.01, max(trabajo_rueda)+0.01])

    # Gráfico 3
    plot_with_shades(axs[0, 2], tiempo_2[2:], potencia_rueda, colors[2])
    axs[0, 2].set_title('Potencia de Ruedas')
    axs[0, 2].set_xlabel('Tiempo (s)')
    axs[0, 2].set_ylabel('$P_ruedas (Watt)$')
    axs[0, 2].grid(color='#2A3459')

    # Gráfico 4
    plot_with_shades(axs[1, 0], tiempo[1:], energia_cinetica_bici, colors[3])
    axs[1, 0].set_title('Energía Cinética de Bici')
    axs[1, 0].set_xlabel('Tiempo (s)')
    axs[1, 0].set_ylabel('$Ec_bici (J)$')
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(tiempo[1:]), max(tiempo[1:])])
    axs[1, 0].set_ylim([min(energia_cinetica_bici), max(energia_cinetica_bici)])

    # Gráfico 5
    plot_with_shades(axs[1, 1], tiempo[2:], trabajo_bici, colors[4])
    axs[1, 1].set_title('Trabajo de Bici')
    axs[1, 1].set_xlabel('Tiempo (s)')
    axs[1, 1].set_ylabel('$W_bici (J)$')
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(tiempo[2:]), max(tiempo[2:])])
    axs[1, 1].set_ylim([min(trabajo_bici), max(trabajo_bici)])

    # Gráfico 6
    plot_with_shades(axs[1, 2], tiempo[3:], potencia_bici, colors[5])
    axs[1, 2].set_title('Potencia de Bici')
    axs[1, 2].set_xlabel('Tiempo (s)')
    axs[1, 2].set_ylabel('$P_bici (Watt)$')
    axs[1, 2].grid(color='#2A3459')
    axs[1, 2].set_xlim([min(tiempo[3:]), max(tiempo[3:])])
    axs[1, 2].set_ylim([min(potencia_bici), max(potencia_bici)])

    # Gráfico 7
    plot_with_shades(axs[2, 0], tiempo[1:], energia_cinetica_total, colors[0])
    axs[2, 0].set_title('Energía Cinética Total')
    axs[2, 0].set_xlabel('Tiempo (s)')
    axs[2, 0].set_ylabel('$Ec_tot (J)$')
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_xlim([min(tiempo[1:]), max(tiempo[1:])])
    axs[2, 0].set_ylim([min(energia_cinetica_total), max(energia_cinetica_total)])

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
