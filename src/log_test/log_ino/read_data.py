import serial
import struct

def receive_data_bits(file, ser):
    
    # Tailles en bytes de chaque donnée dans le buffer
    short_address_size = 2
    range_size = 4
    rx_power_size = 4
    fp_power_size = 4
    quality_size = 4
    timer_size_ps = 4
    timer_size_rs = 4
    timer_size_ino = 4

    buffer_size = short_address_size + range_size + rx_power_size + fp_power_size + quality_size + timer_size_ino + timer_size_ps + timer_size_rs
    
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
    timer_ps = struct.unpack('f', buffer[range_size+rx_power_size+fp_power_size+quality_size:range_size+rx_power_size+fp_power_size+quality_size+timer_size_ps])[0]
    timer_rs = struct.unpack('f', buffer[range_size+rx_power_size+fp_power_size+quality_size+timer_size_ps:range_size+rx_power_size+fp_power_size+quality_size+timer_size_ps+timer_size_rs])[0]
    timer_ino = struct.unpack('f', buffer[range_size+rx_power_size+fp_power_size+quality_size+timer_size_ps+timer_size_rs:range_size+rx_power_size+fp_power_size+quality_size+timer_size_ps+timer_size_rs+timer_size_ino])[0]
    if logging:
        file.write(str(short_address) + ";"+ str(timer_ino) + ";"+ str(range_value) + ";" + str(rx_power) + ";" + str(fp_power) + ";" + str(quality) + ";" + str(timer_ps) + ";" + str(timer_rs) + "\n")
        file.flush()
    # Retourner un dictionnaire contenant les données
    return {
        'short_address': short_address,
        'range': range_value,
        'rx_power': rx_power,
        'fp_power': fp_power,
        'quality': quality,
        'timer_ps': timer_ps,
        'timer_rs': timer_rs,
        'timer_ino': timer_ino
    }

if __name__ == "__main__":
    # Ouvrir une connexion série sur le port COM5
    import datetime
    import os
    ser = serial.Serial('COM5', 115200)
    logging = 1
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    if logging:
        f = open(f"{THIS_FOLDER}/{date_str}_log-all-with-time.csv","w")
        f.write("Short Address;Timer Ino;Range;RX Power;FP Power;Quality;Timer PS;Timer RS\n")
        f.flush()
    else:
        f = None
    i = 0
    while 1:
        r = receive_data_bits(f, ser)
        print(r)
