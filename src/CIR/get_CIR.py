import os
import sys
import datetime
import csv
import serial
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
import matplotlib.pyplot as plt

def plot_data(filename):
    x = []
    y = []
    with open(filename, 'r') as file:
        f = file.readlines()
        for i in range(len(f)):
            row = f[i].strip().split(',')
            x.append(int(i))
            y.append(float(row[0]))
    plt.plot(x, y)
    plt.title('CIR')
    plt.xlabel('Nombre de mesures')
    plt.ylabel('dBm')
    plt.show()

looging_data = 0

if looging_data:
    # Ouvrir le port série
    ser = serial.Serial('COM8', 115200)

    # Ouvrir un fichier de log CSV avec un nom basé sur la date et l'heure
    
    log_file_name = "CIR_data\\CIR_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    log_file_path = os.path.join(THIS_FOLDER, log_file_name)

    i = 0
    with open(log_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Boucle principale de log
        while True:
            if ser.in_waiting > 0:
                # Lire les données reçues du port série
                data = ser.readline().decode().strip()

                # Ajouter une ligne au fichier de log
                csv_writer.writerow([data])
                csv_file.flush()

                # Afficher les données à l'écran
                print(data)
                i+=1


else:
    csv_file_los = THIS_FOLDER + f"\\CIR_data\\CIR_2023-04-18_11-59-14.csv"
    csv_file_nlos = THIS_FOLDER + f"\\CIR_data\\CIR_2023-04-18_11-59-28.csv"
    plot_data(csv_file_los)
    plot_data(csv_file_nlos)

    import numpy as np

    # # Load the CIR data from the CSV file
    cir_los = np.genfromtxt(csv_file_los,skip_header=17)
    cir_nlos = np.genfromtxt(csv_file_nlos,skip_header=17)

    # Number of subsets to create
    subset_size = 250 #int(len(cir) / num_subsets)
    num_subsets = min(len(cir_los)//subset_size, len(cir_nlos)//subset_size) #100


    # List to store kurtosis values
    kurtosis_values_los = []
    kurtosis_values_nlos = []

    # List to store τm values
    tau_m_values_los = []
    tau_m_values_nlos = []

    # List to store τrms values
    tau_rms_values_los = []
    tau_rms_values_nlos = []

    # Create subsets and calculate kurtosis for each subset
    kurtosis = lambda x : np.mean((np.abs(x) - np.mean(np.abs(x))) ** 4) / (np.mean((np.abs(x) - np.mean(np.abs(x))) ** 2) ** 2)
    from tqdm import tqdm

    for i in tqdm(range(num_subsets)):

        start_index = i * subset_size
        end_index = start_index + subset_size


        #k LOS ans NLOS

        h_los = cir_los[start_index:end_index]
        k_los = kurtosis(h_los)

        h_nlos = cir_nlos[start_index:end_index]
        k_nlos = kurtosis(h_nlos)

        kurtosis_values_los.append(k_los)
        kurtosis_values_nlos.append(k_nlos)


        #LOS tm and trms

        t_nlos = np.arange(len(h_los)) #np.linspace(start_index, end_index, min(len(h_nlos),len(h_nlos)))

        # tau_m_los = np.trapz(h_los**2 * t_nlos, dx=1/64) / np.trapz(h_los**2, dx=1/64)
        tau_m_los = np.sum(h_los**2 * t_nlos) / np.sum(h_los**2)
        tau_m_values_los.append(tau_m_los)

        # tau_rms_los = np.sqrt(np.trapz(((t_nlos - tau_m_los)*h_los)**2, dx=1/64) / np.trapz(h_los**2, dx=1/64))
        tau_rms_los = np.sqrt(np.sum(((t_nlos - tau_m_los)*h_los)**2) / np.trapz(h_los**2))
        tau_rms_values_los.append(tau_rms_los)


        #NLOS tm and trms
        
        t_nlos = np.arange(len(h_nlos)) #np.linspace(start_index, end_index, min(len(h_los),len(h_nlos)))

        # tau_m_nlos = np.trapz(h_nlos**2 * t_nlos, dx=1/64) / np.trapz(h_nlos**2, dx=1/64)
        tau_m_nlos = np.sum(h_nlos**2 * t_nlos) / np.sum(h_nlos**2)
        tau_m_values_nlos.append(tau_m_nlos)

        # tau_rms_nlos = np.sqrt(np.trapz(((t_nlos - tau_m_nlos)*h_nlos)**2, dx=1/64) / np.trapz(h_nlos**2, dx=1/64))
        tau_rms_nlos = np.sqrt(np.sum(((t_nlos - tau_m_nlos)*h_nlos)**2) / np.sum(h_nlos**2))
        tau_rms_values_nlos.append(tau_rms_nlos)

    # Plot histogram
    plt.figure()
    plt.hist(kurtosis_values_los, bins=num_subsets,label='LOS', alpha=0.5)
    plt.hist(kurtosis_values_nlos, bins=num_subsets,label='NLOS',alpha=0.5)
    plt.xlabel('Kurtosis')
    plt.ylabel('Number of samples')
    plt.title('Distribution of Kurtosis Values')
    plt.legend()

    # Plot histogram
    plt.figure()
    plt.hist(tau_m_values_los, bins=num_subsets, label='LOS', alpha=0.5)
    plt.hist(tau_m_values_nlos, bins=num_subsets, label='NLOS', alpha=0.5)
    plt.xlabel('τm')
    plt.ylabel('Number of samples')
    plt.title('Distribution of τm Values')
    plt.legend()

    # Plot histogram
    plt.figure()
    plt.hist(tau_rms_values_los, bins=num_subsets, label='LOS', alpha=0.5)
    plt.hist(tau_rms_values_nlos, bins=num_subsets, label='NLOS', alpha=0.5)
    plt.xlabel('τrms')
    plt.ylabel('Number of samples')
    plt.title('Distribution of τrms Values')
    plt.legend()
    plt.show()