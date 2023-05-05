#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import contextlib

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = THIS_FOLDER #os.path.join(THIS_FOLDER, 'old')

def load_single_file(filename):
    RX = np.array([])
    FP = np.array([])
    Q = np.array([])
    # Charger le fichier CSV
    data = np.genfromtxt(filename, delimiter=';', skip_header=1)
    with_RX = False; with_all = False
    if data.shape[1] >= 4: with_RX = True
    if data.shape[1] > 4: with_all = True

    # Extraire les colonnes ID, temps et distance
    ids = data[:, 0]
    times_ms = data[:, 1]
    distances = data[:, 2]

    # Convertir les temps en secondes et soustraire le temps de départ
    time = times_ms / 1000.0  #/ 60. /60.
    dist = distances
    time = time - np.min(time)

    if with_RX:
        RXs = data[:, 3]
        RX = RXs

    if with_all:
        FPs = data[:, 4]
        FP = FPs
        Qs = data[:, 5]
        Q = Qs


    return time, dist, ids, RX, with_RX, FP, Q, with_all

def load_multiple_files():
    time = np.array([])
    dist = np.array([])
    ids = np.array([])
    RX = np.array([])
    # Parcourir tous les fichiers CSV dans le dossier "logs"
    with_RX = False
    for filename in os.listdir(LOGS_FOLDER):
        # if filename.endswith('.csv'):
        if filename.startswith('Long_log_04_04_2023'): #or filename.startswith('Long_log_02_04') or filename.startswith('Long_log_03_04'):
            filepath = os.path.join(LOGS_FOLDER, filename)
            file_time, file_dist, file_ids, file_RX, with_RX, file_FP, file_Q, file_with_all = load_single_file(filepath)
            time = np.hstack((file_time, time))
            ids = np.hstack((file_ids, ids))
            dist = np.hstack((file_dist, dist))
            if with_RX:
                RX = np.hstack((file_RX, RX))

    # Obtenir les index triés en fonction de la valeur de temps
    sorted_indices = np.argsort(time)

    # Réorganiser les tableaux time et dist selon les index triés
    time = time[sorted_indices]/1000
    dist = dist[sorted_indices]
    ids = ids[sorted_indices]
    if with_RX:
        RX = RX[sorted_indices]
        tab = np.vstack((ids,time,dist,RX))
    else:
        tab = np.vstack((ids, time))
    header = "n°Anchor, Time (s), Distance (m), RX, FP, Q"
    np.savetxt(f"{THIS_FOLDER}/{filename}_all.csv", tab.T, delimiter=";", header=header)

    return time, dist, ids, RX

def load_data(filename):
    multiple_files = False
    if multiple_files:
        return load_multiple_files()
    else:
        # Charger le fichier CSV
        return load_single_file(filename)

def plot_data(ids, time, dist, RX, with_RX, FP, Q, with_all, sigma_rw = 0.00005,display_allan=1, display_dbm=1, display_quality=1):
    # Tracer la distance en fonction du temps sans mask
    idx_start = time.shape[0]//4
    idx_end = -1 # dist.shape[0] - time.shape[0]//7 #-1 #
    time = time[idx_start:idx_end] - time[idx_start]
    dist = dist[idx_start:idx_end]

    print(f"Moyenne : {np.mean(dist)}")
    print(f"Ecart-Type : {np.std(dist)}")

    if display_dbm:
        if with_all:
            RX = RX[idx_start:idx_end]
            FP = FP[idx_start:idx_end]
            Q = Q[idx_start:idx_end]

            #Ploting the Allan deviation
            fig, axs = plt.subplots(1,3)
            ax0 = axs[1]
            ax0.plot(time/60/60, RX)
            ax0.set_xlabel("Time [h]")
            ax0.set_ylabel("dBm")
            ax0.set_title("RX")
            ax0.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            ax0.grid()

            ax1 = axs[2]
            ax1.plot(time/60/60, FP)
            ax1.set_xlabel("Time [h]")
            ax1.set_ylabel("dBm")
            ax1.set_title("FP")
            ax1.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            ax1.grid()

            ax = axs[0]
            fig.suptitle(f"Déviation d'Allan for anchor {int(ids[0])}")
        
            ax.scatter(time/60/60, dist, s=0.1)
            ax.set_xlabel("Time [h]")
            ax.set_ylabel("m")
            ax.set_title("Measurements")
            ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            ax.grid()
        else:
            fig, ax = plt.subplots(1,1)
            fig.suptitle(f"Déviation d'Allan for anchor {int(ids[0])}")
        
            ax.scatter(time/60/60, dist, s=0.1)
            ax.set_xlabel("Time [h]")
            ax.set_ylabel("m")
            ax.set_title("Measurements")
            ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            ax.grid()

        

    with contextlib.redirect_stdout(None), contextlib.suppress(ImportError):
        import qrunch

    Frequency = 1 #/np.mean(np.diff(time))
    T, data, std = qrunch.allan_deviation(dist,Frequency)

    print(f"Frequency = {Frequency}\n")

    sigma_bb = std[0]
    bb = sigma_bb/np.sqrt(T)
    rw = sigma_rw*np.sqrt(T/3)

    if display_allan:
        fig, ax = plt.subplots(1,1)
        ax.loglog(T/3600, data, label = "allan deviation")

        ax.loglog(T/3600, bb, label = "gaussian noise")
        ax.loglog(T/3600, rw, label = "random walk")

        total = np.sqrt(bb**2+ rw**2)
        ax.loglog(T/3600, total, label = "total", linewidth = 3, color = 'red')

        ax.set_xlabel('h')
        ax.set_ylabel('m')
        ax.set_title('Allan Deviation for anchor {}'.format(int(ids[0])))

        plt.legend()

    if display_quality:
        if with_all:
            fig, ax = plt.subplots(1,2)
            ax0 = ax[0]
            ax1 = ax[1]
            ax0.plot(time/3600, RX - FP, label='diff power [dbM]')
            ax0.set_title("RX - FP")
            ax0.set_ylabel("dBM")
            ax0.set_xlabel("time [h]")
            ax0.legend()

            ax1.plot(time/3600, Q, label = 'quality (FP2/STD)')
            ax1.set_title("Quality of signal")
            ax1.set_ylabel("ua")
            ax1.set_xlabel("time [h]")
            ax1.legend()
        # except:
        #     print("Nothing remains")
        



if __name__ == "__main__":
    filenames = []
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_24_03_2023_16_44_05.csv")] #anchor 80 LOS, moyenne sur trois données
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_05_04_2023_17_23_38.csv")] #80/81 LOS
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_07_04_2023_17_09_02.csv")] #80/81/82/83 LOS
    LOS_80 = os.path.join(THIS_FOLDER, "Long_log_04_04_2023_17_18_22.csv") #anchor 80 LOS, donnée brute
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_11_04_2023_17_10_41.csv")] #80 LOS 7h
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_13_04_2023_17_28_39.csv")] #82 LOS 13h
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_17_04_2023_17_26_57.csv")] #los/nlos
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_18_04_2023_17_15_32.csv")] #?    
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_19_04_2023_17_26_08.csv")] #?
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_21_04_2023_17_53_22.csv")] #los/nlos : 80 bureau thomas, 81 salle réu, 82/82 en LOS
    NLOS_80 = os.path.join(THIS_FOLDER, "Long_log_27_04_2023_16_48_12.csv") #anchor 80 NLOS
    filenames = [LOS_80, NLOS_80]
    # filenames = [os.path.join(THIS_FOLDER, "Long_log_02_05_2023_17_19_06.csv")] #anchor 80 LOS, f = 10Hz, mean of 3 datas

    for filename in filenames:
        time, dist, ids, RX, with_RX, FP, Q, with_all = load_data(filename)
        time = np.arange(0,dist.shape[0],1)
        masked = 0
        display_allan = 0
        display_quality = 1
        display_dbm = 1

        # plot_data(ids, time, dist, RX, with_RX)
        val_idx = np.unique(ids)
        for idx in val_idx:
            print("Anchor n°{}\n".format(idx))

            ## Apply filter
            if masked:
                alp = 1
                # print(alp*np.std(dist) + np.mean(dist))
                # mask = np.abs(dist[ids == idx] - np.mean(dist[ids == idx])) > alp*np.std(dist[ids == idx])
                mask = np.abs(np.diff(dist[ids == idx])) > 10
                mask = np.hstack((True, mask))
                # mask = (RX - FP < 0) #mask |
                # mask = mask | (Q < 80)
                # mask = mask | (dist <= 0) #
                # mask = RX[ids == idx] < -55
                # mask = Q[ids == idx] < 150
                # print(f"The mask deleted {int(time[ids == idx][~mask].shape[0]/time[ids == idx].shape[0]*100)/100}% of values")

                new_ids = ids[ids == idx][~mask]
                new_dist = dist[ids == idx][~mask]
                new_time = time[ids == idx][~mask]
                if with_all:
                    new_RX = RX[ids == idx][~mask]
                    new_FP = FP[ids == idx][~mask]
                    new_Q = Q[ids == idx][~mask]
                    new_FP = FP[ids == idx][~mask]
                    
                    plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all)
                elif with_RX:
                    new_RX = RX[ids == idx][~mask]
                    plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False)
                else:
                    plot_data(new_ids, new_time, new_dist, np.array([]), False, np.array([]), np.array([]), False)
            
            else:
                new_ids = ids[ids == idx]
                new_dist = dist[ids == idx]
                new_time = time[ids == idx]
                if with_all:
                    new_RX = RX[ids == idx]
                    new_FP = FP[ids == idx]
                    new_Q = Q[ids == idx]
                    new_FP = FP[ids == idx]
                    plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all)
                elif with_RX:
                    new_RX = RX[ids == idx]
                    plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False)
                else:
                    plot_data(ids, time, dist, np.array([]), False, np.array([]), np.array([]), False)
    plt.show()