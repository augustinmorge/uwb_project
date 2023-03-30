#!/usr/bin/python3
import time
import socket
import json
import keyboard
import numpy as np
import matplotlib.pyplot as plt
import os

# Modules pour l'interpolation
from scipy import stats
from scipy.interpolate import interp1d
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

# def plot_polynomial_regression(ax, x, y, degrees, num_anc=0):

#     # Calculate coefficients for each degree of polynomial
#     coeffs = []
#     for degree in degrees:
#         p = np.polyfit(x, y, degree)
#         coeffs.append(p)

#     # Plot data and polynomial lines of best fit
#     ax.scatter(x, y, label='Data')
#     for i, c in enumerate(coeffs):
#         line_x = np.linspace(min(x), max(x), 10000)
#         line_y = np.polyval(c, line_x)
#         r_squared = r2_score(y, np.polyval(c, x))
#         # Construct equation string
#         eqn = f"y = {c[-1]:.2f}"
#         for j in range(len(c)-2, -1, -1):
#             if len(c)-j-1 == 1:
#                 eqn += f" + {c[j]:.2f}x"
#             else:
#                 eqn += f" + {c[j]:.2f}x^{len(c)-j-1}"
#         ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.2f})', color = 'red')

#     ax.legend(loc='upper left')


import numpy as np
from sklearn.metrics import r2_score

def plot_polynomial_regression(ax, x: np.ndarray, y: np.ndarray, degrees: list[int], num_anc: int = 0) -> None:
    """
    Plots polynomial regression lines of best fit for input data.

    Args:
        ax: A matplotlib Axes object to plot the data and lines on.
        x: A 1D numpy array of x-values.
        y: A 1D numpy array of y-values.
        degrees: A list of degrees of polynomial to fit.
        num_anc: An integer representing the number of ancestors.

    Returns:
        None
    """

    try:
        # Calculate coefficients for each degree of polynomial
        coeffs = [np.polyfit(x, y, degree) for degree in degrees]

        # Plot data and polynomial lines of best fit
        ax.scatter(x, y, label='Data')
        for i, c in enumerate(coeffs):
            line_x = np.linspace(min(x), max(x), 10000)
            line_y = np.polyval(c, line_x)
            r_squared = r2_score(y, np.polyval(c, x))
            # Construct equation string
            coeffs_str = [f"{c[j]:.2f}x^{len(c)-j-1}" if len(c)-j-1 > 1 else f"{c[j]:.2f}x" if len(c)-j-1 == 1 else f"{c[j]:.2f}" for j in range(len(c)-2, -1, -1)]
            eqn = f"y = {c[-1]:.2f} + {' + '.join(coeffs_str)}" if len(coeffs_str) > 0 else f"y = {c[-1]:.2f}"
            ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.2f})', color='red')

        ax.legend(loc='upper left')

    except Exception as e:
        print(f"Error: {e}")

def main(nb_anchor, dmin, dmax, pas, sec):
    end = False
    N =  np.arange(dmin, dmax + pas, pas).shape[0]

    
    D = np.zeros((N,nb_anchor+1))
    D[:,0] = np.linspace(dmin,dmax,N).reshape(-1,1).squeeze()
    # D = np.loadtxt(f"{THIS_FOLDER}/log_cali/Test_on_2023_03_21.csv", delimiter=";", skiprows=1)
    while not end:
        for anchor in range(0,nb_anchor):
            idx_D = 0
            # if anchor == 3: 
            #     dmin = 3.5
            #     idx_D = int(2*dmin - 1)
            for d in np.arange(dmin, dmax + pas, pas):
                
                print(f"Please select Anchor n°{anchor+80}")
                print(f"Measuring distance from {d}m")
                print("Do you want to start ?")
                print("Press ENTER three times")
                keyboard.wait("ENTER")
                keyboard.wait("ENTER")
                keyboard.wait("ENTER")

                t0 = time.time()
                a1_range = 0; i1 = 0
                a2_range = 0; i2 = 0
                a3_range = 0; i3 = 0
                a4_range = 0; i4 = 0
                while time.time() - t0 < sec:
                    list = read_data()

                    for one in list:

                        if one["A"] == "1780":
                            a1_range += uwb_range_offset(float(one["R"])); 
                            i1 += 1

                        if one["A"] == "1781":
                            a2_range += uwb_range_offset(float(one["R"])); 
                            i2 += 1

                        if one["A"] == "1782":
                            a3_range += uwb_range_offset(float(one["R"])); 
                            i3 += 1

                        if one["A"] == "1783":
                            a4_range += uwb_range_offset(float(one["R"])); 
                            i4 += 1
                
                if i1 != 0 and anchor == 0: 
                    D[idx_D,1] = a1_range/i1

                if i2 != 0 and anchor == 1: 
                    D[idx_D,2] = a2_range/i2

                if i3 != 0 and anchor == 2: 
                    D[idx_D,3] = a3_range/i3

                if i4 != 0 and anchor == 3: 
                    D[idx_D,4] = a4_range/i4
                
                idx_D += 1
            
                D_temp = D
                np.savetxt(f"{THIS_FOLDER}/log_cali/Test_on_{date_str}.csv", D_temp, delimiter=";", header="Distance(m); Anchor 1; Anchor 2; Anchor 3; Anchor 4", fmt="%.3f")
        
            if d == dmax : end = True
    
    return D


if __name__ == '__main__':
    import datetime
    doing_calibration = False

    if doing_calibration:
        date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        data, addr = connect_to_tag()

        print("Start Calibration..")



        nb_anchor = 1
        D = main(nb_anchor, dmin = 0.5,dmax = 10, pas = 0.5, sec=30)
        ch_nb_anchor = ""
        for anchor in range(nb_anchor):
            ch_nb_anchor += "Anchor {}; ".format(anchor)
        np.savetxt(f"{THIS_FOLDER}/log_cali/Test_on_{date_str}.csv", D, delimiter=";", header=f"Distance (m); {ch_nb_anchor}", fmt="%.3f")

    else:
        ### if 4 anchors:
        name_log = 'Test_on_2023_03_30_09_35_46'
        # D = np.loadtxt(f"{THIS_FOLDER}/log_cali/Test_on_2023_03_21.csv", delimiter=";", skiprows=1)
        # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
        # plt.suptitle("Calibration for the Anchors")
        # axs = axs.flatten()
        # for i, ax in enumerate(axs):
        #     ax.set_title(f"Anchor {80 + i}")
        #     ax.set_xlabel("Distance (m)")
        #     ax.set_ylabel("Measured Range (m)")
        #     plot_polynomial_regression(ax, D[0:,i+1], D[0:,0], [1], 80 + i)
        # ### To save the plot
        # f = plt.gcf()
        # dpi = f.get_dpi()
        # h, w = f.get_size_inches()
        # f.set_size_inches(h*2, w*2)
        # plt.savefig(f"{THIS_FOLDER}/log_cali/First_data.png")


        D = np.loadtxt(f"{THIS_FOLDER}/log_cali/{name_log}.csv", delimiter=";", skiprows=1)
        print(D)
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
        ax.set_title(f"Anchor 1")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Measured Range (m)")
        plot_polynomial_regression(ax, D[:,1], D[:,0], [1], 80)

        plt.show()