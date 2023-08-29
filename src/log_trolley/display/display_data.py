import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import os
# from import_data import *

from scipy.optimize import curve_fit

def sinus(x, amplitude, phase, offset):
    return amplitude * np.sin(x + phase) + offset

display_distance = 0
display_direction = 0
display_rxfp = 1
display_quality = 0
display_innov = 0
display_offset = 0
display_speed_linear = 0
display_orientation = 0
display_speed_turn = 0

import pickle

# TEST = ['28_06_2023']
# TEST = ['03_07_2023']
# TEST = ['05_07_2023']
TEST = ['11_07_2023']
# TEST = ['17_07_2023_2']
# TEST = ['26_07_2023']

# TEST = ['28_06_2023', '03_07_2023', '05_07_2023', '11_07_2023', '17_07_2023_2', "26_07_2023"]

for test in TEST:
    # Charger le dictionnaire à partir du fichier
    filename = f"\\..\\{test}\\{test}_anchor_interp_data.pkl"
    current_directory = os.path.dirname(__file__)
    filepath = current_directory + filename
    with open(filepath, 'rb') as file:
        anchor_interp_data = pickle.load(file)

    for id in np.arange(6016,6020,1):
        anchor_interp_data[id]['Innov_o'] = anchor_interp_data[id]['Innov_o']*100
        anchor_interp_data[id]['lbl_range'] = anchor_interp_data[id]['lbl_range']*100
        # anchor_interp_data[id]['d_meas_xpf'] = anchor_interp_data[id]['d_meas_xpf']*100

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

    sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))

    if display_distance:
        figd, axsd = plt.subplots(2,2)
        figd.suptitle("Distance")
        fig_err, axes_err = plt.subplots(2,2)
        fig_err.suptitle(f"{test}")
        
    if display_innov:
        fig_d, axes_d = plt.subplots(2, 4, figsize=(10, 10))
        fig_d.suptitle(f"{test}")

    if display_direction:
        fig_h, axs_h = plt.subplots(2,2)
        fig_h.suptitle(f"Error depending on direction\n{test}")

    if display_quality:
        fig_q, axs_q = plt.subplots(2,2)
        fig_q.suptitle(f"Error depending on quality\n{test}")

    if display_rxfp:
        fig_rxfp, axs_rxfp = plt.subplots(2,2)
        fig_rxfp.suptitle(f"Error depending on RX - FP\n{test}")

    if display_speed_linear:
        fig_s, axs_s = plt.subplots(2,2)
        fig_s.suptitle(f"Error depending on linear speed\n{test}")

    if display_speed_turn:
        fig_st, axs_st = plt.subplots(2,2)
        fig_st.suptitle(f"Error depending on angular speed\n{test}")

    if display_orientation:
        fig_or, axs_or = plt.subplots(2,2)
        fig_or.suptitle(f"Error depending on orientation\n{test}")

    for id in np.arange(6016, 6020):

        # The beacon used
        b = anchor_interp_data[id]

        # Calculer la distance entre la centrale et le balise actuel
        d_lbl = np.sqrt((b['ins_x'] - b['beacon_x'])**2 +
                        (b['ins_y'] - b['beacon_y'])**2 +
                        (b['ins_z'] - b['beacon_depths'])**2)
        
        nid = id - 6016
        
        if display_distance:
            axd = axsd[nid//2, nid%2]
            axd.set_title(f"Distance {id}")
            axd.scatter(b['time'], b['lbl_range'], label = 'distance',s=1)
            axd.set_ylabel("distance [cm]")
            axd.set_xlabel("time [s]")

            ### Display the error with the distance ###
            ax_err = axes_err[nid//2, nid%2]
            fig_err.suptitle(f"Innovation en fonction de la distance\n{test}")
            mask = np.abs(b["Innov_o"]) < 5*100 #(np.abs(b["Innov_o"] - np.mean(b["Innov_o"])) < 3*np.std(b["Innov_o"]))

            ax_err.set_title(f'Beacon ID {hex(int(id))}')
            ax_err.scatter(b['d_meas_xpf'][mask], b['Innov_o'][mask], label = 'Innov(d)', s = 1)
            ax_err.set_ylabel("Innovation [cm]")
            ax_err.set_xlabel("distance [m]")
            # ax_err.set_xlim([-2,175])
            # ax_err.set_ylim([-5,5])
            # ax_err.set_ylim([-1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o']),1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o'])])
            plot_polynomial_regression(ax_err, b['d_meas_xpf'][mask], b['Innov_o'][mask], [1])

        ### ###

        if display_innov:
            ax_d = axes_d[0,id - 6016]
            ax2_d = axes_d[1,id - 6016]

            # Tracer les estimations de distance pour le balise actuel
            ax_d.set_title(f'Beacon ID {hex(int(id))}')
            ax_d.scatter(b['time'], b['d_meas_xpf']*100 - b["Innov_o"], label='d(GPS - anchor)', marker='x', color='blue', s=1)
            ax_d.scatter(b['time'], b['d_meas_xpf']*100, label='LBL - Range (m)', marker='x', color='orange', s=1)

            mask = np.abs(b["Innov_o"]) < 50
            # mask = np.array([True]*b['time'].shape[0])
            # ax2_d.scatter(b['time'][mask], b["Innov_o"][mask], label='Innovation (m)', marker='x', color='black', s=1)
            ax2_d.plot(b['time'][mask], b["Innov_o"][mask], label='Innovation (m)')
            ax2_d.plot(b['time'][mask], np.mean(b["Innov_o"][mask])*np.ones(b['time'][mask].shape[0]), label=f'mean = {int(np.mean(b["Innov_o"][mask])*100)/100}', color='red')
            ax2_d.set_ylim([-100,100])
            ax2_d.set_xlabel("Time [s]")

            # Configurer les propriétés du sous-graphique
            ax_d.set_ylabel('Distance [cm]')
            ax_d.legend()

            ax2_d.set_ylabel('Distance [cm]')
            ax2_d.legend()

            # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
            print(f"For beacon {hex(int(id))} the mean error is {np.mean(b['Innov_o'])}; the sd of {np.std(b['Innov_o'])}")

        if display_direction:
            ### Display heading ###
            ax_h = axs_h[nid//2, nid%2]
            # start_idx = b['end_idx_ali']
            start_idx = 0
            orientation = sawtooth(np.arctan2((b["beacon_y"][start_idx:] - b["ins_y"][start_idx:]),(b["beacon_x"][start_idx:] - b["ins_x"][start_idx:])) - np.pi/2 - b["heading"][start_idx:])
            # orientation = b['heading'][start_idx:]
            ax_h.scatter(orientation, b["Innov_o"][start_idx:], s=0.5, label='data')
            ax_h.set_xlabel("Direction [rad]")
            ax_h.set_ylabel("Innovation")
            ax_h.set_title(hex(int(id)))
            ax_h.set_ylim([-100,100])

            mask = np.logical_and(b["Innov_o"][start_idx:] >= -100, b["Innov_o"][start_idx:] <= 100)

            params, params_covariance = curve_fit(sinus, orientation[mask], b["Innov_o"][start_idx:][mask])
            amplitude, phase, offset = params

            formula = f'y = {amplitude:.2f} * sin(x + {phase:.2f}) + {offset:.2f}'

            # X_fit = np.linspace(0, 2*np.pi, 100)
            X_fit = np.linspace(-np.pi, np.pi, 100)
            Y_fit = sinus(X_fit, amplitude, phase, offset)
            ax_h.plot(X_fit, Y_fit, color='red', label='Courbe ajustée')
            ax_h.text(0.05, 0.9, formula, transform=ax_h.transAxes, fontsize=10) 
            ax_h.legend(loc='upper right')
            # plt.ylim([-1,1])

        if display_quality:
            ### Display the error with the quality ###
            ax_q = axs_q[nid//2, nid%2]
            ax_q.set_title(f'Beacon ID {hex(int(id))}')
            ax_q.scatter(b['Quality'], b['Innov_o'], label = 'Innov(q)', s = 1)
            ax_q.set_ylabel("Innovation [cm]")
            ax_q.set_xlabel("Quality")
            ax_q.set_ylim([-100,100])
            # mask = (b['Innov_o'] > -2*100) & (b['Innov_o'] < 2*100)
            # try:
            #     plot_polynomial_regression(ax_q, b['Quality'][mask], b['Innov_o'][mask], [1])
            # except:
            #     print("Impossible to do a linear regression")

        if display_rxfp:
            ### Display the error with RX - FP ###
            ax_rxfp = axs_rxfp[nid//2, nid%2]
            ax_rxfp.set_title(f'Beacon ID {hex(int(id))}')
            # ax_rxfp.scatter(b['RXPower_FPPower'], b['Innov_o'], label = 'Innov(RX-FP)', s = 1)
            ax_rxfp.scatter(b['RXPower']-b['FPPower'], b['Innov_o'], label = 'Innov(RX-FP)', s = 1)
            ax_rxfp.set_ylabel("Innovation [cm]")
            ax_rxfp.set_xlabel("RX - FP")
            ax_rxfp.set_ylim([-100,100])
            # ax_rxfp.set_xlim([0,np.max(b['RXPower_FPPower'])])
            ax_rxfp.set_xlim([0,np.max(b['RXPower']-b['FPPower'])])
            # mask = (b['Innov_o'] > -2*100) & (b['Innov_o'] < 2*100) & (b['RXPower_FPPower'] > 0)
            # try:
            #     plot_polynomial_regression(ax_rxfp, b['RXPower_FPPower'][mask], b['Innov_o'][mask], [1])
            # except:
            #     print("Impossible to do a linear regression")
        
        if display_speed_turn:
            ax_st = axs_st[nid//2, nid%2]
            ax_st.set_title(f'Beacon ID {hex(int(id))}')
            # ax_st.scatter(b['FullCompensatedRotRateGeoX'], b['Innov_o'], label = 'w_x', s = 1)
            # ax_st.scatter(b['FullCompensatedRotRateGeoY'], b['Innov_o'], label = 'w_y', s = 1)
            ax_st.scatter(b['FullCompensatedRotRateGeoZ'], b['Innov_o'], label = 'w_z', s = 1)
            ax_st.set_ylabel("Innovation [cm]")
            ax_st.set_xlabel("Speed [m/s]")
            ax_st.set_ylim([-100,100])
            ax_st.legend()

        if display_speed_linear:
            ax_s = axs_s[nid//2, nid%2]
            ax_s.set_title(f'Beacon ID {hex(int(id))}')
            ax_s.scatter(b['speedEast'], b['Innov_o'], label = 'speed_x', s = 1)
            ax_s.scatter(b['speedNorth'], b['Innov_o'], label = 'speed_y', s = 1)
            ax_s.scatter(b['speedVertical'], b['Innov_o'], label = 'speed_z', s = 1)
            ax_s.set_ylabel("Innovation [cm]")
            ax_s.set_xlabel("Speed [m/s]")
            ax_s.set_ylim([-100,100])
            ax_s.legend()
        
        
        if display_orientation:
            ### Display the error with RX - FP ###
            ax_or = axs_or[nid//2, nid%2]
            ax_or.set_title(f'Beacon ID {hex(int(id))}')
            ax_or.scatter(sawtooth(np.arctan2((b['beacon_y'] - b['ins_y']),(b['beacon_x'] - b['ins_x'])))*180/np.pi, b['Innov_o'], label = 'orientation', s = 1)
            ax_or.set_ylabel("Innovation [cm]")
            ax_or.set_xlabel("Orientation [°]")
            ax_or.legend()
            ax_or.set_ylim([-100,100])
            # plot_polynomial_regression(ax_or, b['RXPower_FPPower'], b['Innov_o'], [1])



    # X = anchor_interp_data[6019]["heading"][b['end_idx_ali']:,]
    # Y = anchor_interp_data[6019]["Innov_o"][b['end_idx_ali']:,]

    # print(X,Y)

    # mask = np.logical_and(Y >= -50, Y <= 50)
    # X = X[mask]
    # Y = Y[mask]

    # params, params_covariance = curve_fit(sinus, X, Y)
    # amplitude, phase, offset = params

    # formula = f'y = {amplitude:.2f} * sin(x + {phase:.2f}) + {offset:.2f}'

    # X_fit = np.linspace(0, 2*np.pi, 100)
    # Y_fit = sinus(X_fit, amplitude, phase, offset)
    # plt.figure()
    # plt.scatter(X, Y, label='Points donnés')
    # plt.plot(X_fit, Y_fit, color='red', label='Courbe ajustée')
    # plt.legend()
    # plt.xlabel('Cap de la centrale [rad]')
    # plt.ylabel('Innovation [cm]')
    # plt.title('Forme de l\'erreur en fonction du cap')
    # plt.text(0.3, 0.3, formula, transform=plt.gca().transAxes, fontsize=10)  
    # # plt.ylim([-1,1])

    thresold = 50
    if display_offset:
        plt.figure()
    L = {6016 : [], 6017 : [], 6018 : [], 6019 : []}
    for id in np.arange(6016, 6020):
        mask = np.abs(anchor_interp_data[id]["Innov_o"]) < thresold

        for i in range(anchor_interp_data[id]["Innov_o"][mask].shape[0]):
            L[id].append(np.mean(anchor_interp_data[id]['Innov_o'][mask][:i,]))

        t = anchor_interp_data[id]["time"][mask]
        if display_offset:
            plt.plot((t-t[0])/60, np.array(L[id]),label=f'{hex(int(id))}')
            # plt.plot((t[:-1]-t[0])/60, np.diff(np.array(L[id])),label=f'{hex(int(id))}')


    # Write data to offset.txt if not already present and sort by date
    test_threshold_str = f"{test}; {thresold}"
    with open(current_directory + "\offset.txt", "r") as file:
        lines = file.readlines()

    # Check if the test and threshold already exist in the file
    data_exists = False
    for i in range(len(lines)):
        if i > 2:
            line = lines[i]
            if line.split(";")[0] == test and float(line.split(";")[1]) == thresold:
                data_exists = True

    if not data_exists:
        # Append the new data to the lines list
        new_data_line = f"{test_threshold_str}; {L[6016][-1]}; {L[6017][-1]}; {L[6018][-1]}; {L[6019][-1]}\n"
        lines.append(new_data_line)

        # Sort the lines by date and threshold
        sorted_lines = []
        header_lines = []
        for line in lines:
            if line.startswith("#"):
                header_lines.append(line)
            else:
                elements = line.strip().split(";")
                if len(elements) >= 2:
                    try:
                        sorted_lines.append((elements[0], float(elements[1]), line))
                    except ValueError:
                        print(f"Warning: Line '{line.strip()}' has invalid data and will be skipped during sorting.")
        
        sorted_lines.sort(key=lambda item: (item[0], item[1]))
        sorted_lines = [line for _, _, line in sorted_lines]

        # Write the sorted data back to the file, including the header lines
        with open(current_directory + "\offset.txt", "w") as file:
            file.writelines(header_lines)
            file.writelines("\n")
            file.writelines(sorted_lines)

    else:
        print("Data already exists in the file. Skipping write operation.")

    if display_offset:
        plt.title(f"{test}")
        plt.xlabel("time [min]")
        plt.ylabel("offset [cm]")
        plt.legend()

plt.show()