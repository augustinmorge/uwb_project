import os, struct, time, sys

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def read_data(ser):
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
    return coeffs



def main(file, ser, sec = 60):
    
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
            one = read_data(ser)
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