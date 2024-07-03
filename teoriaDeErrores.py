import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math
import pandas as pd

for i in range(1, 6):
    df_marca = pd.read_csv(f'Datos_Extraidos_Marca/datos_marca_video_{i}.csv')
    tiempo = df_marca['tiempo']
    x = df_marca['posicion_x']
    y = df_marca['posicion_y']
    vx = df_marca['velocidad_x']
    vy = df_marca['velocidad_y']

    # Calcular la señal filtrada para cada variable
    señal_filtrada_x = [2.65 * t + 3 - 0.35 * math.sin(8.46 * t + 7.75) for t in tiempo]
    señal_filtrada_y = [0.28 * math.sin(9 * t - 3.58) + 4.45 for t in tiempo]
    señal_filtrada_vx = [3 * math.exp(-0.3 * t) * math.sin(9.024 * t + 0.024) + 3.5 + (-0.31 * t - 0.016) for t in tiempo]
    señal_filtrada_vy = [3.5 * math.exp(-0.12 * t) * math.sin(9.024 * t - 2) + 0.1 for t in tiempo]

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

    df_errores = pd.DataFrame({
        'mae_x': mae_x,
        'mse_x': mse_x,
        'mae_y': mae_y,
        'mse_y': mse_y,
        'mae_vx': mae_vx,
        'mse_vx': mse_vx,
        'mae_vy': mae_vy,
        'mse_vy': mse_vy,
    }, index=[0])
    
    # Escribir resultados en archivos
    df_errores.to_csv(f'Teoria_De_Errores\\errores_video_{i}.csv', index=False)