import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import savgol_filter

for i in range(1, 6):
    velociades_bici = []
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\velocidad_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        velocidades_bici = [float(numero.strip()) for numero in numeros]
    
    velocidades_bici = np.square(velocidades_bici)

    producto_parcial = np.multiply(velocidades_bici,79)

    energia_cinetica = np.multiply(producto_parcial,0.5)

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\energiaCinetica_{i}.txt', "w") as file:
        for item in energia_cinetica:
            file.write(f"{item.round(2)},")
    
    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\variacion_energiaCinetica_{i}.txt', "w") as file:
        valor = energia_cinetica[len(energia_cinetica)-1] - energia_cinetica[0]
        file.write(f"{valor.round(2)}")

