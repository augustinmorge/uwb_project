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

import os, sys
import numpy as np

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# date = '28_06_2023'
# date = "03_07_2023"
# date = "05_07_2023"
# date = "11_07_2023"
# date = "17_07_2023_2"
date = "26_07_2023"

filename = f'{date}_PH-2248_A_POSTPROCESSING-ins.xpf.txt'
file_name = f"\\..\\{date}\\{filename}"
file_path = current_directory + file_name

######################### RECUPERATION DU HEADER #########################

with open(file_path, 'r') as file:
    header_lines = [next(file) for _ in range(12)]
header = ''.join(header_lines).rstrip('\t\n')
######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_path, delimiter='\t', skip_header=12, dtype='<U15')
anchor_id = np.arange(6016, 6020)
new_file_anchor_path = current_directory + f"\\..\\{date}\\anchor_{filename}"
filtered_data_anchor = data[np.isin(data[:, 2].astype(float), anchor_id)]

dbm_data_id = np.arange(16, 20)
new_file_dbm_path = current_directory + f"\\..\\{date}\\dbm_{filename}"
filtered_data_dbm = data[np.isin(data[:, 2].astype(float), dbm_data_id)]

if filtered_data_anchor[0, 5].astype(float) > -100:
    print("Have to change altitude :")
    print("old altititude: ", filtered_data_anchor[:, 5])
    filtered_data_anchor[:, 5] = (filtered_data_anchor[:, 5].astype(float) - 47.26).astype(str) # Conversion en chaînes de caractères
print("new altitude : ", filtered_data_anchor[:, 5])

#Change l'écart-type
val_std = 1
filtered_data_anchor[:, 7] = f'{val_std}'

adapt = 1
if adapt:
    from tqdm import tqdm
    matching_indices = []
    dbm_time_seconds = np.array([time.split(':')[0] for time in filtered_data_dbm[:, 1]]).astype(float) * 3600 + np.array([time.split(':')[1] for time in filtered_data_dbm[:, 1]]).astype(float) * 60 + np.array([time.split(':')[2] for time in filtered_data_dbm[:, 1]]).astype(float)
    print("\nAdapt the std value with RX - FP..")
    for i in tqdm(range(filtered_data_anchor.shape[0])):
        row_anchor = filtered_data_anchor[i]
        anchor_time = row_anchor[1]
        anchor_beacon_id = row_anchor[2]
        anchor_range = float(row_anchor[6])
        
        anchor_time_parts = anchor_time.split(':')
        anchor_seconds = float(anchor_time_parts[0]) * 3600 + float(anchor_time_parts[1]) * 60 + float(anchor_time_parts[2])
        
        # Trouver l'indice du temps le plus proche dans dbm_time_seconds
        time_diffs = np.abs(dbm_time_seconds - anchor_seconds)
        closest_dbm_time_index = np.argmin(time_diffs)
        
        # Vérifier si la différence de temps est inférieure à 0.1 seconde
        if time_diffs[closest_dbm_time_index] < 0.5:
            dbm_beacon_id = int(filtered_data_dbm[closest_dbm_time_index, 2])
            if (int(dbm_beacon_id + 6000) == int(anchor_beacon_id)) and float(filtered_data_dbm[closest_dbm_time_index, 6]) < 6:
                matching_indices.append(closest_dbm_time_index)

    # Mettre à jour les valeurs en une seule opération
    filtered_data_anchor[matching_indices, 7] = '0.5'
    print(f"Updated val_std for {len(matching_indices)}/{filtered_data_anchor.shape[0]} anchors data\n")


if date == '11_07_2023':
    # print("Old atitude for 6018: ", filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3])
    lat82 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3][0][10]
    lon82 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 4][0][10]
    depth82 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 5][0][10]
    lat83 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 3][0][10]
    lon83 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 4][0][10]
    depth83 = filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 5][0][10]
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3] = (lat83.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3].shape)).astype(str)
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 4] = (lon83.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3].shape)).astype(str)
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 5] = (depth83.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3].shape)).astype(str)
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 3] = (lat82.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 3].shape)).astype(str)
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 4] = (lon82.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 3].shape)).astype(str)
    filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 5] = (depth82.astype(float)*np.ones(filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6019), 3].shape)).astype(str)
    print(f"Change lat/lon for 82 and 83 in {date}")
    # print("New atitude for 6018: ", filtered_data_anchor[np.where(filtered_data_anchor[:, 2].astype(float) == 6018), 3])


np.savetxt(new_file_anchor_path, filtered_data_anchor, delimiter='\t', fmt='%s', newline='\n', header=header, comments='')
np.savetxt(new_file_dbm_path, filtered_data_dbm, delimiter='\t', fmt='%s', newline='\n', header=header, comments='')

print("Data saved.")
