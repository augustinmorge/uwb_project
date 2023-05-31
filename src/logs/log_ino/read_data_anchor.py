import serial
import struct

def receive_data_bits(file, ser):
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
    short_address =  struct.unpack('H', ser.read(2)[:short_address_size])[0]

    while int(short_address) != 125: # Attendre de lire l'octet 0xFF
        short_address =  struct.unpack('H', ser.read(2)[:short_address_size])[0]

    # Lire les données disponibles depuis la connexion série
    buffer = ser.read(buffer_size - short_address_size) # Lire le reste du buffer, moins l'octet déjà reçu

    range_value = struct.unpack('i', buffer[:range_size])[0]
    rx_power = struct.unpack('i', buffer[range_size:range_size + rx_power_size])[0]
    fp_power = struct.unpack('i', buffer[range_size + rx_power_size:range_size + rx_power_size + fp_power_size])[0]
    quality = struct.unpack('i', buffer[range_size + rx_power_size + fp_power_size:range_size + rx_power_size + fp_power_size + quality_size])[0]
    timer_poll_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size])[0]
    timer_poll_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size])[0]
    timer_poll_ack_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size])[0]
    timer_poll_ack_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size])[0]
    timer_range_sent = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size])[0]
    timer_range_received = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size:range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size])[0]
    timer_ino = struct.unpack('f', buffer[range_size + rx_power_size + fp_power_size + quality_size + timer_poll_sent_size + timer_poll_received_size + timer_poll_ack_sent_size + timer_poll_ack_received_size + timer_range_sent_size + timer_range_received_size:])[0]

    if logging:
        file.write(
            '7D' + ";" +
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

    # Retourner un dictionnaire contenant les données
    return {
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
    }

if __name__ == "__main__":
    # Ouvrir une connexion série sur le port COM8
    import datetime
    import os
    print("Opening COM8")
    ser = serial.Serial('COM8', 115200)
    print("COM8 opened")
    logging = 1
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    if logging:
        f = open(f"{THIS_FOLDER}/anchor/{date_str}_log-all-with-time.csv","w")
        f.write("Short Address;Timer Ino;Range;RX Power;FP Power;Quality;Timer PS;Timer RS\n")
        f.flush()
    else:
        f = None
    i = 0
    print("Start reading data")
    while 1:
        r = receive_data_bits(f, ser)
        print(r)
