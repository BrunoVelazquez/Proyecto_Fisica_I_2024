import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Configuración del estilo
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#FF073A',
]

# Función para aplicar el efecto de sombreado
def plot_with_shades(ax, x, y, color):
    n_shades = 5
    diff_linewidth = 0.5
    alpha_value = 0.3 / n_shades
    for n in range(1, n_shades + 1):
        ax.plot(x, y,
                linewidth=1 + (diff_linewidth * n),
                alpha=alpha_value,
                color=color)
    ax.plot(x, y, marker='', color=color, linewidth=1)
    min_value = min(0,min(y))
    ax.fill_between(x, y, y2=[min_value]*len(x), color=color, alpha=0.1)

for i in range(1, 6):
    df = pd.read_csv(f'Datos_Extraidos_Bici/datos_bici_video_{i}.csv')
    t = df['tiempo']
    x = df['posicion']
    vx = df['velocidad']
    ax = df['aceleracion']
    viscous_force = df['fuerza_viscosa']
    
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))

    # Gráfico 1
    plot_with_shades(axs[0, 0], t, x, colors[0])
    axs[0, 0].set_title('Posición en eje X')
    axs[0, 0].set_xlabel('Tiempo(s)')
    axs[0, 0].set_ylabel('$x(m)$')
    axs[0, 0].grid(color='#2A3459')
    axs[0, 0].set_xlim([min(t), max(t)])
    axs[0, 0].set_ylim([min(x), max(x)])

    # Gráfico 2
    plot_with_shades(axs[0, 1], t, vx, colors[1])
    axs[0, 1].set_title('Velocidad en eje X')
    axs[0, 1].set_xlabel('Tiempo(s)')
    axs[0, 1].set_ylabel('$v_{x} (m/s)$')
    axs[0, 1].grid(color='#2A3459')
    axs[0, 1].set_xlim([min(t), max(t)])
    axs[0, 1].set_ylim([min(vx), max(vx)])

    # Gráfico 3
    plot_with_shades(axs[1, 0], t, ax, colors[2])
    axs[1, 0].set_title('Aceleración en eje X')
    axs[1, 0].set_xlabel('Tiempo(s)')
    axs[1, 0].set_ylabel('$a_{x} (m/s^2)$')
    axs[1, 0].grid(color='#2A3459')
    axs[1, 0].set_xlim([min(t), max(t)])
    axs[1, 0].set_ylim([min(ax), max(ax)])

    # Gráfico 4
    plot_with_shades(axs[1, 1], t, viscous_force, colors[3])
    axs[1, 1].set_title('Fuerza viscosa')
    axs[1, 1].set_xlabel('Tiempo(s)')
    axs[1, 1].set_ylabel('$F_{v} (N)$')
    axs[1, 1].grid(color='#2A3459')
    axs[1, 1].set_xlim([min(t), max(t)])
    axs[1, 1].set_ylim([min(viscous_force), max(viscous_force)])

    # Gráfico 5
    plot_with_shades(axs[2, 0], vx, viscous_force, colors[4])
    axs[2, 0].set_title('Fuerza viscosa en función de la velocidad')
    axs[2, 0].set_xlabel('$v_{x} (m/s)$')
    axs[2, 0].set_ylabel('$F_{v} (N)$')
    axs[2, 0].grid(color='#2A3459')
    axs[2, 0].set_xlim([min(vx), max(vx)])
    axs[2, 0].set_ylim([min(viscous_force), max(viscous_force)])

    # Ajustar espacios entre subplots
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0.3, hspace=0.5)

    # Mostrar la figura
    plt.show()