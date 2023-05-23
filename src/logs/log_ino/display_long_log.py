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
    # time = time - np.min(time)
    dist = distances

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
    idx_end = dist.shape[0] - 10*time.shape[0]//25 #-1 #
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

            ## Pour afficher une déviation linéaire au cours du temps
            fig, ax = plt.subplots()
            ax.scatter(time/60/60, dist,s=1)#, s = 1)
            ax.set_xlabel("Time [h]")
            ax.set_ylabel("m")
            ax.set_title("Measurements")
            ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            ax.grid()
            # def plot_polynomial_regression(ax, x, y, degrees, label = ""):
            #     coeffs = [np.polyfit(x, y, degree) for degree in degrees]
            #     ax.scatter(x, y, label='Mean data '+label)
            #     for i, c in enumerate(coeffs):
            #         line_x = np.linspace(min(x), max(x), 10000)
            #         line_y = np.polyval(c, line_x)
            #         r_squared = r2_score(y, np.polyval(c, x))
            #         eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
            #         ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.3f}) \n'+label)
            #     ax.legend(loc='upper left')
            # plot_polynomial_regression(ax, time/60/60, dist, [1])
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

    filenames = [os.path.join(THIS_FOLDER, "17_05_2023_15_35_29_log-all-with-time.csv")] #80: NLOS derriere reu; 81: NLOS contre mur imprimante; 82: Francoise; 83: Dans la salle réu
    # filenames = [os.path.join(THIS_FOLDER, "22_05_2023_12_01_12_log-all-with-time.csv")] 
    # filenames = [os.path.join(THIS_FOLDER, "22_05_2023_17_16_41_log-all-with-time.csv")] 


    for filename in filenames:
        time, dist, ids, RX, with_RX, FP, Q, with_all = load_data(filename)
        dist = dist/100
        RX = RX/100
        FP = FP/100
        Q = Q/100

        masked = 0
        display_allan = 1
        display_quality = 1
        display_dbm = 1

        sigma_rw = 0.00005

        # plot_data(ids, time, dist, RX, with_RX)
        val_idx = np.unique(ids)
        for idx in val_idx:
            if True: #idx == 1780:
                print("Anchor n°{}\n".format(idx))

                ## Apply filter
                if masked:
                    alp = 1
                    # print(alp*np.std(dist) + np.mean(dist))
                    # mask = np.abs(dist[ids == idx] - np.mean(dist[ids == idx])) > 0.5 #alp*np.std(dist[ids == idx])
                    # mask = np.abs(np.diff(dist[ids == idx])) > 10


                    # print(np.mean(np.abs(np.diff(time[ids == idx]))))
                    # mask = np.abs(np.diff(time[ids == idx])) > 200
                    # mask = np.hstack((True, mask))


                    # mask = mask | (RX[ids == idx] == 0)
                    mask = dist[ids == idx] < 0
                    # mask = (RX - FP < 0) #mask |
                    # mask = mask | (Q < 80)
                    # mask = mask | (dist <= 0) #
                    # mask = RX[ids == idx] < -55
                    # mask = Q[ids == idx] < 150
                    # print(f"The mask deleted {int(time[ids == idx][~mask].shape[0]/time[ids == idx].shape[0]*100)/100}% of values")
                    
                    new_ids = ids[ids == idx][~mask]
                    new_dist = dist[ids == idx][~mask]
                    new_time = time[ids == idx][~mask]
                    print(f"Using {int(new_dist.shape[0]/dist[ids == idx].shape[0]*10000)/100}% of data")

                    mask_abs = np.abs(dist[ids == idx] - np.mean(dist[ids == idx])) > 0.5
                    
                    print(f"Data HS {int((np.sum(mask_abs)/dist[ids == idx].shape[0])*10000)/100}% of data")

                    if with_all:
                        new_RX = RX[ids == idx][~mask]
                        new_FP = FP[ids == idx][~mask]
                        new_Q = Q[ids == idx][~mask]
                        new_FP = FP[ids == idx][~mask]
                        
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all, sigma_rw, display_allan, display_dbm, display_quality)
                    elif with_RX:
                        new_RX = RX[ids == idx][~mask]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality)
                    else:
                        plot_data(new_ids, new_time, new_dist, np.array([]), False, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality)
                
                else:
                    new_ids = ids[ids == idx]
                    new_dist = dist[ids == idx]
                    new_time = time[ids == idx]
                    if with_all:
                        new_RX = RX[ids == idx]
                        new_FP = FP[ids == idx]
                        new_Q = Q[ids == idx]
                        new_FP = FP[ids == idx]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all, sigma_rw, display_allan, display_dbm, display_quality)
                    elif with_RX:
                        new_RX = RX[ids == idx]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality)
                    else:
                        plot_data(ids, time, dist, np.array([]), False, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality)
        plt.show()