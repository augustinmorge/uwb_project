import socket
import json
import numpy as np
import matplotlib.pyplot as plt
import time
# Modules pour l'interpolation
from sklearn.metrics import r2_score
import sys

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

def read_data(data):
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

def plot_polynomial_regression(ax, x, y, degrees, label = ""):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    ax.scatter(x, y, label='Mean data '+label)
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.3f}) \n'+label)
    ax.legend(loc='upper left')

def main(file, data, sec = 60):
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
            list = read_data(data)

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