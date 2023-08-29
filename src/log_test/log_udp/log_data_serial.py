import serial
import datetime
import os, time

# Définir le port série et le baudrate
ser = serial.Serial('COM5', 115200)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
filename = f"{THIS_FOLDER}/Serial_long_log_{date_str}.csv"
i = 0
# Ouvrir le fichier en mode écriture
with open(filename, "w") as f:
    f.write("Num of Anchor; Time [ms]; Range [m]; RX power [dBm]; FP power [dBm]; Quality; timerpoll [ms]; timersent; timerino\n")

    # Écouter les lignes reçues depuis l'Arduino
    while True:
        line = ser.readline()
        try :
            line = ser.readline().decode().split()

            num = float(line[1])
            data_anchor = float(line[3])
            RX_anchor = float(line[7])
            FP_anchor = float(line[11])
            Q_anchor = float(line[14])
            time_anchor = float(line[16])

            # Affichage des informations à l'écran
            print(f"from: {num} - Range: {data_anchor} m, RX power: {RX_anchor} dBm, FP power: {FP_anchor} dBm, Quality: {Q_anchor}, Timer : {time_anchor}")
            f.write(str(num) + ";"+ str(time_anchor) + ";"+ str(data_anchor) + ";" + str(RX_anchor) + ";" + str(FP_anchor) + ";" + str(Q_anchor) + "\n")
            
            i += 1
            if i%1000==0: 
                f.flush()
        except:
            pass
        
# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
# filename = f"{THIS_FOLDER}/save_times_ms2.csv"
# i = 0
# # Ouvrir le fichier en mode écriture
# with open(filename, "w") as f:
#     f.write("Time name; timer [s/ps]\n")

#     # Écouter les lignes reçues depuis l'Arduino
#     while 1:
#         line = ser.readline()
#         print(line)
#         try :
#             line = ser.readline().decode().split(":")

#             name = line[0]
#             timer = float(line[1])

#             # Affichage des informations à l'écran
#             print(line)
#             f.write(str(name) + ";"+ str(timer)+"\n")
            
#         except:
#             pass

#         if KeyboardInterrupt: f.flush()
