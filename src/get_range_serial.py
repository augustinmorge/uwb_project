import csv
import serial
import matplotlib.pyplot as plt

def log_range_to_csv(file, ser):
    # Ouvre le fichier CSV en mode append
    plt.figure()
    plt.ion()
    ct = 0; R = []
    with open(file, 'a', newline='') as csvfile:
        # Initialise le writer CSV
        writer = csv.writer(csvfile)
        
        while True:
            # Lit une ligne depuis le port série
            r = ser.readline().decode('utf-8').rstrip()
            csvfile.write(str(r)+"\n")
            R.append(float(r))
            plt.plot([i for i in range(ct+1)],R);ct+=1
            plt.pause(0.5)

def plot_range(file_path):
    range_values = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            range_values.append(float(row[0]))
    
    plt.figure()
    plt.plot(range(len(range_values)), range_values)
    plt.title("Changement brutal d'entrée en volt")
    plt.xlabel("Itérations")
    plt.ylabel("Range")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    import os
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    # ser = serial.Serial('COM5', 115200)
    # file = f"{THIS_FOLDER}/get_range.csv"
    # log_range_to_csv(file, ser)
    plot_range(f"{THIS_FOLDER}/logs/log_long/Long_log_12_05_2023_10_40_54.csv")