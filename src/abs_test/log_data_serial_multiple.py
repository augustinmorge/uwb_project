#!/usr/bin/python3
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import serial, struct

# Modules pour l'interpolation
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def read_data():
    # Taille totale du buffer d'envoi en bytes
    buffer_size = 22
    
    # Tailles en bytes de chaque donnée dans le buffer
    short_address_size = 2
    range_size = 4
    rx_power_size = 4
    fp_power_size = 4
    quality_size = 4
    timer_size = 4
    
    # Attendre que des données soient disponibles sur la connexion série
    short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]
    ids = ['1780', '1781', '1782', '1783']
    while short_address not in ids: # Attendre de lire l'octet 0xFF
        short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]

    # Lire les données disponibles depuis la connexion série
    buffer = ser.read(buffer_size-short_address_size) # Lire le reste du buffer, moins l'octet déjà reçu

    range_value = struct.unpack('f', buffer[:range_size])[0]
    rx_power = struct.unpack('f', buffer[range_size:range_size+rx_power_size])[0]
    fp_power = struct.unpack('f', buffer[range_size+rx_power_size:range_size+rx_power_size+fp_power_size])[0]
    quality = struct.unpack('f', buffer[range_size+rx_power_size+fp_power_size:range_size+rx_power_size+fp_power_size+quality_size])[0]
    timer = struct.unpack('I', buffer[range_size+rx_power_size+fp_power_size+quality_size:range_size+rx_power_size+fp_power_size+quality_size+timer_size])[0]
    # Retourner un dictionnaire contenant les données
    return {
        'A': short_address,
        'R': range_value,
        'RX': rx_power,
        'FP': fp_power,
        'Q': quality,
        'T': timer
    }


import numpy as np
from sklearn.metrics import r2_score

def plot_polynomial_regression(ax, x, y, degrees):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    ax.scatter(x, y, label='Mean data')
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.3f})')
    ax.legend(loc='upper left')



def main(file, sec = 60):
    
    while True:
        input("Press ENTER to continue\n")
        d = float(input("Please select the distance: "))
        print(f"Measuring distance from {d}m")
        while True:
            b = input("Is it okay ? (y/n)").lower()
            if b == 'y':
                break
            elif b == 'n':
                d = float(input("Please select the distance: "))
                print(f"Measuring distance from {d}m")
            else:
                print("Invalid input, please enter 'y' or 'n'.")
        if d == 0: file.close(); sys.exit()
        input("Press ENTER three times\n")
        input("Press ENTER three times\n")
        input("Press ENTER three times\n")


        print(f"Measuring distance from {d}m")

        t0 = time.time()

        while time.time() - t0 < sec:
            one = read_data()
            print(one)

            if one["A"] == "1780":
                time_anchor1 = float(one["T"]);
                data_anchor1 = float(one["R"]); 
                RX_anchor1 = float(one["RX"])
                FP_anchor1 = float(one["FP"])
                Q_anchor1 = float(one["Q"])
                if data_anchor1 != 0:
                    file.write("1780 ; "+ str(d) + ";" + str(time_anchor1) + ";"+ str(data_anchor1) + ";" + str(RX_anchor1) + ";" + str(FP_anchor1) + ";" + str(Q_anchor1) + "\n")

            if one["A"] == "1781":
                time_anchor2 = float(one["T"]);
                data_anchor2 = float(one["R"]); 
                RX_anchor2 = float(one["RX"])
                FP_anchor2 = float(one["FP"])
                Q_anchor2 = float(one["Q"])
                if data_anchor2 != 0:
                    file.write("1781 ; "+ str(d) + ";" + str(time_anchor2) + ";"+ str(data_anchor2) + ";" + str(RX_anchor2) + ";" + str(FP_anchor2) + ";" + str(Q_anchor2) + "\n")

            if one["A"] == "1782":
                time_anchor3 = float(one["T"]);
                data_anchor3 = float(one["R"]); 
                RX_anchor3 = float(one["RX"])
                FP_anchor3 = float(one["FP"])
                Q_anchor3 = float(one["Q"])
                if data_anchor3 != 0:
                    file.write("1782 ; "+ str(d) + ";" + str(time_anchor3) + ";"+ str(data_anchor3) + ";" + str(RX_anchor3) + ";" + str(FP_anchor3) + ";" + str(Q_anchor3) + "\n")

            if one["A"] == "1783":
                time_anchor4 = float(one["T"]);
                data_anchor4 = float(one["R"]); 
                RX_anchor4 = float(one["RX"])
                FP_anchor4 = float(one["FP"])
                Q_anchor4 = float(one["Q"])
                if data_anchor4 != 0:
                    file.write("1783 ; "+ str(d) + ";" + str(time_anchor4) + ";"+ str(data_anchor4) + ";" + str(RX_anchor4) + ";" + str(FP_anchor4) + ";" + str(Q_anchor4) + "\n")
            
            file.flush()


if __name__ == '__main__':
    import datetime, sys
    doing_test = 1
    nb_anchor = 1

    offset = {1780 : 0, 1781 : 0, 1782 : 0, 1783 : 0}
    # offset = {1780 : 0.086, 1781 : -0.419, 1782 : -0.910, 1783 : 0.659}
    coords = {1780 : {'x' : 1.29, 'y' : 12.543, 'z' : 1.348}, 1781 : {'x' : 0, 'y' : 0, 'z' : 1.342}, \
              1782 : {'x' : -3.167, 'y' : -11.36, 'z' : 1.213}, 1783 : {'x' : 1.1, 'y' : -28.066, 'z' : -1.502}}
    def f_distance(id,d): 
        ###
        # id : l'identifiant de l'ancre
        # d : la distance mesurée entre lancre A et le tag (cf schéma)
        ###
        return np.sqrt((coords[id]['x'] - coords[1780]['x'])**2 + (coords[id]['y'] - (coords[1780]['y'] - d))**2 + (coords[id]['z'] - np.sqrt((coords[1780]['z']**2-0.2294**2)))**2)
    

    date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    if doing_test:
        ser = serial.Serial('COM5', 115200)

        print("Start test..")
        file = open(f"{THIS_FOLDER}/{date_str}_Serial_Test_multiple_points.csv", "w")
        file.write("n°anchor; d_real [m]; time [ms]; d_measured [m]; RX [dbm]; FP [dbm]; Q;\n")

        D = main(file)

        file.close()

    else:
        # filenames = [f"{THIS_FOLDER}/2023_05_02_15_09_14_Test_multiple_points.csv", f"{THIS_FOLDER}/2023_05_03_16_12_38_Test_multiple_points.csv",\
        #              f"{THIS_FOLDER}/2023_04_27_14_17_12_Test_multiple_points.csv"]
        filenames = [f"{THIS_FOLDER}/2023_05_02_15_09_14_Test_multiple_points.csv"]
        for filename in filenames:
            data = np.genfromtxt(filename, delimiter=';', skip_header=1)

            ids = data[:,0]
            d_real = data[:,1]
            t = data[:,2]
            d_measured = data[:,3]
            RX = data[:,4]
            FP = data[:,5]
            Q = data[:,6]

            show_all = 0
            cancel_adjust = 0
            add_filter = 0
            add_offset = 0

            L_new_d_measured = []; L_D_mean_mes = []; L_new_d_real = []; L_D = []
            for idx in np.unique(ids):

                D_mean_real = []
                D_mean_mes = []

                false_value = np.abs(d_measured[ids == idx] - f_distance(idx,d_real)[ids == idx]) > 2
                if not add_filter : false_value[1:] = False

                indices = np.where(np.abs(d_measured[ids == idx] - f_distance(idx,d_real)[ids == idx]) > 2)
                # print(np.unique(d_real[indices]))
                
                new_ids = ids[ids == idx][~false_value]
                new_d_real = d_real[ids == idx] 
                new_d_real = f_distance(idx,new_d_real)[~false_value]
                D = np.unique(new_d_real)

                new_t = t[ids == idx][~false_value]
                new_d_measured = d_measured[ids == idx][~false_value] + offset[idx]
                
                # Add offset when we start
                if add_offset : new_d_measured = new_d_measured + (np.mean(new_d_real[new_d_real == D[0]] - new_d_measured[new_d_real == D[0]]))
                
                new_RX = RX[ids == idx][~false_value]
                new_FP = FP[ids == idx][~false_value]
                new_Q = Q[ids == idx][~false_value]

                if cancel_adjust:
                    alpha = 2.334
                    for i in range(new_RX.shape[0]): #rx in new_RX:
                        if new_RX[i]/(1+alpha)-88*alpha > -88 and filename[-44:] != "2023_04_26_16_31_06_Test_multiple_points.csv":
                            new_RX[i] = 1/(alpha+1)*(new_RX[i] - 88)
                    for i in range(new_FP.shape[0]):
                        if new_FP[i]/(1+alpha)-88*alpha > -88 and filename[-44:] != "2023_04_26_16_31_06_Test_multiple_points.csv":
                            new_FP[i] = 1/(alpha+1)*(new_FP[i] - 88)
                
                

                for d in D:
                    D_mean_mes.append(np.mean(new_d_measured[new_d_real == d]))
                    
                D_mean_mes = np.array(D_mean_mes)

                L_new_d_measured.append(new_d_measured)
                L_D_mean_mes.append(D_mean_mes)
                L_new_d_real.append(new_d_real)
                L_D.append(D)

                print(f"Résidus = {(D_mean_mes - D)}")
                print(f"Ecart-type des résidus = {np.std(D_mean_mes - D)}")
                print(f"Moyenne des résidus = {np.mean(D_mean_mes - D)}\n")

                if show_all:
                    means_RX = [np.mean(new_RX[(new_d_real == d)]) for d in D]
                    means_FP = [np.mean(new_FP[(new_d_real == d)]) for d in D]
                    means_Q = [np.mean(new_Q[(new_d_real == d)]) for d in D]

                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("RX")
                    plt.scatter(new_d_real, new_RX)                    
                    plt.plot(D, means_RX, color = 'red')
                    plt.title("RX - Anchor {}".format(idx))
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("FP")
                    plt.scatter(new_d_real, new_FP)                    
                    plt.plot(D, means_FP, color = 'red')
                    plt.title("FP - Anchor {}".format(idx))
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("Q")
                    plt.scatter(new_d_real, new_Q)                    
                    plt.plot(D, means_Q, color = 'red')
                    plt.title("Q - Anchor {}".format(idx))
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("RX - FP")
                    plt.scatter(new_d_real, new_RX - new_FP)                    
                    plt.plot(D, np.array(means_RX) - np.array(means_FP), color = 'red')
                    plt.title("RX - FP - Anchor {}".format(idx))
                    plt.grid()
                
            ### DISPLAY
            fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
            fig.suptitle(filename[-44:])
            for i in range(2):
                for j in range(2):
                    ax = axs[i,j]
                    idx = 2*i + j
                    ax.set_xlabel("Distance (m)")
                    ax.set_ylabel("Measured Range (m)")
                    ax.set_title("Anchor n°{}".format(80 + idx))
                    ax.set_xlim([0, int(np.max(D)+5)])
                    ax.set_ylim([0, int(np.max(D)+5)])
                    ax.scatter(L_new_d_measured[idx], L_new_d_real[idx], label = 'data', s = 0.4)
                    ax.plot(range(0,int(np.max(D))+5),range(0,int(np.max(D))+5))
                    plot_polynomial_regression(ax, L_D_mean_mes[idx], L_D[idx], [1])
        plt.show()