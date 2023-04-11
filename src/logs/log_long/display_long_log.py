#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = THIS_FOLDER #os.path.join(THIS_FOLDER, 'old')

def load_single_file(filename):
    dbm = np.array([])
    # Charger le fichier CSV
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
        alp = 1
        # print(alp*np.std(dist) + np.mean(dist))
        mask = np.abs(dist - np.mean(dist)) > alp*np.std(dist)
        # mask = dist <= 0
        time = time[~mask]
        dist = dist[~mask]
        ids = ids[~mask]
        if with_dbm:
            dbm = dbm[~mask]

    return time, dist, ids, dbm, with_dbm

def load_multiple_files():
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
            file_time, file_dist, file_ids, file_dbm = load_single_file(filepath)
            time = np.hstack((file_time, time))
            ids = np.hstack((file_ids, ids))
            dist = np.hstack((file_dist, dist))
            if with_dbm:
                dbm = np.hstack((file_dbm, dbm))

    # Obtenir les index triés en fonction de la valeur de temps
    sorted_indices = np.argsort(time)

    # Réorganiser les tableaux time et dist selon les index triés
    time = time[sorted_indices]/1000
    dist = dist[sorted_indices]
    ids = ids[sorted_indices]
    if with_dbm:
        dbm = dbm[sorted_indices]
        tab = np.vstack((ids,time,dist,dbm))
    else:
        tab = np.vstack((ids, time))
    header = "n°Anchor, Time (s), Distance (m), dbm"
    np.savetxt(f"{THIS_FOLDER}/{filename}_all.csv", tab.T, delimiter=";", header=header)

    return time, dist, ids, dbm

def load_data(filename):
    multiple_files = False
    if multiple_files:
        return load_multiple_files()
    else:
        # Charger le fichier CSV
        return load_single_file(filename)

def plot_data(ids, time, dist, dbm, with_dbm=True):
    # Tracer la distance en fonction du temps sans mask
    idx_start = 0 # np.argmax(time.flatten() > 25000) #9540
    idx_end = time.shape[0] #- time.shape[0]//10
    time = time[idx_start:idx_end] - time[idx_start]
    dist = dist[idx_start:idx_end]

    print(f"Moyenne : {np.mean(dist)}")
    print(f"Ecart-Type : {np.std(dist)}")

    if with_dbm:
        dbm = dbm[idx_start:idx_end]
        #Ploting the Allan deviation
        fig, axs = plt.subplots(1,2)
        ax0 = axs[1]
        ax0.plot(time/60/60, dbm)
        ax0.set_xlabel("Time [h]")
        ax0.set_ylabel("dBm")
        ax0.set_title("DBM")
        ax0.set_xlim([np.min(time/60/60), np.max(time/60/60)])
        ax0.grid()
        ax = axs[0]
    else:
        fig, ax = plt.subplots(1,1)

    fig.suptitle(f"Déviation d'Allan for anchor {int(ids[0])}")
    
    ax.scatter(time/60/60, dist, s=0.1)
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("m")
    ax.set_title("Measurements")
    ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
    ax.grid()

    import qrunch
    from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

    Frequency = 1/np.mean(np.diff(time))
    T, data, std = qrunch.allan_deviation(dist,Frequency)

    sigma = data[0] #np.std(dist)
    print(f"sigma = {sigma}")

    sigma_bb = 1.2*sigma
    sigma_rw = 0.00005
    dbb = sigma*np.sqrt(3)/T
    q = sigma/(2*T)
    bb = sigma_bb/np.sqrt(T)
    tau = 1000
    bc = 2*tau*sigma**2/T*(1-tau/(2*T)*(3-4*np.exp(-T/tau) + np.exp(-2*T/tau)))
    rw = sigma_rw*np.sqrt(T/3)
    derive = sigma*T/np.sqrt(2)

    T = T/60/60 # s->h
    
    if not with_dbm:
        fig2, ax2 = plt.subplots(1,1)
        ax2.loglog(T, data, label = "allan deviation")

        ax2.loglog(T, bb, label = "gaussian noise")
        # ax2.loglog(T, bc, label = "bruit corélé")
        # ax2.loglog(T, derive, label = "derive")
        ax2.loglog(T, rw, label = "random walk")
        # ax2.loglog(T, q, label = "quantification")
        # ax2.loglog(T, dbb, label = "dérivée bruit blanc")

        total = np.sqrt(bb**2 + (rw)**2)
        ax2.loglog(T, total, label = "total", linewidth = 3, color = 'red')
        ax2.set_xlabel('h')
        ax2.set_ylabel('m')
        ax2.set_title('Allan Deviation for anchor {}'.format(int(ids[0])))

        plt.legend()
    if with_dbm:
        fig, ax = plt.subplots(1,2)
        fig.suptitle("Allan deviation for anchor {}".format(int(ids[0])))

        ax1 = ax[0]
        ax1.loglog(T, data, label = "data")
        ax1.loglog(T, std, label = "std")

        ax1.loglog(T, bb, label = "gaussian noise")
        # ax1.loglog(T, bc, label = "bruit corélé")
        # ax1.loglog(T, derive, label = "derive")
        ax1.loglog(T, rw, label = "random walk")
        # ax1.loglog(T, q, label = "quantification")
        # ax1.loglog(T, dbb, label = "dérivée bruit blanc")

        total = np.sqrt(bb**2 + (rw)**2) # + (bc)**2)
        # total = np.sqrt(bb**2 + (0.0013*rw)**2)
        ax1.loglog(T, total, label = "total", linewidth = 3, color = 'red')
        ax1.set_xlabel('h')
        ax1.set_ylabel('m')
        ax1.set_title('Distance')
        ax1.legend()

        T, data_dbm, std_dbm = qrunch.allan_deviation(dbm,Frequency)
        
        ax1 = ax[1]
        sigma = data_dbm[0]
        bb = sigma/np.sqrt(T)
        T = T/60/60
        ax1.plot((T), (std_dbm), label = 'std')
        ax1.loglog(T, data_dbm, label='data')
        ax1.loglog(T, bb, label = "gaussian noise")
        rw = 0.05*np.sqrt(T/3)
        ax1.loglog(T, np.sqrt(rw**2 + bb**2), label = "total", linewidth = 3, color = 'red')
        ax1.set_title("DBM")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("dBm")
        ax1.legend()

    plt.show()

if __name__ == "__main__":
    filename = os.path.join(THIS_FOLDER, "Long_log_07_04_2023_17_09_02.csv")
    time, dist, ids, dbm, with_dbm = load_data(filename)

    # plot_data(ids, time, dist, dbm, with_dbm)
    val_idx = np.unique(ids)
    for idx in val_idx:
        new_ids = ids[ids == idx]
        new_dist = dist[ids == idx]
        new_time = time[ids == idx]
        new_dbm = dbm[ids == idx]
        plot_data(new_ids, new_time, new_dist, new_dbm, with_dbm)