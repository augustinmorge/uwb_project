import os
import numpy as np
import pyproj
# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='WGS84', datum='WGS84')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

test = '12_06_2023'
file_uwb = f"{test}\{test}_PH-2248_A_POSTPROCESSING-ins.xpf.txt"
file_ins = f"{test}\{test}_PH-2248_R_PHINS_STANDARD.log"

file_path_uwb = os.path.join(current_directory, file_uwb)
file_path_ins = os.path.join(current_directory, file_ins)

######################### RECUPERATION DU HEADER #########################

with open(file_path_ins, 'r') as file:
    header_lines = [next(file) for _ in range(4)]
header = ''.join(header_lines).rstrip('\t\n')
header_arr = np.array(header_lines[-1].split("\t"))

print(header_arr)
######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data_ins = np.genfromtxt(file_path_ins, delimiter='\t', skip_header=4, dtype='<U15')
data_uwb = np.genfromtxt(file_path_uwb, delimiter='\t', skip_header=12, dtype='<U15')

new_data = data_uwb.copy()

# Extraire les colonnes correspondantes aux variables d'intérêt et les convertir en float64
lbl_range = data_ins[:, np.where(header_arr == 'LBL - Range (m)')[0][0]].astype(np.float64)
time = data_ins[:, np.where(header_arr == 'Pc - HH:MM:SS.SSS')[0][0]]
gps_latitude = data_ins[:, np.where(header_arr == 'GPS - Latitude (deg)')[0][0]].astype(np.float64)
gps_longitude = data_ins[:, np.where(header_arr == 'GPS - Longitude (deg)')[0][0]].astype(np.float64)
gps_altitude = data_ins[:, np.where(header_arr == 'GPS - Altitude (m)')[0][0]].astype(np.float64)
beacon_ids = data_ins[:, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(np.float64)
beacon_latitudes = data_ins[:, np.where(header_arr == 'LBL - Latitude (deg)')[0][0]].astype(np.float64)
beacon_longitudes = data_ins[:, np.where(header_arr == 'LBL - Longitude (deg)')[0][0]].astype(np.float64)
beacon_depths = data_ins[:, np.where(header_arr == 'LBL - Altitude (m)')[0][0]].astype(np.float64)

# Convertir les coordonnées de l'gps en coordonnées cartésiennes
gps_x, gps_y = cartesian_proj(gps_longitude, gps_latitude)

# Convertir les coordonnées des balises en coordonnées cartésiennes
beacon_x, beacon_y = cartesian_proj(beacon_longitudes, beacon_latitudes)

#Ajout des bras de levier
gps_x += -0.492
gps_y += 0.169
gps_altitude += 0.728

beacon_x += 0.080
beacon_y += 0.211
beacon_depths += 1.183

# Calculer la distance entre l'gps et le balise actuel

print(str(np.sqrt((gps_x - beacon_x)**2 + \
                    (gps_y - beacon_y)**2 + \
                    (gps_altitude - beacon_depths)**2))
)
new_data[:, 6] = np.sqrt((gps_x - beacon_x)**2 + \
                    (gps_y - beacon_y)**2 + \
                    (gps_altitude - beacon_depths)**2)

# Ecrire un nouveau fichier
new_file_path = os.path.join(current_directory, f"{test}\\true_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.txt")

with open(file_path_uwb, 'r') as file:
    header_lines = [next(file) for _ in range(12)]
header_uwb = ''.join(header_lines).rstrip('\t\n')

# with open(new_file_path, 'w') as new_file:
#     # Écrire le header dans le nouveau fichier
#     new_file.write(header_uwb + '\n')
#     # Écrire les données modifiées dans le nouveau fichier
#     np.savetxt(new_file, new_data, delimiter='\t', fmt='%s')

# print("Data saved.")
