import os
import numpy as np
# import display_data

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

test = '28_06_2023'
file_path = current_directory + f"\\..\\{test}\\anchor_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.txt"

# Chemin absolu du fichier d'offset
offset_file_name = "offset.txt"
offset_file_path = os.path.join(current_directory, offset_file_name)

######################### RECUPERATION DU HEADER #########################

with open(file_path, 'r') as file:
    header_lines = [next(file) for _ in range(12)]
header = ''.join(header_lines).rstrip('\t\n')
header_arr = np.array(header_lines[-1].split("\t"))

######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_path, delimiter='\t', skip_header=12, dtype='<U15')

offset = {}
with open(offset_file_path, 'r') as offset_file:
    offset_header = offset_file.readline().strip()
    lines = offset_file.readlines()
    for line in lines:
        line = line.strip()
        beacon_id, offset_value = line.split(':')
        offset[float(beacon_id)] = float(offset_value)

new_data = data.copy()

for i in range(len(new_data)):
    if float(new_data[i, 2]) in offset.keys():
        # Change range
        if i > 0:
            if new_data[i,6] != new_data[i-1,6]: 
                new_data[i, 6] = str(float(new_data[i, 6]) + offset[int(new_data[i, 2])])

        #Change std
        new_data[i, 7] = str(1)

# Ecrire un nouveau fichier
new_file_path = os.path.join(current_directory, f"{test}\\new_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.txt")

# with open(new_file_path, 'w') as new_file:
#     # Écrire le header dans le nouveau fichier
#     new_file.write(header + '\n')
#     # Écrire les données modifiées dans le nouveau fichier
#     np.savetxt(new_file, new_data, delimiter='\t', fmt='%s')

# print("Data saved.")
