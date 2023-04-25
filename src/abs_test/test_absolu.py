#!/usr/bin/python3
import time
import socket
import json
import numpy as np
import matplotlib.pyplot as plt
import os

# Modules pour l'interpolation
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def connect_to_tag():
    hostname = socket.gethostname()
    UDP_IP = socket.gethostbyname(hostname)
    print("***Local ip:" + str(UDP_IP) + "***")
    UDP_PORT = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.listen(1)  # 接收的连接数
    print("En attente de connexion...")
    data, addr = sock.accept()
    print("Connected !")

    return data, addr

def read_data():
    data.setblocking(False)
    try:
        line = data.recv(1024).decode('UTF-8')
    except BlockingIOError:
        return []  # retourne une liste vide si aucun donnée n'est disponible

    # print("Received data:", line) # Ajout d'une instruction de débogage
    
    uwb_list = []

    try:
        uwb_data = json.loads(line)
        print(uwb_data)

        uwb_list = uwb_data["links"]
        # for uwb_archor in uwb_list:
        #     print(uwb_archor)

    except:
        print("Error decoding JSON:", line) # Ajout d'une instruction de débogage
    # print("Current uwb_list:", uwb_list) # Ajout d'une instruction de débogage

    return uwb_list

def uwb_range_offset(uwb_range):

    temp = uwb_range
    return temp


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
            list = read_data()

            for one in list:

                if one["A"] == "1780":
                    time_anchor1 = uwb_range_offset(float(one["T"]));
                    data_anchor1 = uwb_range_offset(float(one["R"])); 
                    RX_anchor1 = float(one["RX"])
                    FP_anchor1 = float(one["FP"])
                    Q_anchor1 = float(one["Q"])
                    if data_anchor1 != 0:
                        file.write("1780 ; "+ str(d) + ";" + str(time_anchor1) + ";"+ str(data_anchor1) + ";" + str(RX_anchor1) + ";" + str(FP_anchor1) + ";" + str(Q_anchor1) + "\n")

                if one["A"] == "1781":
                    time_anchor2 = uwb_range_offset(float(one["T"]));
                    data_anchor2 = uwb_range_offset(float(one["R"])); 
                    RX_anchor2 = float(one["RX"])
                    FP_anchor2 = float(one["FP"])
                    Q_anchor2 = float(one["Q"])
                    if data_anchor2 != 0:
                        file.write("1781 ; "+ str(d) + ";" + str(time_anchor2) + ";"+ str(data_anchor2) + ";" + str(RX_anchor2) + ";" + str(FP_anchor2) + ";" + str(Q_anchor2) + "\n")

                if one["A"] == "1782":
                    time_anchor3 = uwb_range_offset(float(one["T"]));
                    data_anchor3 = uwb_range_offset(float(one["R"])); 
                    RX_anchor3 = float(one["RX"])
                    FP_anchor3 = float(one["FP"])
                    Q_anchor3 = float(one["Q"])
                    if data_anchor3 != 0:
                        file.write("1782 ; "+ str(d) + ";" + str(time_anchor3) + ";"+ str(data_anchor3) + ";" + str(RX_anchor3) + ";" + str(FP_anchor3) + ";" + str(Q_anchor3) + "\n")

                if one["A"] == "1783":
                    time_anchor4 = uwb_range_offset(float(one["T"]));
                    data_anchor4 = uwb_range_offset(float(one["R"])); 
                    RX_anchor4 = float(one["RX"])
                    FP_anchor4 = float(one["FP"])
                    Q_anchor4 = float(one["Q"])
                    if data_anchor4 != 0:
                        file.write("1783 ; "+ str(d) + ";" + str(time_anchor4) + ";"+ str(data_anchor4) + ";" + str(RX_anchor4) + ";" + str(FP_anchor4) + ";" + str(Q_anchor4) + "\n")
            
            file.flush()


if __name__ == '__main__':
    import datetime, sys
    doing_test = 0
    nb_anchor = 1

    offset = {1780 : 0, 1781 : 0, 1782 : 0, 1783 : 0}
    


    date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    if doing_test:

        data, addr = connect_to_tag()

        print("Start test..")
        file = open(f"{THIS_FOLDER}/{date_str}_Test_multiple_points.csv", "w")
        file.write("n°anchor; d_real [m]; time [ms]; d_measured [m]; RX [dbm]; FP [dbm]; Q;\n")

        D = main(file)

        file.close()

    else:

        ## ONE ANCHOR ONLY
        filename = f"{THIS_FOLDER}/2023_04_25_16_08_59_Test_multiple_points.csv"
        data = np.genfromtxt(filename, delimiter=';', skip_header=1)

        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
        ax.set_title(f"Anchor 1")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Measured Range (m)")


        D_mean_real = []
        D_mean_mes = []

        ids = data[:,0]
        d_real = data[:,1]
        t = data[:,2]
        d_measured = data[:,3]
        RX = data[:,4]
        FP = data[:,5]
        Q = data[:,6]

        for idx in np.unique(ids):

            false_value = np.abs(d_measured - d_real) > 2
            new_ids = ids[ids == idx][~false_value]
            new_d_real = d_real[ids == idx][~false_value]
            new_t = t[ids == idx][~false_value]
            new_d_measured = d_measured[ids == idx][~false_value] + offset[idx]
            new_RX = RX[ids == idx][~false_value]
            new_FP = FP[ids == idx][~false_value]
            new_Q = Q[ids == idx][~false_value]
            
            D = np.unique(new_d_real)

            if idx == 1780:
                for d in D:
                    D_mean_mes.append(np.mean(new_d_measured[new_d_real == d]))
                    
                ax.scatter(new_d_measured, new_d_real, label = 'data', s = 0.4)
                plot_polynomial_regression(ax, D_mean_mes, D, [1])

                
                # f = plt.gcf()
                # dpi = f.get_dpi()
                # h, w = f.get_size_inches()
                # f.set_size_inches(h*2, w*2)
                # plt.savefig(f"{THIS_FOLDER}/{date_str}.png")
                D_mean_mes = np.array(D_mean_mes)
                print(f"Résidus = {np.abs(D_mean_mes - D)}")
                print(f"Ecart-type des résidus = {np.std(D_mean_mes - D)}")
                print(f"Moyenne des résidus = {np.mean(D_mean_mes - D)}")

                show_all = 0

                if show_all:
                    means_RX = [np.mean(new_RX[(new_d_real == d)]) for d in D]
                    means_FP = [np.mean(new_FP[(new_d_real == d)]) for d in D]
                    means_Q = [np.mean(new_Q[(new_d_real == d)]) for d in D]

                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("RX")
                    plt.scatter(new_d_real, new_RX)                    
                    plt.plot(D, means_RX, color = 'red')
                    plt.title("RX")
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("FP")
                    plt.scatter(new_d_real, new_FP)                    
                    plt.plot(D, means_FP, color = 'red')
                    plt.title("FP")
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("Q")
                    plt.scatter(new_d_real, new_Q)                    
                    plt.plot(D, means_Q, color = 'red')
                    plt.title("Q")
                    plt.grid()
                    
                    plt.figure()
                    plt.xlabel("Distance [m]")
                    plt.ylabel("RX - FP")
                    plt.scatter(new_d_real, new_RX - new_FP)                    
                    plt.plot(D, np.array(means_RX) - np.array(means_FP), color = 'red')
                    plt.title("RX - FP")
                    plt.grid()
                
                plt.show()
