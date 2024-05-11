import cv2
import os

# Parámetros configurables:
start_vid_index = 1
end_vid_index = 4

# Ruta donde están las imágenes
ruta = "Vectores\\Video1\\"

for i in range(start_vid_index, end_vid_index):
    # Obtener lista de nombres de archivo de las imágenes
    prefix = f''
    tmpdir = os.path.join(ruta, prefix)
    frames = [f for f in os.listdir(tmpdir) if f.endswith('.jpg')]
    frames.sort(key=lambda f1: int(''.join(filter(str.isdigit, f1))))

    # Leer la primera imagen para obtener las dimensiones
    frame_path = os.path.join(tmpdir, frames[0])
    frame = cv2.imread(frame_path)
    height, width, channels = frame.shape

    # Nombre de archivo de salida
    output = f'{prefix}.mov'

    # Crear el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Códec para el formato MP4
    out = cv2.VideoWriter(output, fourcc, 30.0, (width, height))

    # Agregar las imágenes al vídeo
    for f in frames:
        frame_path = os.path.join(tmpdir, f)
        frame = cv2.imread(frame_path)
        out.write(frame)

    # Liberar el objeto VideoWriter
    out.release()