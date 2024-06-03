import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Cargar datos desde el archivo
A_data = []
t_data = []

with open('Datos_Extraidos_Marca/Datos_Video_1/velocidadY_1.txt', 'r') as f:
    numeros = f.readline().split(',')
    A_data = [float(numero.strip()) for numero in numeros]

with open(f'Datos_Extraidos_Bici\\Datos_Video_1\\tiempo_1.txt', 'r') as f:
        numeros = f.readline().split(',')
        t_data = [float(numero.strip()) for numero in numeros]   

t_data = np.array(t_data[1:])

# Define la función V(t)
def V(t, A, s, w, phi):
    return A * np.exp(-t * s) * np.cos(w * t + phi)


# Ajuste de la curva
# Utiliza curve_fit para encontrar los mejores parámetros
popt, pcov = curve_fit(V, t_data, A_data, p0=[3, 0.5, 1.5, 0])

# popt contiene los valores óptimos para A, s, w y phi
A_opt, s_opt, w_opt, phi_opt = popt

# Genera datos ajustados para comparación
A_fit = V(t_data, A_opt, s_opt, w_opt, phi_opt)

# Grafica los datos originales y los datos ajustados
plt.scatter(t_data, A_data, label='Datos', color='red')
plt.plot(t_data, A_fit, label='Ajuste', color='blue')
plt.legend()
plt.xlabel('Tiempo (t)')
plt.ylabel('Velocidad (V(t))')

# Título con la ecuación de la función ajustada
plt.title(r'Ajuste de datos a la función $V(t) = A \cdot e^{-t \cdot s} \cdot \cos(w \cdot t + \phi)$')

plt.show()

# Guardar los datos ajustados y los parámetros en un archivo
with open('ajusteMAS.txt', 'w') as f:
    # Escribir los datos ajustados
    f.write("Datos ajustados (A_fit):\n")
    for dato in A_fit:
        f.write(f"{dato}\n")
    
    # Escribir los parámetros ajustados
    f.write("\nParámetros ajustados:\n")
    f.write(f"A = {A_opt}\n")
    f.write(f"s = {s_opt}\n")
    f.write(f"w = {w_opt}\n")
    f.write(f"phi = {phi_opt}\n")

# Imprime los parámetros ajustados en la consola
print(f'Parámetros ajustados:\nA = {A_opt}\ns = {s_opt}\nw = {w_opt}\nphi = {phi_opt}')