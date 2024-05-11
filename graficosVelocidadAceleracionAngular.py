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

   
    velocidad_angular_suavizada = savgol_filter(velocidades_angulares,len(velocidades_angulares),5)
    aceleracion_angular_suavizada = savgol_filter(aceleraciones_angulares,len(aceleraciones_angulares),5)

    # Graficamos los datos
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    axs[0, 0].plot(t[1:], velocidades_angulares)
    axs[0, 0].set_xlabel('tiempo')
    axs[0, 0].set_ylabel('$ω$')
    axs[0, 0].grid(True)

    axs[0, 1].plot(t[2:], aceleraciones_angulares)
    axs[0, 1].set_xlabel('tiempo')
    axs[0, 1].set_ylabel('$α$')
    axs[0, 1].grid(True)

    axs[1, 0].plot(t[1:], velocidad_angular_suavizada)
    axs[1, 0].set_xlabel('tiempo')
    axs[1, 0].set_ylabel('$ω_suavizada$')
    axs[1, 0].grid(True)

    axs[1, 1].plot(t[2:], aceleracion_angular_suavizada)
    axs[1, 1].set_xlabel('tiempo')
    axs[1, 1].set_ylabel('$α_suavizada$')
    axs[1, 1].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()        