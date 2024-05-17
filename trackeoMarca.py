import numpy as np
import matplotlib.pyplot as plt
import cv2
import json
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
    # Listas para almacenar los valores de las columnas
    posiciones_x = []
    posiciones_y = []
    velocidades_bici = []
    t = []

    # Obtenemos los datos de las posiciones x e y en función del tiempo
    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\datosRuedaX_{i}.txt', 'r') as f:
        for linea in f:
            partes = linea.split()
            t.append(float(partes[0].replace(',', '.')))
            posiciones_x.append(float(partes[1].replace(',', '.')))

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\datosRuedaY_{i}.txt', 'r') as f:
        for linea in f:
            partes = linea.split()
            posiciones_y.append(float(partes[1].replace(',', '.')))

    with open(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\velocidad_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        velocidades_bici = [float(numero.strip()) for numero in numeros]

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

     # Rutas de los archivos
    file_path_posiciones_x = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionX_{i}.txt'
    file_path_posiciones_y = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionY_{i}.txt'
    file_path_velocidad_x = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadX_{i}.txt'
    file_path_velocidad_y = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadY_{i}.txt'
    file_path_aceleracion_x = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleracionX_{i}.txt'
    file_path_aceleracion_y = f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleracionY_{i}.txt'

    # Escribir en los archivos
    with open(file_path_posiciones_x, "w") as file:
        for item in posiciones_x:
            file.write(f"{item.round(2)},")
    with open(file_path_posiciones_y, "w") as file:
        for item in posiciones_y:
            file.write(f"{item},")
    with open(file_path_velocidad_x, "w") as file:
        for item in vx:
            file.write(f"{item},")
    with open(file_path_velocidad_y, "w") as file:
        for item in vy:
            file.write(f"{item},")        
    with open(file_path_aceleracion_x, "w") as file:
        for item in ax:
            file.write(f"{item},")
    with open(file_path_aceleracion_y, "w") as file:
        for item in ay:
            file.write(f"{item},")        

    print(len(vx))
    print(len(velocidades_bici))

    # Calculamos la velocidad angular
    velocidad_angular = [np.divide((np.sqrt(np.square(vx[i]-velocidades_bici[i])+np.square(vy[i]))),0.7366) for i in range(len(vx))]


    # Guardamos la velocidad angular en un archivo
    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidades_angulares_{i}.txt', 'w') as f:
        for angular_speed in velocidad_angular:
            f.write(f"{angular_speed}\n")

    aceleracion_angular = calculate_angular_aceleration(velocidad_angular,t[1:])
    # Guardamos la aceleracion angular en un archivo
    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\aceleraciones_angulares_{i}.txt', 'w') as f:
        for angular_aceleration in aceleracion_angular:
            f.write(f"{angular_aceleration}\n")

    # Graficamos los datos
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    axs[0, 0].plot(t, posiciones_x)
    axs[0, 0].set_xlabel('tiempo')
    axs[0, 0].set_ylabel('$p_{x}$')
    axs[0, 0].grid(True)

    axs[0, 1].plot(t, posiciones_y)
    axs[0, 1].set_xlabel('tiempo')
    axs[0, 1].set_ylabel('$p_{y}$')
    axs[0, 1].grid(True)

    axs[1, 0].plot(t[1:], vx)
    axs[1, 0].set_xlabel('tiempo')
    axs[1, 0].set_ylabel('$v_{x}$')
    axs[1, 0].grid(True)

    axs[1, 1].plot(t[1:], vy)
    axs[1, 1].set_xlabel('tiempo')
    axs[1, 1].set_ylabel('$v_{y}$')
    axs[1, 1].grid(True)

    axs[2, 0].plot(t[2:], ax)
    axs[2, 0].set_xlabel('tiempo')
    axs[2, 0].set_ylabel('$a_{x}$')
    axs[2, 0].grid(True)

    axs[2, 1].plot(t[2:], ay)
    axs[2, 1].set_xlabel('tiempo')
    axs[2, 1].set_ylabel('$a_{y}$')
    axs[2, 1].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()


    # Graficamos los datos de la velocidad angular y aceleración angular
    velocidad_angular = savgol_filter(velocidad_angular, 30, 3)
    aceleracion_angular = savgol_filter(aceleracion_angular, 30, 3)
    fig, axs = plt.subplots(1, 2, figsize=(14, 10))
    
    axs[0].plot(t[1:], velocidad_angular)
    axs[0].set_xlabel('tiempo')
    axs[0].set_ylabel('omega')
    axs[0].grid(True)
    
    axs[1].plot(t[2:], aceleracion_angular)
    axs[1].set_xlabel('tiempo')
    axs[1].set_ylabel('alpha')
    axs[1].grid(True)
    
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)

    plt.show()
    
    #Convierto a pixeles para graficar

    vx = np.divide(vx,valor)
    vy = np.divide(vy,valor)
    ax = np.divide(ax,valor)
    ay = np.divide(ay,valor)
    posiciones_x = np.divide(posiciones_x,valor)
    posiciones_y = np.divide(posiciones_y,valor)
    velocidades_bici = np.divide(velocidades_bici,valor)


    # Leer video frame a frame y graficar vectores
    cap = cv2.VideoCapture(f'vid{i}.mov')
    frame_count = 0
    x = 0
    y = 0
    z = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        # Graficar vectores en la imagen
        if frame_count >= 1:
            cv2.imwrite(f'Vectores_En_Videos\\Video{i}\\\imagen{frame_count}.jpg', frame)
            imagen = cv2.imread(f'Vectores_En_Videos\\Video{i}\\imagen{frame_count}.jpg')
            punto_origen = (int(posiciones_x[x]), int(posiciones_y[x]))
            punto_destino = (punto_origen[0]+int(vx[z])-int(velocidades_bici[z]), punto_origen[1]+int(vy[z]))
            imagen_con_vector = cv2.arrowedLine(imagen, punto_origen, punto_destino, (0,0,255), thickness=3)
            cv2.imwrite(f'Vectores_En_Videos\\Video{i}\\imagen{frame_count}.jpg', imagen_con_vector)
            z = z + 1
            y = y + 1

        frame_count += 1
        x = x + 1

    cap.release()
   