#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


def plot_polynomial_regression(ax, x: np.ndarray, y: np.ndarray, degrees: list[int], label = "", R2 = True) -> None:
    """
    Plots polynomial regression lines of best fit for input data.

    Args:
        ax: A matplotlib Axes object to plot the data and lines on.
        x: A 1D numpy array of x-values.
        y: A 1D numpy array of y-values.
        degrees: A list of degrees of polynomial to fit.
        label: label for the plot

    Returns:
        None
    """

    try:
        # Calculate coefficients for each degree of polynomial
        coeffs = [np.polyfit(x, y, degree) for degree in degrees]

        # Plot data and polynomial lines of best fit
        for i, c in enumerate(coeffs):
            line_x = np.linspace(min(x), max(x), 10000)
            line_y = np.polyval(c, line_x)
            r_squared = r2_score(y, np.polyval(c, x))
            # Construct equation string
            coeffs_str = [f"{c[j]:.5f}x^{len(c)-j-1}" if len(c)-j-1 > 1 else f"{c[j]:.5f}x" if len(c)-j-1 == 1 else f"{c[j]:.5f}" for j in range(len(c)-2, -1, -1)]
            eqn = f"y = {c[-1]:.5f} + {' + '.join(coeffs_str)}" if len(coeffs_str) > 0 else f"y = {c[-1]:.5f}"
            if R2:
                ax.plot(line_x, line_y, label=f'{degrees[i]}° {label}: {eqn}\n(R² = {r_squared:.5f})')
            else:
                ax.plot(line_x, line_y, label=f'{degrees[i]}° {label}: {eqn}')

        ax.legend(loc='upper left')

    except Exception as e:
        print(f"Error: {e}")


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = os.path.join(THIS_FOLDER, 'log_long')

multiple_files = False
if multiple_files:
    time = np.array([])
    dist = np.array([])
    # Parcourir tous les fichiers CSV dans le dossier "logs"
    for filename in os.listdir(LOGS_FOLDER):
        if filename.endswith('.csv'):
            filepath = os.path.join(LOGS_FOLDER, filename)
            
            # Charger le fichier CSV
            data = np.genfromtxt(filepath, delimiter=';', skip_header=1)

            # Extraire les colonnes ID, temps et distance
            ids = data[:, 0]
            times_ms = data[:, 1]
            distances = data[:, 2]

            # Convertir les temps en secondes et soustraire le temps de départ
            times_s = times_ms / 1000.0  / 60. /60.

            time = np.hstack((times_s, time))
            dist = np.hstack((distances, dist))

# Charger le fichier CSV
filename = os.path.join(LOGS_FOLDER, "Long_log_28_03_2023_17_25_20.csv")

data = np.genfromtxt(filename, delimiter=';', skip_header=1)

# Extraire les colonnes ID, temps et distance
ids = data[:, 0]
times_ms = data[:, 1]
distances = data[:, 2]

# Convertir les temps en secondes et soustraire le temps de départ
time = times_ms / 1000.0  #/ 60. /60.
dist = distances
time = time - np.min(time)

# Tracer la distance en fonction du temps sans mask
idx_start = np.argmax(time.flatten() > 8000) #9540
idx_end = time.shape[0] #- time.shape[0]//10
time = time[idx_start:idx_end] - time[idx_start]
dist = dist[idx_start:idx_end]

print(f"Moyenne : {np.mean(dist)}")
print(f"Ecart-Type : {np.std(dist)}")


#Ploting the Allan deviation
fig, axs = plt.subplots(1,2)
fig.suptitle(f"Déviation d'Allan")

ax = axs[0]
ax.scatter(time/60/60, dist, s=0.1)
ax.set_xlabel("Time [h]")
ax.set_ylabel("Measurements [m]")
ax.set_title("Measurements")
ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
# ax.set_ylim([np.mean(dist)-5*np.std(dist), np.mean(dist)+5*np.std(dist)])
ax.grid()

import qrunch
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

tau = np.mean(np.diff(time))
print(f"f = {tau}")
T, data, std = qrunch.allan_deviation(dist, 1/tau)

transfo_log = lambda x : np.log(x)/np.log(10)

def create_basic_plot_allan(ax, T, data, title="Allan Deviation"):
    ax.plot(transfo_log(T), transfo_log(data), label='allan')
    ax.set_title(f"{title}")
    ax.set_xlabel("Time [log(s)]")
    ax.set_ylabel("m")
    #Limiter les chiffres significatifs
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 0))
    ax.grid()
    ax.legend()

ax1 = axs[1]
ax1.plot(transfo_log(T), transfo_log(std), label = 'std')
create_basic_plot_allan(ax1, T, data)

fig2, ax2 = plt.subplots(1,1)
fig3, ax3 = plt.subplots(1,1)


# ax2 = axs[1,0]
create_basic_plot_allan(ax2, T, data, "Gaussian noise")

# ax2 = axs[1,1]
create_basic_plot_allan(ax3, T, data, "?")

# Regression linéaire pour la déviation d'Allan
T_log = transfo_log(T)
data_log = transfo_log(data)
std_log = transfo_log(std)

min_index = np.argmin(data_log[1:,]) #//2
max_index = np.argmax(data_log[min_index:,]) + min_index

T_log1 = T_log[1:min_index,]
T_log2 = T_log[min_index:max_index,]

line1 = data_log[1:min_index,]
line2 = data_log[min_index:max_index,]

sigma = np.std(dist)
print(f"sigma = {sigma}")
print(f"sigma = {np.std(dist)}")

bb = transfo_log(sigma/np.sqrt(T))
rw = transfo_log(sigma*np.sqrt(T/3))
derive = transfo_log(sigma*T/np.sqrt(2))
bc = transfo_log(2*tau*sigma**2/T*(1-tau/(2*T)*(3-4*np.exp(-T/tau) + np.exp(-2*T/tau))))
q = transfo_log(sigma/(2*T))
dbb = transfo_log(sigma*np.sqrt(3)/T)

plot_polynomial_regression(ax2, T_log1, line1, [1],"measured")
plot_polynomial_regression(ax2, T_log1, (bb)[1:min_index,], [1],"estimated", R2 = False)

plot_polynomial_regression(ax3, T_log2, line2,[1],"measured")
plot_polynomial_regression(ax3, T_log2, (rw)[min_index:max_index,],[1],"estimated", R2 = False)

plt.legend()
plt.show()

