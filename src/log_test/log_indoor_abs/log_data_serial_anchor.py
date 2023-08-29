import os, struct, time, sys, serial

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# def read_data(file, ser, logging = True):
#     # Tailles en bytes de chaque donnée dans le buffer
#     short_address_size = 2
#     range_size = 4
#     rx_power_size = 4
#     fp_power_size = 4
#     quality_size = 4
#     timer_poll_sent_size = 4
#     timer_poll_received_size = 4
#     timer_poll_ack_sent_size = 4
#     timer_poll_ack_received_size = 4
#     timer_range_sent_size = 4
#     timer_range_received_size = 4
#     timer_ino_size = 4

#     buffer_size = (
#         short_address_size +
#         range_size +
#         rx_power_size +
#         fp_power_size +
#         quality_size +
#         timer_poll_sent_size +
#         timer_poll_received_size +
#         timer_poll_ack_sent_size +
#         timer_poll_ack_received_size +
#         timer_range_sent_size +
#         timer_range_received_size +
#         timer_ino_size
#     )

#     # Attendre que des données soient disponibles sur la connexion série
#     short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]
#     ids = ['7d']
    
#     while short_address not in ids:
#         short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]

#     # Lire les données disponibles depuis la connexion série
#     buffer = ser.read(buffer_size - short_address_size) # Lire le reste du buffer, moins l'octet déjà reçu

#     range_value = struct.unpack('f', buffer[:range_size])[0]
#     rx_power = struct.unpack('f', buffer[range_size:range_size + rx_power_size])[0]
#     fp_power = struct.unpack('f', buffer[range_size + rx_power_size:range_size + rx_power_size + fp_power_size])[0]
#     quality = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size:range_size + rx_power_size + fp_power_size + quality_size])[0]
#     timer_poll_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size])[0]
#     timer_poll_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size])[0]
#     timer_poll_ack_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size])[0]
#     timer_poll_ack_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size])[0]
#     timer_range_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size])[0]
#     timer_range_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size])[0]
#     timer_ino = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size:])[0]

#     if logging:
#         file.write(
#             '7D' + ";" +
#             str(timer_ino) + ";" +
#             str(range_value) + ";" +
#             str(rx_power) + ";" +
#             str(fp_power) + ";" +
#             str(quality) + ";" +
#             str(timer_poll_sent) + ";" +
#             str(timer_poll_received) + ";" +
#             str(timer_poll_ack_sent) + ";" +
#             str(timer_poll_ack_received) + ";" +
#             str(timer_range_sent) + ";" +
#             str(timer_range_received) + "\n"
#         )
#         file.flush()

#     # Retourner un dictionnaire contenant les données
#     return {
#         'short_address': short_address,
#         'range': range_value,
#         'rx_power': rx_power,
#         'fp_power': fp_power,
#         'quality': quality,
#         'timer_poll_sent': timer_poll_sent,
#         'timer_poll_received': timer_poll_received,
#         'timer_poll_ack_sent': timer_poll_ack_sent,
#         'timer_poll_ack_received': timer_poll_ack_received,
#         'timer_range_sent': timer_range_sent,
#         'timer_range_received': timer_range_received,
#         'timer_ino': timer_ino
#     }


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
        try:
            ser.open()
        except serial.serialutil.SerialException:
            print("Port Already Open")

        while time.time() - t0 < sec:

            # Tailles en bytes de chaque donnée dans le buffer
            short_address_size = 2
            range_size = 4
            rx_power_size = 4
            fp_power_size = 4
            quality_size = 4
            timer_poll_sent_size = 4
            timer_poll_received_size = 4
            timer_poll_ack_sent_size = 4
            timer_poll_ack_received_size = 4
            timer_range_sent_size = 4
            timer_range_received_size = 4
            timer_ino_size = 4

            buffer_size = (
                short_address_size +
                range_size +
                rx_power_size +
                fp_power_size +
                quality_size +
                timer_poll_sent_size +
                timer_poll_received_size +
                timer_poll_ack_sent_size +
                timer_poll_ack_received_size +
                timer_range_sent_size +
                timer_range_received_size +
                timer_ino_size
            )

            # Attendre que des données soient disponibles sur la connexion série
            short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]
            ids = ['7d']
            
            while short_address not in ids:
                short_address =  hex(struct.unpack('H', ser.read(2)[:short_address_size])[0])[2:]

            # Lire les données disponibles depuis la connexion série
            buffer = ser.read(buffer_size - short_address_size) # Lire le reste du buffer, moins l'octet déjà reçu

            range_value = struct.unpack('f', buffer[:range_size])[0]
            rx_power = struct.unpack('f', buffer[range_size:range_size + rx_power_size])[0]
            fp_power = struct.unpack('f', buffer[range_size + rx_power_size:range_size + rx_power_size + fp_power_size])[0]
            quality = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size:range_size + rx_power_size + fp_power_size + quality_size])[0]
            timer_poll_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size])[0]
            timer_poll_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size])[0]
            timer_poll_ack_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size])[0]
            timer_poll_ack_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size])[0]
            timer_range_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size])[0]
            timer_range_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size])[0]
            timer_ino = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size:])[0]

            if True:
                file.write(
                    '7D' + ";" +
                    str(d) + ";" + 
                    str(timer_ino) + ";" +
                    str(range_value) + ";" +
                    str(rx_power) + ";" +
                    str(fp_power) + ";" +
                    str(quality) + ";" +
                    str(timer_poll_sent) + ";" +
                    str(timer_poll_received) + ";" +
                    str(timer_poll_ack_sent) + ";" +
                    str(timer_poll_ack_received) + ";" +
                    str(timer_range_sent) + ";" +
                    str(timer_range_received) + "\n"
                )

                file.flush()
                print({
                    'short_address': short_address,
                    'range': range_value,
                    'rx_power': rx_power,
                    'fp_power': fp_power,
                    'quality': quality,
                    'timer_poll_sent': timer_poll_sent,
                    'timer_poll_received': timer_poll_received,
                    'timer_poll_ack_sent': timer_poll_ack_sent,
                    'timer_poll_ack_received': timer_poll_ack_received,
                    'timer_range_sent': timer_range_sent,
                    'timer_range_received': timer_range_received,
                    'timer_ino': timer_ino
                })
        
        ser.close()
# if __name__ == "__main__":
#     import serial
#     ser = serial.Serial('COM4', 115200)
#     while True:
#         print(read_data("",ser,False))