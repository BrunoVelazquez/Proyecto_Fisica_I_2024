import cv2
import os
import numpy as np
import json
import pandas as pd

# Parámetros configurables:
start_vid_index = 1
end_vid_index = 2

def generar_imagenes_vectorizadas(i, output_path):
    """
    Genera imágenes de un video dado, con sus respectivos vectores de velocidad.

    Parámetros:
    i (int): índice del video a procesar.
    output_path (str): ruta donde se guardarán las imágenes generadas.
    """
    # Obtenemos los datos de las posiciones y velocidades
    velocidades_bici = pd.read_csv(f'Datos_Extraidos_Bici\\datos_bici_video_{i}.csv')['velocidad']
    
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca\\datos_marca_video_{i}.csv')
    posiciones_x = df_marca['posicion_x']
    posiciones_y = df_marca['posicion_y']
    vx_marca = df_marca['velocidad_x']
    vy_marca = df_marca['velocidad_y']
    
    # Extraemos los datos de conversión de la bicicleta y del marcador
    ruta_archivo = 'Conversiones\Pixeles_A_Metros.json'
    with open(ruta_archivo,"r") as archivo:
        datos = json.load(archivo)
        valor = float(datos[i-1]["valor"])
    
    # Convertimos a pixeles para graficar
    vx_marca = np.divide(vx_marca,valor)
    vy_marca = np.divide(vy_marca,valor)
    posiciones_x = np.divide(posiciones_x,valor)
    posiciones_y = np.divide(posiciones_y,valor)
    velocidades_bici = np.divide(velocidades_bici,valor)

    # Leemos el video frame a frame y graficamos vectores
    cap = cv2.VideoCapture(f'vid{i}.mov')
    frame_count = 0
    x = 0
    z = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Graficamos vectores en la imagen
        if frame_count >= 1:
            cv2.imwrite(f'{output_path}\\imagen{frame_count}.jpg', frame)
            imagen = cv2.imread(f'{output_path}\\imagen{frame_count}.jpg')
            punto_origen = (int(posiciones_x[x]), int(posiciones_y[x]))
            punto_destino = (
                punto_origen[0]+int(vx_marca[z])-int(velocidades_bici[z]),
                punto_origen[1]+int(vy_marca[z])
            )
            imagen_con_vector = cv2.arrowedLine(imagen, punto_origen, punto_destino, (0,0,255), thickness=10)
            cv2.imwrite(f'{output_path}\\imagen{frame_count}.jpg', imagen_con_vector)
            z = z + 1

        frame_count += 1
        x = x + 1

    cap.release()
    
def obtener_imagenes_del_directorio(directorio, extension='.jpg'):
    """
    Obtiene una lista de rutas de imágenes con una extensión específica en un directorio.

    Args:
    - directorio (str): Ruta del directorio donde buscar las imágenes.
    - extension (str, opcional): Extensión de las imágenes a buscar. Default es '.jpg'.

    Returns:
    - list: Lista de rutas de imágenes.
    """
    return [os.path.join(directorio, archivo) for archivo in os.listdir(directorio) if archivo.endswith(extension)]

def crear_video(imagenes, ruta_salida, nombre_video, fps=30):
    """
    Crea un video a partir de una lista de rutas de imágenes.

    Args:
    - imagenes (list): Lista de rutas de imágenes.
    - nombre_video (str): Nombre del archivo de video de salida.
    - fps (int, optional): Cuadros por segundo del video. Default es 30.
    """
    if not imagenes:
        print("No hay imágenes para crear el video.")
        return

    # Leer la primera imagen para obtener el tamaño
    img = cv2.imread(imagenes[0])
    height, width, _ = img.shape

    # Crear objeto VideoWriter
    video_path = os.path.join(ruta_salida, nombre_video)
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Concatenar imágenes en un video
    for imagen_path in sorted(imagenes, key=lambda f1: int(''.join(filter(str.isdigit, f1)))):  # Ordenar las imágenes por nombre
        img = cv2.imread(imagen_path)
        video.write(img)

    # Liberar recursos
    video.release()

def eliminar_imagenes(imagenes):
    # Borrar las imágenes
    for image in imagenes:
        os.remove(image)

for i in range(start_vid_index, end_vid_index):
    
    print(f'Procesando imagenes vectorizadas de video {i}')
    generar_imagenes_vectorizadas(i, f'Vectores_En_Videos\\Video{i}')
    directorio_imagenes = f'Vectores_En_Videos\\Video{i}'
    imagenes = obtener_imagenes_del_directorio(directorio_imagenes)
    nombre_video = f'Video_{i}_Vector_Velocidad.mov'
    
    print(f'Creando video {nombre_video}')
    crear_video(imagenes, directorio_imagenes, nombre_video)
    
    print(f'Eliminando imagenes vectorizadas de video {i}')
    eliminar_imagenes(imagenes)
    
    print(f'Video {i} procesado')