#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = THIS_FOLDER #os.path.join(THIS_FOLDER, 'old')

multiple_files = False
if multiple_files:
    time = np.array([])
    dist = np.array([])
    ids = np.array([])
    dbm = np.array([])
    # Parcourir tous les fichiers CSV dans le dossier "logs"
    with_dbm = False
    for filename in os.listdir(LOGS_FOLDER):
        # if filename.endswith('.csv'):
        if filename.startswith('Long_log_04_04_2023'): #or filename.startswith('Long_log_02_04') or filename.startswith('Long_log_03_04'):
            filepath = os.path.join(LOGS_FOLDER, filename)
            
            # Charger le fichier CSV
            data = np.genfromtxt(filepath, delimiter=';', skip_header=1)

            if data.shape[1] == 4: with_dbm = True

            # Extraire les colonnes ID, temps et distance
            ids_temp = data[:, 0]
            times_ms = data[:, 1]
            distances = data[:, 2]

            # mask_zeros = distances <= 0
            print(np.std(distances))
            mask_zeros = np.abs(distances - np.mean(distances)) > 0.5*np.std(distances)
            mask_zeros |= distances <= 0
            mask_zeros &= np.std(distances) > 0.2
            time = np.hstack((times_ms[~mask_zeros], time))
            ids = np.hstack((ids_temp[~mask_zeros], ids))
            dist = np.hstack((distances[~mask_zeros], dist))

            print(f"{distances[~mask_zeros].shape[0]/distances.shape[0]*100}%")

            if with_dbm:
                dbms = data[:, 3]
                dbm = np.hstack((dbms[~mask_zeros], dbm))

    # Obtenir les index triés en fonction de la valeur de temps
    sorted_indices = np.argsort(time)

    # Réorganiser les tableaux time et dist selon les index triés
    time = time[sorted_indices]/1000
    dist = dist[sorted_indices]
    ids = ids[sorted_indices]
    if with_dbm:
        dbm = dbm[sorted_indices]
        tab = np.vstack((ids,time,dist,dbm))
    else: tab = np.vstack((ids, time))
    header = "n°Anchor, Time (s), Distance (m), dbm"
    np.savetxt(f"{THIS_FOLDER}/{filename}_all.csv", tab.T, delimiter=";", header=header)

    # Charger le fichier CSV
    filename = os.path.join(THIS_FOLDER, "Long_log_01_04_2023_3j.csv")

    data = np.genfromtxt(filename, delimiter=';', skip_header=1)

    # import sys
    # sys.exit()


else:
    # Charger le fichier CSV
    filename = os.path.join(THIS_FOLDER, "Long_log_04_04_2023_13_59_21.csv")
    # filename = os.path.join(LOGS_FOLDER, "Long_log_02_04_2023_21_37_56.csv")

    data = np.genfromtxt(filename, delimiter=';', skip_header=1)
    with_dbm = False
    if data.shape[1] == 4: with_dbm = True

    # Extraire les colonnes ID, temps et distance
    ids = data[:, 0]
    times_ms = data[:, 1]
    distances = data[:, 2]

    # Convertir les temps en secondes et soustraire le temps de départ
    time = times_ms / 1000.0  #/ 60. /60.
    dist = distances
    time = time - np.min(time)

    if with_dbm:
        dbms = data[:, 3]
        dbm = dbms

    masked = True
    if masked:
        # mask = np.abs(dist - np.mean(dist)) > 3*np.std(dist)
        mask = dist <= 0
        time = time[~mask]
        dist = dist[~mask]
        ids = ids[~mask]
        if with_dbm:
            dbm = dbm[~mask]

# Tracer la distance en fonction du temps sans mask
idx_start = 0 #np.argmax(time.flatten() > 12000) #9540
idx_end = time.shape[0] #- time.shape[0]//10
time = time[idx_start:idx_end] - time[idx_start]
dist = dist[idx_start:idx_end]
if with_dbm:
    dbm = dbm[idx_start:idx_end]

print(f"Moyenne : {np.mean(dist)}")
print(f"Ecart-Type : {np.std(dist)}")


if with_dbm:
    #Ploting the Allan deviation
    fig, axs = plt.subplots(1,3)
    ax0 = axs[2]
    ax0.plot(time/60/60, dbm)
    ax0.set_xlabel("Time [h]")
    ax0.set_ylabel("DBM")
    ax0.set_title("Measurements")
    ax0.set_xlim([np.min(time/60/60), np.max(time/60/60)])
    ax0.grid()
else:
    fig, axs = plt.subplots(1,2)

fig.suptitle(f"Déviation d'Allan")
ax = axs[0]
# print(f"----> {(1/np.mean(np.diff(time)))}")
# print(f"----> {time.shape[0]/(time[-1] - time[0])}")
ax.plot(time/60/60, dist)#, s=0.1)
ax.set_xlabel("Time [h]")
ax.set_ylabel("Measurements [m]")
ax.set_title("Measurements")
ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
# ax.set_ylim([np.mean(dist)-5*np.std(dist), np.mean(dist)+5*np.std(dist)])
ax.grid()

import qrunch
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

Frequency = 1/np.mean(np.diff(time))
T, data, std = qrunch.allan_deviation(dist,Frequency)

ax1 = axs[1]
ax1.plot((T), (std), label = 'std')
ax1.loglog(T, data)

fig2, ax2 = plt.subplots(1,1)

sigma = 1.5*data[0] #np.std(dist)
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

bc = 10*bc; rw = 0.0015*rw
ax2.loglog(T, bb, label = "gaussian noise")
# ax2.loglog(T, bc, label = "bruit corélé")
# ax2.loglog(T, derive, label = "derive")
ax2.loglog(T, rw, label = "random walk")
# ax2.loglog(T, q, label = "quantification")
# ax2.loglog(T, dbb, label = "dérivée bruit blanc")

total = np.sqrt(bb**2 + (rw)**2) # + (bc)**2)
# total = np.sqrt(bb**2 + (0.0013*rw)**2)
ax2.loglog(T, total, label = "total", linewidth = 3, color = 'red')
ax2.set_xlabel('h')

ax2.set_ylabel('m')
ax2.set_title('Allan Deviation')


plt.legend()
plt.show()
