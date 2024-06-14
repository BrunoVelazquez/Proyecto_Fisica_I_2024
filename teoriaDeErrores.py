import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

for i in range(1, 6):
    tiempo = []
    x = []
    y = []
    vx = []
    vy = []
    
    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\datosRuedaX_{i}.txt', 'r') as f:
        for linea in f:
            partes = linea.split()
            tiempo.append(float(partes[0].replace(',', '.')))

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionX_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        x = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\posicionY_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        y = [float(numero.strip()) for numero in numeros]       

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadX_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        vx = [float(numero.strip()) for numero in numeros]

    with open(f'Datos_Extraidos_Marca\\Datos_Video_{i}\\velocidadY_{i}.txt', 'r') as f:
        numeros = f.readline().split(',')
        vy = [float(numero.strip()) for numero in numeros]

    # Calcular la señal filtrada para cada variable
    señal_filtrada_x = [2.65 * t + 3 - 0.35 * math.sin(8.46 * t + 7.75) for t in tiempo]
    señal_filtrada_y = [0.28 * math.sin(9 * t - 3.58) + 4.45 for t in tiempo]
    señal_filtrada_vx = [3 * math.exp(-0.3 * t) * math.sin(9.024 * t + 0.024) + 3.5 + (-0.31 * t - 0.016) for t in tiempo[1:]]
    señal_filtrada_vy = [3.5 * math.exp(-0.12 * t) * math.sin(9.024 * t - 2) + 0.1 for t in tiempo[1:]]

    # Calcular MAE y MSE para x
    mae_x = mean_absolute_error(x, señal_filtrada_x)
    mse_x = mean_squared_error(x, señal_filtrada_x)
    
    # Calcular MAE y MSE para y
    mae_y = mean_absolute_error(y, señal_filtrada_y)
    mse_y = mean_squared_error(y, señal_filtrada_y)

    # Calcular MAE y MSE para vx
    mae_vx = mean_absolute_error(vx, señal_filtrada_vx)
    mse_vx = mean_squared_error(vx, señal_filtrada_vx)

    # Calcular MAE y MSE para vy
    mae_vy = mean_absolute_error(vy, señal_filtrada_vy)
    mse_vy = mean_squared_error(vy, señal_filtrada_vy)

    # Escribir resultados en archivos
    with open(f'Teoria_De_Errores\\Video_{i}\\x_mae.txt', 'w') as f:
        f.write(f"{mae_x}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\x_mse.txt', 'w') as f:
        f.write(f"{mse_x}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\y_mae.txt', 'w') as f:
        f.write(f"{mae_y}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\y_mse.txt', 'w') as f:
        f.write(f"{mse_y}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\vx_mae.txt', 'w') as f:
        f.write(f"{mae_vx}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\vx_mse.txt', 'w') as f:
        f.write(f"{mse_vx}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\vy_mae.txt', 'w') as f:
        f.write(f"{mae_vy}\n")
    with open(f'Teoria_De_Errores\\Video_{i}\\vy_mse.txt', 'w') as f:
        f.write(f"{mse_vy}\n")