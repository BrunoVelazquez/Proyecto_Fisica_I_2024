import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import savgol_filter


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

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    # Gráfico 1
    axs[0, 0].plot(t[1:], velocidades_angulares, color='b', linestyle='-', linewidth=1)
    axs[0, 0].set_title('Velocidades Angulares', fontsize=14)
    axs[0, 0].set_xlabel('Tiempo', fontsize=12)
    axs[0, 0].set_ylabel('$ω$', fontsize=12)
    axs[0, 0].grid(True)

    # Gráfico 2
    axs[0, 1].plot(t[2:], aceleraciones_angulares, color='r', linestyle='-', linewidth=1)
    axs[0, 1].set_title('Aceleraciones Angulares', fontsize=14)
    axs[0, 1].set_xlabel('Tiempo', fontsize=12)
    axs[0, 1].set_ylabel('$α$', fontsize=12)
    axs[0, 1].grid(True)

    # Gráfico 3
    axs[1, 0].plot(t[1:], velocidad_angular_suavizada, color='g', linestyle='-.', linewidth=2)
    axs[1, 0].set_title('Velocidad Angular Suavizada', fontsize=14)
    axs[1, 0].set_xlabel('Tiempo', fontsize=12)
    axs[1, 0].set_ylabel('$ω_{suavizada}$', fontsize=12)
    axs[1, 0].grid(True)

    # Gráfico 4
    axs[1, 1].plot(t[2:], aceleracion_angular_suavizada, color='m', linestyle=':', linewidth=2)
    axs[1, 1].set_title('Aceleración Angular Suavizada', fontsize=14)
    axs[1, 1].set_xlabel('Tiempo', fontsize=12)
    axs[1, 1].set_ylabel('$α_{suavizada}$', fontsize=12)
    axs[1, 1].grid(True)

    # Opcional: si tienes más subplots, puedes añadir más configuración aquí

    # Ajustar espacios entre subplots
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.5)

    # Mostrar la figura
    plt.show()