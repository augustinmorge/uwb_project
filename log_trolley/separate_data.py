"""
This program is used to separate the data :
    - Beacon id staring with 6016 + N (dec) = 0x1780 + N (hex) and correspond to the real lat/lon/depth
    - Beacon id staring with 16 + N (dec) is used to create dbm values in delphINS

        Store as                        Correspond to
        ----------------------------------------------
        Longitude [m]                   -FPPower (10log((f1^2 + f2^2 + f3^2)/N^2) - A) [dbm]
        Latitude [m]                    -RXPower (10log(C/N^2)-A) [dbm]
        Depth [m]                       Quality (f2/std_noise) [dbm]
        Range  [m]                      RXPower - FPPower [dbm]
        Beacon_range_std_dev            FPPower/std_noise

This was created in order to characterize LOS/NLOS on RLTS.
"""

import os
import numpy as np

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

date = "28_06_2023"
filename = f'{date}_PH-2248_A_POSTPROCESSING-ins.xpf.txt'
file_name = f"{date}\\{filename}"

file_path = os.path.join(current_directory, file_name)

######################### RECUPERATION DU HEADER #########################

with open(file_path, 'r') as file:
    header_lines = [next(file) for _ in range(12)]
header = ''.join(header_lines).rstrip('\t\n')

######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_path, delimiter='\t', skip_header=12, dtype='<U15')
anchor_id = np.arange(6016, 6020)
new_file_anchor_path = os.path.join(current_directory, f"{date}\\anchor_{filename}")
filtered_data_anchor = data[np.isin(data[:, 2].astype(float), anchor_id)]
if filtered_data_anchor[0, 5].astype(float) > -100:
    filtered_data_anchor[:, 5] = (filtered_data_anchor[:, 5].astype(float) - 47.26).astype(str) # Conversion en chaînes de caractères
filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6016), 7] = '0.2'
filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6017), 7] = '0.2'
filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 7] = '0.2'
filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 7] = '0.2'
np.savetxt(new_file_anchor_path, filtered_data_anchor, delimiter='\t', fmt='%s', newline='\n', header=header, comments='')


dbm_data_id = np.arange(16, 20)
new_file_dbm_path = os.path.join(current_directory, f"{date}\\dbm_{filename}")
filtered_data_dbm = data[np.isin(data[:, 2].astype(float), dbm_data_id)]
filtered_data_dbm[:, 3] = np.where(filtered_data_dbm[:, 3].astype(float) < 50, filtered_data_dbm[:, 3].astype(float) + 90, filtered_data_dbm[:, 3])
np.savetxt(new_file_dbm_path, filtered_data_dbm, delimiter='\t', fmt='%s', newline='\n', header=header, comments='')

print("Data saved.")
