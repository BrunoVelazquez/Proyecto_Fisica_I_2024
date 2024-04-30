import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

def calculate_aceleration(vx,vy, t_values):
    ax = np.diff(vx) / np.diff(t_values) # La función diff() de numpy calcula la diferencia entre dos puntos sucesivos.
    ay = np.diff(vy) / np.diff(t_values)

    return ax.round(2),ay.round(2)

def calculate_velocity(x_values,y_values, t_values):
    dx_dt = np.diff(x_values) / np.diff(t_values)
    dy_dt = np.diff(y_values) / np.diff(t_values)
   
    return dx_dt.round(2),dy_dt.round(2)  

# Listas para almacenar los valores de las columnas
posiciones_x = []
posiciones_y = []
t = []

# Obtenemos los datos de las posiciones x e y en funcion del tiempo de la app PhysicsLab
with open('datosRuedaX_1.txt', 'r') as f:
    # Itera sobre cada línea del archivo
    for linea in f:
        # Divide la línea en dos partes utilizando el espacio como delimitador
        partes = linea.split()
        # Convierte las partes a números y guárdalas en las listas correspondientes
        t.append(float(partes[0].replace(',', '.')))  # Reemplaza ',' por '.' para convertir a número decimal
        posiciones_x.append(float(partes[1].replace(',', '.')))

with open('datosRuedaY_1.txt', 'r') as f:
    # Itera sobre cada línea del archivo
    for linea in f:
        # Divide la línea en dos partes utilizando el espacio como delimitador
        partes = linea.split()
        # Convierte las partes a números y guárdalas en las listas correspondientes
        posiciones_y.append(float(partes[1].replace(',', '.')))        



posiciones_x=np.multiply(posiciones_x,0.00897381812634432)
posiciones_y=np.multiply(posiciones_y,0.00897381812634432)

vx,vy = calculate_velocity(posiciones_x,posiciones_y,t)
ax,ay = calculate_aceleration(vx, vy,t[1:])


#Prueba de graficar puntos cualquiera en una imagen

# Cargar la imagen
image = cv2.imread('frame.jpg')

# Definir las coordenadas de origen y destino 275,520),(409,464)
origen = (275, 520)  # Cambia las coordenadas según tus necesidades
destino = (409, 464)  # Cambia las coordenadas según tus necesidades

# Dibujar el vector en la imagen
color = (0, 255, 0)  # Color del vector (en formato BGR)
cv2.arrowedLine(image, origen, destino, color, thickness=2)

# Convertir la imagen de BGR a RGB (Matplotlib espera imágenes en RGB)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imwrite('frame2.jpg',image)

# Mostrar la imagen con Matplotlib
plt.imshow(image_rgb)
plt.show()
