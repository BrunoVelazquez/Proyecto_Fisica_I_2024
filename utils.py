import numpy as np
import matplotlib.pyplot as plt

def fill(arr, maxlength):
    return np.append(arr, [arr[-1]] * (maxlength - len(arr)))

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
    '#FFE4C4',
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
                color=colors[color])
    ax.plot(x, y, marker='', color=colors[color], linewidth=1)
    min_value = min(0,min(y))
    #ax.fill_between(x, y, y2=[min_value]*len(x), color=colors[color], alpha=0.1)