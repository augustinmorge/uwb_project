import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pickle
import os

sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))

# test = '28_06_2023' 
# test = '03_07_2023'
# test = '05_07_2023'
test = '11_07_2023'
# test = '17_07_2023_2'
# test = '17_07_2023'
# test = '26_07_2023'

# Charger le dictionnaire à partir du fichier
filename = f"\\..\\{test}\\{test}_anchor_interp_data.pkl"
current_directory = os.path.dirname(__file__)
filepath = current_directory + filename
with open(filepath, 'rb') as file:
    anchor_interp_data = pickle.load(file)
    

display_rxfp = 1
display_quality = 0
display_distance = 0

if display_rxfp:
    figrf2, axsrf2 = plt.subplots(2,2)
    figrf2.suptitle(f"RX - FP Histogramme - {test}")
    alpha_rxfp = 2

if display_quality:
    figq2, axsq2 = plt.subplots(2,2)
    figq2.suptitle(f"Quality Histogramme - {test}")
    alpha_q = 50

if display_distance:
    figd2, axsd2 = plt.subplots(2,2)
    figd2.suptitle("d_meas_xpf Histogramme")

# fig_h2, axs_h2 = plt.subplots(2,2)
# fig_h2.suptitle(f"Histogramme error depending on direction\n{test}")



for id in np.arange(6016, 6020):

    # The beacon used
    b = anchor_interp_data[id]

    # Calculer la distance entre la centrale et le balise actuel
    # d_lbl = np.sqrt((b['ins_x'] - b['beacon_x'])**2 +
    #                 (b['ins_y'] - b['beacon_y'])**2 +
    #                 (b['ins_z'] - b['beacon_depths'])**2)
    
    nid = id - 6016
    
    # Create arrays to store binned values and quantiles


    
    mask_innov = np.abs(np.abs(b['Innov_o'])) < 2 # - np.mean(b['Innov_o'])) < 3*np.std(b['Innov_o'])
    if display_rxfp:
        axrf2 = axsrf2[nid//2, nid%2]
        # RXFP = b['RXPower'] - b['FPPower']
        RXFP = b['RXPower_FPPower']
        bins_rx_fp = np.arange(max(min((RXFP)),-1000), max((RXFP)), alpha_rxfp)
        quantiles_rx_fp = []
        valid_pos = []
        # RXFP = RXFP + np.mean(b['Innov_o'][mask_innov])

        # Calculate the quantiles for each bin of RX - FP
        for i in range(len(bins_rx_fp) - 1):
            mask = np.logical_and((RXFP) >= bins_rx_fp[i], (RXFP) < bins_rx_fp[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                valid_pos.append((bins_rx_fp[i+1] + bins_rx_fp[i])/2)
                # quantiles = np.percentile(innov_, [0, 17, 50, 83, 100]) #1 sigma
                quantiles = np.percentile(innov_, [5, 17, 50, 83, 95]) #2sigma
                quantiles_rx_fp.append(quantiles)
        
        positions_rxfp = np.array(valid_pos)

        bp_rx_fp = axrf2.boxplot([q for q in quantiles_rx_fp if len(q) > 0],
                                positions=positions_rxfp[:len(quantiles_rx_fp)],
                                widths=alpha_rxfp * 0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_rx_fp['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_rx_fp['medians']:
            median.set(color='red')

        axrf2.set_ylabel("Innovation")
        if nid >= 2: axrf2.set_xlabel("RX - FP")
        axrf2.set_title(f"{hex(int(id))}")
        axrf2.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Limit to 2 significant figures

        axrf2.plot(positions_rxfp, np.mean(b['Innov_o'][mask_innov])*np.ones(positions_rxfp.shape))
        axrf2.set_xlim([0, np.max(positions_rxfp)])
        axrf2.set_ylim([-0.5, 0.5])

        # # Affichage du dernier plot dans une nouvelle fenêtre
        # if id == 6019:
        #     plt.figure()
        #     bp_rx_fp = plt.boxplot([q for q in quantiles_rx_fp if len(q) > 0],
        #                         positions=positions_rxfp[:len(quantiles_rx_fp)],
        #                         widths=alpha_rxfp * 0.7,
        #                         showfliers=False,
        #                         patch_artist=True)

        #     boxes = bp_rx_fp['boxes']
        #     medians = bp_rx_fp['medians']

        #     for box in boxes:
        #         box.set(facecolor='lightyellow')

        #     for median in medians:
        #         median.set(color='red')

        #     plt.ylabel("Innovation [m]", fontsize = 18)
        #     plt.xlabel("RX - FP [dbm]", fontsize = 18)
        #     plt.title(f"Evolution de l'erreur en fonction de RX - FP pour une ancre", fontsize = 18)
        #     plt.tick_params(axis='both', which='major', labelsize=18) 
        #     plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Limit to 2 significant figures

        #     plt.xlim([0, np.max(positions_rxfp)])
        #     plt.ylim([-0.5, 0.5])

        #     x_ticks_interval = 2  # Définir l'intervalle souhaité
        #     plt.xticks(ticks=positions_rxfp[::x_ticks_interval])

        #     # Ajouter une légende
        #     plt.legend([boxes[0], medians[0]], ['Boîtes', 'Médianes'], fontsize = 18)

        #     plt.show()

    if display_quality:
        axq2 = axsq2[nid//2, nid%2]
        bins_quality = np.arange(min(b['Quality']), max(b['Quality']), alpha_q)
        quantiles_quality = []
        valid_pos = []

        # Calculate the quantiles for each bin of Quality
        for i in range(len(bins_quality) - 1):
            mask = np.logical_and(b['Quality'] >= bins_quality[i], b['Quality'] < bins_quality[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                valid_pos.append((bins_quality[i+1] + bins_quality[i])/2)
                quantiles = np.percentile(innov_, [0, 17, 50, 83, 100])
                quantiles_quality.append(quantiles)

        # Create the boxplot for Quality
        positions_q = np.array(valid_pos)

        bp_quality = axq2.boxplot([q for q in quantiles_quality if len(q) > 0],
                        positions=positions_q[:len(quantiles_quality)],
                        widths=alpha_q * 0.7,
                        showfliers=False,
                        patch_artist=True)

        for box in bp_quality['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_quality['medians']:
            median.set(color='red')

        axq2.set_ylabel("Erreur")
        if nid >= 2:axq2.set_xlabel("Quality")
        axq2.set_title(f"{hex(int(id))}")
        axq2.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Limit to 2 significant figures
        axq2.plot(positions_q, np.mean(b['Innov_o'][mask_innov])*np.ones(positions_q.shape))
        axq2.set_xlim([0, np.max(positions_q)])
        axq2.set_ylim([-0.5, 0.5])

        # if id == 6016:
        #     plt.figure()
        #     bp_quality = plt.boxplot([q for q in quantiles_quality if len(q) > 0],
        #                         positions=positions_q[:len(quantiles_quality)],
        #                         widths=alpha_q * 0.7,
        #                         showfliers=False,
        #                         patch_artist=True)

        #     boxes = bp_quality['boxes']
        #     medians = bp_quality['medians']

        #     for box in boxes:
        #         box.set(facecolor='lightyellow')

        #     for median in medians:
        #         median.set(color='red')

        #     plt.ylabel("Innovation [m]", fontsize = 18)
        #     plt.xlabel("Quality factor [dbm]", fontsize = 18)
        #     plt.title(f"Evolution de l'erreur en fonction de f2/std pour une ancre", fontsize = 18)
        #     plt.tick_params(axis='both', which='major', labelsize=18)  
        #     plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Limit to 2 significant figures
        #     x_ticks_interval = 3  # Définir l'intervalle souhaité
        #     plt.xticks(ticks=positions_q[::x_ticks_interval])
        #     plt.xlim([0, np.max(positions_q)])
        #     # plt.ylim([-0.5, 0.5])

        #     # Ajouter une légende
        #     plt.legend([boxes[0], medians[0]], ['Boîtes', 'Médianes'], fontsize = 18)

        #     plt.show()

    if display_distance:
        ### Display the error with the distance ###
        alpha_d = 20
        # bins_d = np.arange(np.floor(min(b['d_meas_xpf'])), np.ceil(max(b['d_meas_xpf'])), alpha_d)
        bins_d = np.arange(0, np.ceil(max(b['d_meas_xpf'])), alpha_d)
        axd2 = axsd2[nid//2, nid%2]
        valid_pos = []
        quantiles_d = []

        # Calculate the quantiles for each bin of d_meas_xpf
        for i in range(len(bins_d) - 1):
            mask = np.logical_and(b['d_meas_xpf'] >= bins_d[i], b['d_meas_xpf'] < bins_d[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                # quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles = np.percentile(innov_, [5, 17, 50, 83, 95]) #2sigma
                quantiles_d.append(quantiles)
                valid_pos.append((bins_d[i+1] + bins_d[i])/2)

        positions_d = np.array(valid_pos)
        bp_d = axd2.boxplot([q for q in quantiles_d if len(q) > 0],
                        positions=positions_d[:len(quantiles_d)],
                        widths=alpha_d * 0.7,
                        showfliers=False,
                        patch_artist=True)

        for box in bp_d['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_d['medians']:
            median.set(color='red')

        axd2.set_ylabel("Innovation")
        axd2.set_xlabel("lbl_range")
        axd2.set_title(f"{hex(int(id))}")
        axd2.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))  # Limit to 0 significant figures
        axd2.plot(bins_d, np.mean(b['Innov_o'][mask_innov])*np.ones(bins_d.shape))
        axd2.set_ylim([-0.5,0.5])





    ### ###
    # orientation = sawtooth(np.arctan2((b["beacon_y"] - b["ins_y"]),(b["beacon_x"] - b["ins_x"])) - np.pi/2 - b["heading"])

    # ax_h2 = axs_h2[nid//2, nid%2]
    # alpha_o = 0.5

    # quantiles_orientation = []
    # bins_orientation = np.arange(min(orientation), max(orientation), alpha_o)

    # # Calculate the quantiles for each bin of Quality
    # for i in range(len(bins_orientation) - 1):
    #     mask = np.logical_and(orientation >= bins_orientation[i], orientation < bins_orientation[i+1])
    #     innov_ = b['Innov_o'][mask]
    #     if len(innov_) > 0:
    #         quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
    #         quantiles_orientation.append(quantiles)

    # # Create the boxplot for Quality
    # positions_q = bins_orientation[:-1]
    # bp_quality = ax_h2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_orientation if len(q) > 0],
    #                         positions=positions_q[:len(quantiles_orientation)],
    #                         widths=alpha_o*0.7,
    #                         showfliers=False,
    #                         patch_artist=True)

    # for box in bp_quality['boxes']:
    #     box.set(facecolor='lightyellow')

    # for median in bp_quality['medians']:
    #     median.set(color='red')

    # ax_h2.set_ylabel("Erreur")
    # ax_h2.set_xlabel("Orientation")
    # ax_h2.set_title(f"{hex(int(id))}")
    # ax_h2.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))  # Limit to 1 significant figure
    # ax_h2.plot(bins_orientation, np.mean(b['Innov_o'][mask_innov])*np.ones(bins_orientation.shape))

plt.show()


