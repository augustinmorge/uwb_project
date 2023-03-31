#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = THIS_FOLDER #os.path.join(THIS_FOLDER, 'log_long')

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
filename = os.path.join(LOGS_FOLDER, "Long_log_24_03_2023_16_44_05.csv")

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
idx_start = np.argmax(time.flatten() > 12000) #9540
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

T, data, std = qrunch.allan_deviation(dist, 1/np.mean(np.diff(time)))

def create_basic_plot_allan(ax, T, data, title="Allan Deviation"):
    ax.loglog(T, data, label='allan')
    ax.set_title(f"{title}")
    ax.set_xlabel("Time [log(s)]")
    ax.set_ylabel("m")
    #Limiter les chiffres significatifs
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 0))
    ax.grid()
    ax.legend()

ax1 = axs[1]
ax1.plot((T), (std), label = 'std')
ax1.loglog(T, data)

fig2, ax2 = plt.subplots(1,1)

sigma = np.std(dist)
print(f"sigma = {sigma}")

dbb = sigma*np.sqrt(3)/T
q = sigma/(2*T)
bb = sigma/np.sqrt(T)
tau = 1000
bc = 2*tau*sigma**2/T*(1-tau/(2*T)*(3-4*np.exp(-T/tau) + np.exp(-2*T/tau)))
rw = sigma*np.sqrt(T/3)
derive = sigma*T/np.sqrt(2)

T= T/60/60 # s->h
ax2.loglog(T, data, label = "allan deviation")


ax2.loglog(T, bb, label = "gaussian noise")
ax2.loglog(T, 5*bc, label = "bruit corélé")
# ax2.loglog(T, derive, label = "derive")
ax2.loglog(T, 0.0013*rw, label = "random walk")
# ax2.loglog(T, q, label = "quantification")
# ax2.loglog(T, dbb, label = "dérivée bruit blanc")

total = np.sqrt(bb**2 + (0.0013*rw)**2 + (5*bc)**2)
# total = np.sqrt(bb**2 + (0.0013*rw)**2)
ax2.loglog(T, total, label = "total", linewidth = 3, color = 'red')
ax2.set_xlabel('h')

ax2.set_ylabel('m')
ax2.set_title('Allan Deviation')


plt.legend()
plt.show()
