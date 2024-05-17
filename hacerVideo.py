import cv2
import os
import numpy as np
import json

# Parámetros configurables:
start_vid_index = 1
end_vid_index = 6

def generar_imagenes_vectorizadas(i, output_path):
    """
    Genera imágenes de un video dado, con sus respectivos vectores de velocidad.

    Parámetros:
    i (int): índice del video a procesar.
    output_path (str): ruta donde se guardarán las imágenes generadas.
    """
    # Obtenemos los datos de las posiciones y velocidades
    posiciones_x = obtener_datos(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionX_{i}.txt')
    posiciones_y = obtener_datos(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionY_{i}.txt')
    velocidades_bici = obtener_datos(f'Datos_Extraidos_Bici\\Datos_Video_{i}\\velocidad_{i}.txt')
    vx_marca = obtener_datos(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadX_{i}.txt')
    vy_marca = obtener_datos(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadY_{i}.txt')
    
    # Extraemos los datos de conversión de la bicicleta y del marcador
    ruta_archivo = 'Conversiones\Pixeles_A_Metros.json'
    with open(ruta_archivo,"r") as archivo:
        datos = json.load(archivo)
        valor = float(datos[i-1]["valor"])
    
    # Convertimos a pixeles para graficar
    vx_marca = np.divide(vx_marca,valor)
    vy_marca = np.divide(vy_marca,valor)
    '''
    Lo comento porque, por ahora, no lo necesitaremos acá
    ax = np.divide(ax,valor)
    ay = np.divide(ay,valor)
    '''
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
            imagen_con_vector = cv2.arrowedLine(imagen, punto_origen, punto_destino, (0,0,255), thickness=3)
            cv2.imwrite(f'{output_path}\\imagen{frame_count}.jpg', imagen_con_vector)
            z = z + 1

        frame_count += 1
        x = x + 1

    cap.release()

def obtener_datos(archivo_absoluto):
    """
    Obtiene los datos de un archivo de texto, donde cada línea es una lista de números separados por comas.

    Args:
    - archivo_absoluto (str): Ruta del archivo de texto.

    Returns:
    - Una lista de números de punto flotante.
    """
    # Abrimos el archivo de texto y leemos la línea
    with open(archivo_absoluto, 'r') as f:
        numeros = f.readline().split(',')

        # Verificamos si el último elemento es una cadena vacía
        if numeros[-1] == '':
            # Eliminamos el último elemento si es una cadena vacía
            numeros = numeros[:-1]

        # Convertimos cada número a punto flotante y lo devolvemos
        return [float(numero) for numero in numeros]
    
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