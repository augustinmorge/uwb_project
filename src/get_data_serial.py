import serial
import struct

def receive_data(ser):
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
        'short_address': short_address,
        'range': range_value,
        'rx_power': rx_power,
        'fp_power': fp_power,
        'quality': quality,
        'timer': timer
    }

if __name__ == "__main__":
    # Ouvrir une connexion série sur le port COM5
    ser = serial.Serial('COM5', 115200)

    while 1:
        print(receive_data(ser))