import numpy as np
import matplotlib.pyplot as plt
import cv2
import json
import pandas as pd
from utils import fill
from scipy.signal import savgol_filter

def calculate_aceleration(vx, vy, t_values):
    """
    Calcula los componentes de la aceleración según los valores de tiempo y velocidad

    Parametros:
    vx (array): Arreglo de velocidades en el eje x.
    vy (array): Arreglo de velocidades en el eje y.
    t_values (array): Arreglo de valores de tiempo.

    Retorna:
    tuple: Valores de aceleración en el eje x y en el eje y.
    """
    ax = np.diff(vx) / np.diff(t_values)
    ay = np.diff(vy) / np.diff(t_values)

    return ax.round(2), ay.round(2)

def calculate_velocity(x_values, y_values, t_values):
    """
    Calcula los componentes de la velocidad según los valores de tiempo y posición

    Parametros:
    x_values (array): Arreglo de pocisiones en el eje x.
    y_values (array): Arreglos de pocisiones en el eje y.
    t_values (array): Arreglo de valores de tiempo.

    Retorna:
    tuple: Valores de velocidad en el eje x y en el eje y.
    """
    dx_dt = np.diff(x_values) / np.diff(t_values)
    dy_dt = np.diff(y_values) / np.diff(t_values)

    return dx_dt.round(2), dy_dt.round(2)

def calculate_angular_aceleration(w_values, t_values):
    """
    Calcula la aceleración angular según la velocidad angular y los valores de tiempo.

    Parametros:
    w_values (array): Arreglo de valores de velocidad angular.
    t_values (array): Arreglos de valores de tiempo.

    Retorna:
    array: Valores de aceleración angular.
    """
    dw_dt = np.diff(w_values) / np.diff(t_values)

    return dw_dt.round(2)

# Bucle para procesar cada video
for i in range(1, 6):
    df_bici = pd.read_csv(f'Datos_Extraidos_Bici\\datos_bici_video_{i}.csv')
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv')
    # Listas para almacenar los valores de las columnas
    posiciones_x = df_marca['posicion_x_px'].to_numpy()
    posiciones_y = df_marca['posicion_y_px'].to_numpy()
    t = df_marca['tiempo']
    velocidades_bici = df_bici['velocidad']
    

    # Extraigo del archivo los datos de conversion
    ruta_archivo = 'Conversiones\Pixeles_A_Metros.json'
    with open(ruta_archivo,"r") as archivo:
        datos = json.load(archivo)
        valor = float(datos[i-1]["valor"])

    # Convertimos las posiciones x e y a metros
    posiciones_x = np.multiply(posiciones_x, valor)
    posiciones_y = np.multiply(posiciones_y, valor)

    # Calculamos las velocidades y aceleraciones
    vx, vy = calculate_velocity(posiciones_x, posiciones_y, t)
    ax, ay = calculate_aceleration(vx, vy, t[1:])

    maxlength = max(len(posiciones_x), len(posiciones_y), len(vx), len(vy), len(ax), len(ay))
    vx = fill(vx, maxlength)
    vy = fill(vy, maxlength)
    ax = fill(ax, maxlength)
    ay = fill(ay, maxlength)
    
    df_marca['posicion_x'] = posiciones_x
    df_marca['posicion_y'] = posiciones_y
    df_marca['velocidad_x'] = vx
    df_marca['velocidad_y'] = vy
    df_marca['aceleracion_x'] = ax
    df_marca['aceleracion_y'] = ay
    
    # Calculamos la velocidad angular y la aceleración angular
    velocidad_angular = [np.divide((np.sqrt(np.square(vx[i]-velocidades_bici[i])+np.square(vy[i]))),0.7366) for i in range(len(vx))]
    aceleracion_angular = calculate_angular_aceleration(velocidad_angular,t)

    df_marca['velocidad_angular'] = velocidad_angular
    df_marca['aceleracion_angular'] = fill(aceleracion_angular, maxlength)
    
    df_marca.to_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv', index=False)
    # # Graficamos los datos
    # fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    
    # axs[0, 0].plot(t, posiciones_x)
    # axs[0, 0].set_xlabel('tiempo (s)')
    # axs[0, 0].set_ylabel('$x (m)$')
    # axs[0, 0].grid(True)

    # axs[0, 1].plot(t, posiciones_y)
    # axs[0, 1].set_xlabel('tiempo (s)')
    # axs[0, 1].set_ylabel('$y (m)$')
    # axs[0, 1].grid(True)

    # axs[1, 0].plot(t[1:], vx)
    # axs[1, 0].set_xlabel('tiempo (s)')
    # axs[1, 0].set_ylabel('$v_{x} (m/s)$')
    # axs[1, 0].grid(True)

    # axs[1, 1].plot(t[1:], vy)
    # axs[1, 1].set_xlabel('tiempo (s)')
    # axs[1, 1].set_ylabel('$v_{y} (m/s)$')
    # axs[1, 1].grid(True)

    # axs[2, 0].plot(t[2:], ax)
    # axs[2, 0].set_xlabel('tiempo (s)')
    # axs[2, 0].set_ylabel('$a_{x} (m/s^2)$')
    # axs[2, 0].grid(True)

    # axs[2, 1].plot(t[2:], ay)
    # axs[2, 1].set_xlabel('tiempo (s)')
    # axs[2, 1].set_ylabel('$a_{y} (m/s^2)$')
    # axs[2, 1].grid(True)

    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    # plt.show()