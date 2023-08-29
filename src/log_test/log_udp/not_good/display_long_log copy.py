#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import contextlib

def plot_polynomial_regression(ax, x, y, degrees, label = ""):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    # ax.scatter(x, y, label='Mean data '+label)
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'{eqn}'+label,color='red')
    ax.legend(loc='upper left')


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = THIS_FOLDER #os.path.join(THIS_FOLDER, 'old')

def load_single_file(filename):
    RX = np.array([])
    FP = np.array([])
    Q = np.array([])
    # Charger le fichier CSV
    data = np.genfromtxt(filename, delimiter=';', skip_header=1, dtype='<U15')
    with_RX = False; with_all = False
    print(data)
    try:
        if data.shape[1] >= 4: with_RX = True
        if data.shape[1] > 4: with_all = True
    except:
        return
    # Extraire les colonnes ID, temps et distance
    try:
        ids = data[:, 0].astype(np.float64)
    except:
        ids = np.zeros(data[:,0].shape)
    times_ms = data[:, 1].astype(np.float64)
    distances = data[:, 2].astype(np.float64)

    # Convertir les temps en secondes et soustraire le temps de départ
    time = times_ms / 1000.0  #/ 60. /60.
    # time = time - np.min(time)
    dist = distances

    if with_RX:
        RXs = data[:, 3].astype(np.float64)
        RX = RXs

    if with_all:
        FPs = data[:, 4].astype(np.float64)
        FP = FPs
        Qs = data[:, 5].astype(np.float64)
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

def plot_data(ids, time, dist, RX, with_RX, FP, Q, with_all, sigma_rw = 0.00005,display_allan=1, display_dbm=1, display_quality=1, filename = None):
    # Tracer la distance en fonction du temps sans mask
    idx_start = 0 #time.shape[0]//4
    idx_end = -1 #dist.shape[0] - 10*time.shape[0]//25 #-1 #
    time = time[idx_start:idx_end] - time[idx_start]
    dist = dist[idx_start:idx_end]

    print(f"Moyenne : {np.mean(dist)}")
    print(f"Ecart-Type : {np.std(dist)}")

    if with_all:
        RX = RX[idx_start:idx_end]
        FP = FP[idx_start:idx_end]
        Q = Q[idx_start:idx_end]

    if display_dbm:
        if with_all:
            
            display_all = False
            if display_all:
                # Ploting the Allan deviation
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
            ax.scatter(time/60/60, dist*100,s=1)#, s = 1)
            ax.set_xlabel("Time [h]")
            ax.set_ylabel("m")
            date = filename.split('\\')[-1]
            ax.set_title(f"Measurements for anchor {int(ids[0])}\n{date}")
            ax.set_xlim([np.min(time/60/60), np.max(time/60/60)])
            # plot_polynomial_regression(ax, time/60/60, dist*100, [1])
            ax.grid()
            # for i in range(len(time) - 1):
            #     if time[i+1] - time[i] > 2:
            #         ax.axvline(x=time[i]/60/60, color='red', linestyle='--')

            # Indices des coupures
            # cutoff_indices = np.where(np.diff(time) > 2)[0]

            
            # # Affichage de l'écart de temps entre chaque coupure
            # print("\nÉcart de temps entre chaque coupure (en minutes):")
            # for i, index in enumerate(cutoff_indices):
            #     time_diff = (time[index+1] - time[index]) / 60
            #     print(f"Coupure {i+1}: {time_diff} minutes")
            # print()

            # # Calcul de la moyenne et de l'écart type de dist pour chaque partie
            # for i in range(len(cutoff_indices) + 1):
            #     if i == 0:
            #         part_dist = dist[:cutoff_indices[i]+1]
            #     elif i == len(cutoff_indices):
            #         part_dist = dist[cutoff_indices[i-1]+1:]
            #     else:
            #         part_dist = dist[cutoff_indices[i-1]+1:cutoff_indices[i]+1]

            #     print(f"\nPartie {i+1}:")
            #     print("Moyenne de dist:", np.mean(part_dist))
            #     print("Écart type de dist:", np.std(part_dist))
            #     print()


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

    Frequency = 1/np.mean(np.diff(time))
    try:
        T, data, std = qrunch.allan_deviation(dist,Frequency)
    except:
        print("ça bug pour allan")
        return
    print(f"Frequency = {Frequency}")

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
        ax.set_title('Allan Deviation') # for anchor {}'.format(int(ids[0])))

        plt.legend()

    if display_quality:
        if with_all:
            print(time.shape)
            print(RX.shape)
            print(FP.shape)
            fig, ax = plt.subplots(1,2)
            fig.suptitle(f"Anchor n°{idx}")

            ax0 = ax[0]
            ax1 = ax[1]
            ax0.scatter(time/3600, RX - FP, label='diff power [dbM]', s=1, marker='x')
            # ax0.plot(time/3600, RX - FP, label='diff power [dbM]') #, s=1, marker='x')
            ax0.set_title("RX - FP")
            ax0.set_ylabel("dBM")
            ax0.set_xlabel("time [h]")
            ax0.legend()

            ax1.scatter(time/3600, Q, label = 'quality (FP2/STD)', s=1, marker='x')
            # ax1.plot(time/3600, Q, label = 'quality (FP2/STD)') #, s=1, marker='x')
            ax1.set_title("Quality of signal")
            ax1.set_ylabel("ua")
            ax1.set_xlabel("time [h]")
            ax1.legend()

        print(f"Mean of RX - FP = {np.mean(RX - FP)}; Std of RX - FP = {np.std(RX - FP)}")
        print(f"Mean of the Quality = {np.mean(Q)}; Std of Quality = {np.std(Q)}\n__________\n")
        # except:
        #     print("Nothing remains")
        



if __name__ == "__main__":
    filenames = []
    import glob

    # filenames = [os.path.join(THIS_FOLDER, "17_05_2023_15_35_29_log-all-with-time.csv")] #80: NLOS derriere reu; 81: NLOS contre mur imprimante; 82: Francoise; 83: Dans la salle réu
    # filenames = [os.path.join(THIS_FOLDER, "22_05_2023_12_01_12_log-all-with-time.csv")] 
    # filenames = [os.path.join(THIS_FOLDER, "26_05_2023_17_20_07_log-all-with-time.csv")] 
    # filenames = [os.path.join(THIS_FOLDER, "15_06_2023_11_56_58_log-all-with-time.csv")] #82: LOS à 1.5m environ du tag; #80: NLOS loin derrière la B224
    # filenames = [os.path.join(THIS_FOLDER, "anchor/30_05_2023_17_07_35_log-all-with-time.csv")]
    # filenames = [os.path.join(THIS_FOLDER, "anchor/05_06_2023_11_58_37_log-all-with-time.csv")]
    # filenames = [os.path.join(THIS_FOLDER, "22_06_2023_11_39_47_log-all-with-time.csv"), os.path.join(THIS_FOLDER, "22_06_2023_14_58_05_log-all-with-time.csv")] 
    
    filenames = [os.path.join(THIS_FOLDER, "Long_log_05_05_2023_17_20_26.csv")]
    filenames = glob.glob(os.path.join(THIS_FOLDER, "*.csv"))

    for filename in filenames:
        time, dist, ids, RX, with_RX, FP, Q, with_all = load_data(filename)
        dist = dist/100
        RX = RX/100
        FP = FP/100
        Q = Q/100

        masked = 1
        display_allan = 0
        display_quality = 0
        display_dbm = 1

        sigma_rw = 0.00005

        # plot_data(ids, time, dist, RX, with_RX)
        val_idx = np.unique(ids)
        for idx in val_idx:
            if True: #idx == 1780:
                print("\n__________\nAnchor n°{}\n".format(idx))

                ## Apply filter
                if masked:
                    # alp = 1
                    # print(alp*np.std(dist) + np.mean(dist))
                    # mask = np.abs(dist[ids == idx] - np.mean(dist[ids == idx])) > 1 #alp*np.std(dist[ids == idx])
                    mask = np.abs(np.diff(dist[ids == idx])) > 10


                    # print(np.mean(np.abs(np.diff(time[ids == idx]))))
                    # mask = np.abs(np.diff(time[ids == idx])) > 200
                    mask = np.hstack((True, mask))


                    # mask = mask | (RX[ids == idx] == 0)
                    # mask = dist[ids == idx] < 0
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
                        
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all, sigma_rw, display_allan, display_dbm, display_quality, filename)
                    elif with_RX:
                        new_RX = RX[ids == idx][~mask]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality, filename)
                    else:
                        plot_data(new_ids, new_time, new_dist, np.array([]), False, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality, filename)
                
                else:
                    new_ids = ids[ids == idx]
                    new_dist = dist[ids == idx]
                    new_time = time[ids == idx]
                    if with_all:
                        new_RX = RX[ids == idx]
                        new_FP = FP[ids == idx]
                        new_Q = Q[ids == idx]
                        new_FP = FP[ids == idx]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, new_FP, new_Q, with_all, sigma_rw, display_allan, display_dbm, display_quality, filename)
                    elif with_RX:
                        new_RX = RX[ids == idx]
                        plot_data(new_ids, new_time, new_dist, new_RX, with_RX, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality, filename)
                    else:
                        plot_data(ids, time, dist, np.array([]), False, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality, filename)
    plt.show()