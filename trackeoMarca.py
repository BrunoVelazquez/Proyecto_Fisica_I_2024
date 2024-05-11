import numpy as np
import matplotlib.pyplot as plt
import cv2

def calculate_aceleration(vx, vy, t_values):
    ax = np.diff(vx) / np.diff(t_values)
    ay = np.diff(vy) / np.diff(t_values)

    return ax.round(2), ay.round(2)

def calculate_velocity(x_values, y_values, t_values):
    dx_dt = np.diff(x_values) / np.diff(t_values)
    dy_dt = np.diff(y_values) / np.diff(t_values)

    return dx_dt.round(2), dy_dt.round(2)

def calculate_angular_aceleration(w_values, t_values):
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


    if i == 1:
        valor = 0.00897381812634432
    else:
        if i == 2:
            valor = 0.008110213653567056
        else:
            if i == 3:
                valor = 0.00780340688235733
            else:
                if i == 4:
                    valor = 0.008445287789158155
                else:
                    valor = 0.006923984374912447 

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
    velocidad_angular = [vx[i]+vy[i] - velocidades_bici[i] for i in range(len(vx))]

    print("velocidades bici")
    print(velocidades_bici)
    print("vx")
    print(vx)
    print("vy")
    print(vy)
    print("velocidad angular")
    print(velocidad_angular)

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

    #Convierto a pixeles para graficar

    vx = np.divide(vx,valor)
    vy = np.divide(vy,valor)
    ax = np.divide(ax,valor)
    ay = np.divide(ay,valor)
    posiciones_x = np.divide(posiciones_x,valor)
    posiciones_y = np.divide(posiciones_y,valor)


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
        if frame_count == 0:
            print()
        else:
            if frame_count == 1:
                color = (0, 255, 0)
                cv2.imwrite(f'Vectores\\Video{i}\\\imagen{frame_count}.jpg', frame)
                imagen = cv2.imread(f'Vectores\\Video{i}\\imagen{frame_count}.jpg')
                imagen_con_vector = cv2.arrowedLine(imagen, (int(posiciones_x[1]), int(posiciones_y[1])), (int(vx[z]), int(vy[z])), color, thickness=2)
                cv2.imwrite(f'Vectores\\Video{i}\\imagen{frame_count}.jpg', imagen_con_vector)
                #cv2.imshow('Imagen con vector', imagen_con_vector)
                cv2.waitKey(0)
                z = z + 1
            else:
                color = (0, 255, 0)
                cv2.imwrite(f'Vectores\\Video{i}\\\imagen{frame_count}.jpg', frame)
                imagen = cv2.imread(f'Vectores\\Video{i}\\imagen{frame_count}.jpg')
                imagen_con_vector = cv2.arrowedLine(imagen, (int(posiciones_x[x]), int(posiciones_y[x])), (int(vx[z]), int(vy[z])), color, thickness=2)
                cv2.imwrite(f'Vectores\\Video{i}\\imagen{frame_count}.jpg', imagen_con_vector)
                z = z + 1
                y = y + 1

        frame_count += 1
        x = x + 1

    cap.release()