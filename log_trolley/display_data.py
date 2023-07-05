import os, sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from import_data import *

def plot_polynomial_regression(ax, x, y, degrees, label = ""):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn}\n(R² = {r_squared:.3f}) \n'+label, color = 'red')
    ax.legend(loc='upper left')

def percent(array, mask, name = ""):
    print(f"Use {array[mask].shape[0]/array.shape[0]*100}% of data for {name}")


def display_interp():
    # figrf, axsrf = plt.subplots(2,2)
    # figrf.suptitle("RX - FP")
    # figq, axsq = plt.subplots(2,2)
    # figq.suptitle("Quality")
    figd, axsd = plt.subplots(2,2)
    figd.suptitle("Distance")
    figrf2, axsrf2 = plt.subplots(2,2)
    figrf2.suptitle("RX - FP Histogramme")
    figq2, axsq2 = plt.subplots(2,2)
    figq2.suptitle("Quality Histogramme")

    fig_d, axes_d = plt.subplots(2, 4, figsize=(10, 10))
    fig_err, axes_err = plt.subplots(2,2)
    date = header_lines[2].split("\t")[1]
    fig_err.suptitle(f"{date}")
    fig_d.suptitle(f"{date}")
    figd2, axsd2 = plt.subplots(2,2)
    figd2.suptitle("d_meas_xpf Histogramme")

    fig_h, axs_h = plt.subplots(2,2)
    fig_h.suptitle("Error depending on direction")

    for id in anchor_id:

        # The beacon used
        b = anchor_interp_data[id]

        # Calculer la distance entre l'gps et le balise actuel
        d_lbl = np.sqrt((b['ins_x'] - b['beacon_x'])**2 +
                        (b['ins_y'] - b['beacon_y'])**2 +
                        (b['ins_z'] - b['beacon_depths'])**2)
        
        nid = id - 6016
        
        # axrf = axsrf[nid//2, nid%2]
        # axrf.set_title(f"Erreur en fonction de la distance {id}")
        # axrf.scatter(b['RXPower_FPPower'], b['Innov_o'], label = 'f(err)', s = 0.5, color = 'black')
        # axrf.set_ylabel("Innovation [m]")
        # axrf.set_xlabel("RX - FP")

        # axq = axsq[nid//2, nid%2]
        # axq.set_title(f"Erreur en fonction de la distance {id}")
        # axq.scatter(b['Quality'], b['Innov_o'], label = 'f(err)', s = 0.5, color = 'black')
        # axq.set_ylabel("Innovation [m]")
        # axq.set_xlabel("Quality")

        axd = axsd[nid//2, nid%2]
        axd.set_title(f"Distance {id}")
        axd.plot(b['time'], d_lbl, label = 'distance')
        axd.set_ylabel("distance [m]")
        axd.set_xlabel("time [s]")

        # Create arrays to store binned values and quantiles
        alpha_rxfp = 5
        alpha_q = 100
        bins_rx_fp = np.arange(np.floor(min(b['RXPower_FPPower'])), np.ceil(max(b['RXPower_FPPower'])), alpha_rxfp)
        bins_quality = np.arange(np.floor(min(b['Quality'])), np.ceil(max(b['Quality'])), alpha_q)

        axrf2 = axsrf2[nid//2, nid%2]

        quantiles_rx_fp = []

        # Calculate the quantiles for each bin of RX - FP
        for i in range(len(bins_rx_fp) - 1):
            mask = np.logical_and(b['RXPower_FPPower'] >= bins_rx_fp[i], b['RXPower_FPPower'] < bins_rx_fp[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_rx_fp.append(quantiles)

        positions_rxfp = bins_rx_fp[:-1] + alpha_rxfp/2
        bp_rx_fp = axrf2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_rx_fp if len(q) > 0],
                                positions=positions_rxfp[:len(quantiles_rx_fp)],
                                widths=alpha_rxfp*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_rx_fp['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_rx_fp['medians']:
            median.set(color='red')

        axrf2.set_ylabel("Erreur")
        axrf2.set_xlabel("RX - FP")
        axrf2.set_title(f"{hex(int(id))}")

        axq2 = axsq2[nid//2, nid%2]

        quantiles_quality = []

        # Calculate the quantiles for each bin of Quality
        for i in range(len(bins_quality) - 1):
            mask = np.logical_and(b['Quality'] >= bins_quality[i], b['Quality'] < bins_quality[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_quality.append(quantiles)

        # Create the boxplot for Quality
        positions_q = bins_quality[:-1] + alpha_q/2
        bp_quality = axq2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_quality if len(q) > 0],
                                positions=positions_q[:len(quantiles_quality)],
                                widths=alpha_q*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_quality['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_quality['medians']:
            median.set(color='red')

        axq2.set_ylabel("Erreur")
        axq2.set_xlabel("Quality")
        axq2.set_title(f"{hex(int(id))}")


        ### Display the error with the distance ###
        
        ax_err = axes_err[nid//2, nid%2]
        fig_err.suptitle("Innovation en fonction de la distance")
        ax_err.set_title(f'Beacon ID {hex(int(id))}')
        ax_err.scatter(b['d_meas_xpf'], b['Innov_o'], label = 'Innov(d)', s = 1)
        ax_err.set_ylabel("Innovation [m]")
        ax_err.set_xlabel("distance [m]")
        ax_err.set_xlim([-2,175])
        ax_err.set_ylim([-5,5])
        # ax_err.set_ylim([-1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o']),1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o'])])
        # plot_polynomial_regression(ax_err, b['d_meas_xpf'], b['Innov_o'], [1])
        alpha_d = 20
        # bins_d = np.arange(np.floor(min(b['d_meas_xpf'])), np.ceil(max(b['d_meas_xpf'])), alpha_d)
        bins_d = np.arange(0, 200, alpha_d)
        axd2 = axsd2[nid//2, nid%2]

        quantiles_d = []

        # Calculate the quantiles for each bin of d_meas_xpf
        for i in range(len(bins_d) - 1):
            mask = np.logical_and(b['d_meas_xpf'] >= bins_d[i], b['d_meas_xpf'] < bins_d[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_d.append(quantiles)

        positions_d = bins_d[:-1] + alpha_d/2
        bp_d = axd2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_d if len(q) > 0],
                                positions=positions_d[:len(quantiles_d)],
                                widths=alpha_d*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_d['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_d['medians']:
            median.set(color='red')

        axd2.set_ylabel("Erreur")
        axd2.set_xlabel("d_meas_xpf")
        axd2.set_title(f"{hex(int(id))}")

        ### ###

        ax_d = axes_d[0,id - 6016]
        ax2_d = axes_d[1,id - 6016]

        # Tracer les estimations de distance pour le balise actuel
        ax_d.set_title(f'Beacon ID {hex(int(id))}')
        ax_d.scatter(b['time'], b['d_meas_xpf'] - b["Innov_o"], label='d(GPS - anchor)', marker='x', color='blue', s=1)
        ax_d.scatter(b['time'], b['d_meas_xpf'], label='LBL - Range (m)', marker='x', color='orange', s=1)

        mask = (np.abs(b["Innov_o"] - np.mean(b["Innov_o"])) < 3*np.std(b["Innov_o"]))
        ax2_d.scatter(b['time'][mask], b["Innov_o"][mask], label='Innovation (m)', marker='x', color='black', s=1)
        ax2_d.plot(b['time'][mask], np.mean(b["Innov_o"][mask])*np.ones(b['time'][mask].shape[0]), label=f'mean = {int(np.mean(b["Innov_o"][mask])*100)/100}', color='red')
        ax2_d.set_ylim([-5,5])
        ax2_d.set_xlabel("Time [s]")

        # Configurer les propriétés du sous-graphique
        ax_d.set_ylabel('Distance (m)')
        ax_d.legend()

        ax2_d.set_ylabel('Distance (m)')
        ax2_d.legend()

        # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
        N = b['d_meas_xpf'].shape[0]
        print(f"For beacon {hex(int(id))} the mean error is {np.mean(b['Innov_o'][:N,])}; the sd of {np.std(b['Innov_o'][:N,])}")

        ### Display heading ###
        ax_h = axs_h[nid//2, nid%2]
        ax_h.scatter(sawtooth(np.arctan2((b["beacon_y"] - b["ins_y"]),(b["beacon_x"] - b["ins_x"])) - np.pi/2 - b["heading"]), b["Innov_o"], s=0.5)
        ax_h.set_xlabel("Direction")
        ax_h.set_ylabel("Innovation")
        ax_h.set_title(hex(int(id)))
        ax_h.set_ylim([-5,5])

display_interp()


# Convertir les coordonnées de l'gps en coordonnées cartésiennes
gps_x, gps_y = cartesian_proj(gps_longitude, gps_latitude)

# Convertir les coordonnées des balises en coordonnées cartésiennes
beacon_x, beacon_y = cartesian_proj(beacon_longitudes, beacon_latitudes)

# Créer les sous-graphiques pour chaque balise
unique_beacon_ids = np.unique(beacon_ids)
num_subplots = len(unique_beacon_ids)

from datetime import datetime

def select_time_idx(starting_values_idx, time):
    datetime_objects = [datetime.strptime(t, '%H:%M:%S.%f') for t in time]
    np_datetime_objects = np.array(datetime_objects, dtype='datetime64')
    elapsed_times = np_datetime_objects - np_datetime_objects[0]
    desired_duration = np.timedelta64(starting_values_idx, 's')
    index = np.where(elapsed_times >= desired_duration)[0][0]
    return index

# list_offset = []
# def etalonnage():
#     ## ETALONNAGE ##
    
#     starting_values_idx = int(input("Combien de temps pour l'étalonnage [s] ? "))
#     # datetime_objects = [datetime.strptime(t, '%H:%M:%S.%f') for t in time]
#     # np_datetime_objects = np.array(datetime_objects, dtype='datetime64')
#     # elapsed_times = np_datetime_objects - np_datetime_objects[0]
#     # desired_duration = np.timedelta64(starting_values_idx, 's')
#     # index = np.where(elapsed_times >= desired_duration)[0][0]
#     # print("L'index correspondant à une durée de", starting_values_idx, "secondes est :", index)

#     fig, axes = plt.subplots(2, 4, figsize=(10, 10))
#     date = header_lines[2].split("\t")[1]
#     fig.suptitle(f"{date} avec étalonnage de {starting_values_idx}s")
    
#     for i, beacon_id in enumerate(unique_beacon_ids):
#         ax = axes[0,i]
#         ax2 = axes[1,i]

#         # Filtrer les données pour le balise ID actuel
#         mask = (beacon_ids == beacon_id)

#         mask[0:10] = False
        
#         current_time = time[mask]
#         index = select_time_idx(starting_values_idx, current_time)

#         current_beacon_x = beacon_x[mask]
#         current_beacon_y = beacon_y[mask]
#         current_beacon_depths = beacon_depths[mask]

#         current_gps_x = gps_x[mask]
#         current_gps_y = gps_y[mask]
#         current_gps_altitude = gps_altitude[mask]

#         # Calculer la distance entre l'gps et le balise actuel
#         distance = np.sqrt((current_gps_x - current_beacon_x)**2 +
#                         (current_gps_y - current_beacon_y)**2 +
#                         (current_gps_altitude - current_beacon_depths)**2)


#         ## SET THE OFFSET ##
#         # offset = np.mean(distance[:index,]-lbl_range[mask][:index,])

#         diff_indices = np.concatenate(([True], np.diff(lbl_range[:index]) != 0))
#         offset = np.mean(distance[:index][diff_indices] - lbl_range[mask][:index][diff_indices])



#         list_offset.append([beacon_id, offset])

#         # Tracer les estimations de distance pour le balise actuel
#         ax.set_title(f'Beacon ID {hex(int(beacon_id))}')
#         ax.scatter(current_time, distance, label='d(GPS - anchor)', marker='x', color='blue', s=1)
#         ax.scatter(current_time, lbl_range[mask] + offset, label='LBL - Range (m) + offset', marker='x', color='green', s=1)
#         ax.plot([current_time[index]]*current_time.shape[0], np.linspace(np.min(distance)-50,np.max(distance)+50,current_time.shape[0]),color='purple')

#         ax2.set_title(f'Beacon ID {hex(int(beacon_id))}')
#         ax2.scatter(current_time, distance-(lbl_range[mask]+offset), label='d(GPS - anchor) - LBL - Range (m) + offset', marker='x', color='green', s=1)
#         ax2.plot(current_time, np.mean(distance-(lbl_range[mask]+offset))*np.ones(current_time.shape[0]), label=f'mean = {int(np.mean(distance-(lbl_range[mask]+offset))*100)/100}', color='red')

#         # Configurer les propriétés du sous-graphique
#         ax.set_ylabel('Distance (m)')
#         ax.legend()

#         ax2.set_ylabel('Distance (m)')
#         ax2.legend()

#         # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
#         xticks_indices = np.linspace(0, np.sum(mask), num=4, dtype=int)
#         ax.set_xticks(xticks_indices)
#         ax.set_xticklabels(time[xticks_indices])

#         ax2.set_xticks(xticks_indices)
#         ax2.set_xticklabels(time[xticks_indices])

#         alph = 3
#         ax2.set_ylim([-alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])
#         ax.set_ylim( [min(-alph*np.std(distance) + np.mean(distance),-alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])),\
#                     max( alph*np.std(distance) + np.mean(distance), alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])) ] )

#         N = distance.shape[0]//4
#         print(f"For beacon {hex(int(beacon_id))} the mean error is {np.mean(distance[N:,] - (lbl_range[mask][N:,]+offset))}; the sd of {np.std(distance[N:,] - (lbl_range[mask][N:,]+offset))} and the offset is {offset}")

#     # plt.tight_layout()
# # etalonnage()

# with open(os.path.join(current_directory,f"offset.txt"),"w") as file:
#     file.write("Beacon ID : offset\n")
#     for elem in list_offset:
#         file.write(str(elem[0]) + ":" + str(elem[1]) + "\n")
#     file.close()

if __name__ == "__main__":
    plt.show()