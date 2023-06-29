import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import serial
from datetime import datetime
import os

# Créer le nom de fichier avec la date actuelle
current_datetime = datetime.now()

# Obtenir le répertoire actuel du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))


logging = False

if logging:

    # Créer le nom de fichier avec la date actuelle
    current_datetime = datetime.now()
    filename = os.path.join(script_directory, f"log_{current_datetime.strftime('%Y%m%d_%H%M%S')}.txt")

    # Paramètres de communication série
    port = 'COM4'
    baudrate = 115200

    # Ouvrir la connexion série
    ser = serial.Serial(port, baudrate)

    # Indicateur pour vérifier si la ligne avec "round1" a été détectée
    start_logging = False

    
    # Ouvrir le fichier de journal en mode d'ajout
    with open(filename, "a") as file:
        # Écrire les en-têtes dans le fichier s'ils n'existent pas déjà
        if file.tell() == 0:
            file.write("round1,round2,reply1,reply2,distance_meas,distance_real\n")

        # Lire les données de l'Arduino et les enregistrer dans le fichier
        while True:
            line = ser.readline().decode().strip()

            # Vérifier si la ligne avec "round1" est détectée
            if line.startswith("round1"):
                start_logging = True

            # Commencer à enregistrer les données après avoir détecté "round1"
            if start_logging:
                if line.startswith("round1"):
                    round1 = line.split(":")[1].strip()
                elif line.startswith("round2"):
                    round2 = line.split(":")[1].strip()
                elif line.startswith("reply1"):
                    reply1 = line.split(":")[1].strip()
                elif line.startswith("reply2"):
                    reply2 = line.split(":")[1].strip()
                elif line.startswith("distance_meas"):
                    distance_meas = line.split(":")[1].strip()
                elif line.startswith("distance_real"):
                    distance_real = line.split(":")[1].strip()

                    # Écrire les valeurs dans le fichier
                    print(f"{round1},{round2},{reply1},{reply2},{distance_meas},{distance_real}\n")
                    file.write(f"{round1},{round2},{reply1},{reply2},{distance_meas},{distance_real}\n")
                    file.flush()

else:
    # Fonction f(T)
    def f(T, a, b, c, d, v):
        return v * (a * b - c * d - (c * T + d * T + T**2)) / (a + b + c + d + 2*T)
    def error(T, D, a, b, c, d, v):
        predictions = f(T, a, b, c, d, v)
        return np.sqrt(np.mean((D - predictions)**2))
    def optimize_T(D, a, b, c, d, v):
        initial_guess = 269758.0 # Valeur initiale de T
        result = minimize(lambda T: error(T, D, a, b, c, d, v), initial_guess, method='BFGS')
        optimal_T = result.x[0]
        return optimal_T

    # Fonction d'appel à minimize
    def f_old(T, a, b, c, d, v):
        return v * ((a * b - c * d) / (a + b + c + d) + T)
    def error_old(T, D, a, b, c, d, v):
        predictions = f_old(T, a, b, c, d, v)
        return np.sqrt(np.mean((D - predictions)**2))
    def optimize_T_old(D, a, b, c, d, v):
        initial_guess = 269758.0 # Valeur initiale de T
        result = minimize(lambda T: error_old(T, D, a, b, c, d, v), initial_guess, method='BFGS')
        optimal_T_old = result.x[0]
        return optimal_T_old
    
    # Importer les données du log
    # data = np.loadtxt(script_directory+"\\log_20230626_150203.txt", delimiter=",", skiprows=1)
    # data = np.loadtxt(script_directory+"\\log_20230626_164916.txt", delimiter=",", skiprows=1)
    # Extraire les colonnes du log
    # round1 = data[:, 0]
    # round2 = data[:, 1]
    # reply1 = data[:, 2]
    # reply2 = data[:, 3]
    # distance_meas = data[:, 4]
    # distance_real = data[:, 5]

    data = np.loadtxt(script_directory+"\\2023_06_27_10_52_36_Serial_Test_multiple_points.csv", delimiter=";", skiprows=1, dtype='<U15')

    distance_meas = data[:, 3].astype(float)
    mask = np.diff(distance_meas) > 0.000005
    mask = np.hstack((False, mask))

    print(f"We use {distance_meas[~mask].shape[0]/distance_meas.shape[0]*100}% of data")

    distance_meas = distance_meas[~mask]
    distance_real = data[:, 1].astype(float)[~mask]

    # Extraire les colonnes du log

    timePollSent = data[:, 7].astype(float)[~mask]
    timePollReceived = data[:, 8].astype(float)[~mask]
    timePollAckSent = data[:, 9].astype(float)[~mask]
    timePollAckReceived = data[:, 10].astype(float)[~mask]
    timeRangeSent = data[:, 11].astype(float)[~mask]
    timeRangeReceived = data[:, 12].astype(float)[~mask]

    timestamp = 1099511627775  # Valeur du timestamp
    timeoverflow = 1099511627776
    timeres = 0.000015650040064103
    offset = (timestamp % timeoverflow) * timeres * 10 ** (-6)

    def adjust_time_array(time_array):
        k = 0
        new_time_array = np.zeros(time_array.shape)
        new_time_array[0] = time_array[0]

        for i in range(1, time_array.shape[0]):
            if time_array[i] < time_array[i - 1]:
                k += 1
            new_time_array[i] = (k * offset + time_array[i])

        return new_time_array

    timePollSent = adjust_time_array(timePollSent)
    timePollReceived = adjust_time_array(timePollReceived)
    timePollAckSent = adjust_time_array(timePollAckSent)
    timePollAckReceived = adjust_time_array(timePollAckReceived)
    timeRangeSent = adjust_time_array(timeRangeSent)
    timeRangeReceived = adjust_time_array(timeRangeReceived)

    round1 = timePollAckReceived-timePollSent
    reply1 = timePollAckSent-timePollReceived
    round2 = timeRangeReceived-timePollAckSent
    reply2 = timeRangeSent-timePollAckReceived



    # Utiliser les données pour l'optimisation
    D = distance_real
    a = round1
    b = round2
    c = reply1
    d = reply2
    # v = 299710666.95 #m/s
    v = 0.0046917639786159

    # Optimiser T
    optimal_T = optimize_T(D, a, b, c, d, v)
    print("Valeur optimale de T new:", optimal_T)

    optimal_T_old = optimize_T_old(D, a, b, c, d, v)
    print("Valeur optimale de T old:", optimal_T_old)

    # Afficher les données mesurées et estimées
    plt.figure()
    plt.scatter(range(D.shape[0]), distance_real, label='Données vraie', s = 2)
    plt.scatter(range(D.shape[0]), distance_meas, label='Données mesurées', s = 2)
    # plt.scatter(range(D.shape[0]), f_old(optimal_T_old, a, b, c, d, v), label='Données calculées en TOF classique', s = 2)
    plt.scatter(range(D.shape[0]), f(optimal_T, a, b, c, d, v), label='Données estimées nouvellement', s = 2)
    plt.ylim([-20, 100])

    plt.legend()
    plt.xlabel("it")
    plt.ylabel("dist [m]")
    plt.title("Distance measured")

    plt.figure()
    plt.title("Diff between old and new calculation")
    plt.xlabel("it")
    plt.ylabel("dist [m]")
    plt.plot(f_old(optimal_T_old, a, b, c, d, v) - f(optimal_T, a, b, c, d, v))

    plt.figure()
    plt.title("Error")
    plt.ylabel("Error [m]")
    plt.xlabel("Time Samples")
    plt.plot(distance_real - f(optimal_T, a, b, c, d, v),label='new method')
    plt.plot(distance_real - f_old(optimal_T_old, a, b, c, d, v),label='old_method')
    plt.legend()
    plt.show()