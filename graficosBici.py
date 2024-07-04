import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import plot_with_shades

for i in range(1, 6):
    df = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    t = df['tiempo']
    x = df['posicion']
    vx = df['velocidad']
    ax = df['aceleracion']
    viscous_force = df['fuerza_viscosa']
    
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    # Gráfico 1
    plot_with_shades(axs[0, 0], t, x, 0)
    axs[0, 0].set_title('Posición en eje X', fontsize=16)
    axs[0, 0].set_xlabel('Tiempo(s)', fontsize=14)
    axs[0, 0].set_ylabel('$x(m)$', fontsize=14)
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(t), max(t)])
    axs[0, 0].set_ylim([min(x), max(x)])

    # Gráfico 2
    plot_with_shades(axs[0, 1], t, vx, 1)
    axs[0, 1].set_title('Velocidad en eje X', fontsize=16)
    axs[0, 1].set_xlabel('Tiempo(s)', fontsize=14)
    axs[0, 1].set_ylabel('$v_{x} (m/s)$', fontsize=14)
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_xlim([min(t), max(t)])
    axs[0, 1].set_ylim([min(vx), max(vx)])

    # Gráfico 3
    plot_with_shades(axs[1, 0], t, ax, 2)
    axs[1, 0].set_title('Aceleración en eje X', fontsize=16)
    axs[1, 0].set_xlabel('Tiempo(s)', fontsize=14)
    axs[1, 0].set_ylabel('$a_{x} (m/s^2)$', fontsize=14)
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(t), max(t)])
    axs[1, 0].set_ylim([min(ax), max(ax)])

    # Gráfico 4
    plot_with_shades(axs[1, 1], t, viscous_force, 3)
    axs[1, 1].set_title('Fuerza viscosa', fontsize=16)
    axs[1, 1].set_xlabel('Tiempo(s)', fontsize=14)
    axs[1, 1].set_ylabel('$F_{v} (N)$', fontsize=14)
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(t), max(t)])
    axs[1, 1].set_ylim([min(viscous_force), max(viscous_force)])

    # Gráfico 5
    plot_with_shades(axs[2, 0], vx, viscous_force, 4)
    axs[2, 0].set_title('Fuerza viscosa en función de la velocidad', fontsize=16)
    axs[2, 0].set_xlabel('$v_{x} (m/s)$', fontsize=14)
    axs[2, 0].set_ylabel('$F_{v} (N)$', fontsize=14)
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_xlim([min(vx), max(vx)])
    axs[2, 0].set_ylim([min(viscous_force), max(viscous_force)])

    # Ajustar espacios entre subplots
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.5)

    # Mostrar la figura
    plt.show()