import os
import numpy as np
import matplotlib.pyplot as plt
import pyproj

# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='WGS84', datum='WGS84')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# test = '00_05_2023\\charieau2'
# file_name = f"{test}\\flo_PH-2248_R_PHINS_STANDARD.log"

test = '06_06_2023\\chariot_3roues'
file_name = f"{test}\chariot_3roues_PH-2248_R_PHINS_STANDARD.log"

file_path = os.path.join(current_directory, file_name)

######################### RECUPERATION DU HEADER #########################

with open(file_path, 'r') as file:
    header_lines = [next(file) for _ in range(4)]
header = ''.join(header_lines).rstrip('\t\n')
header_arr = np.array(header_lines[-1].split("\t"))



######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_path, delimiter='\t', skip_header = 4, dtype='<U15')
lbl_range = np.float64(data[:, np.where(header_arr == 'LBL - Range (m)')[0][0]])
for i in range(1,lbl_range.shape[0]): 
    if lbl_range[i] < 0 : lbl_range[i] = lbl_range[i - 1]

# Extraire les colonnes correspondantes aux variables d'intérêt et les convertir en float64
time = data[:, np.where(header_arr == 'Pc - HH:MM:SS.SSS')[0][0]]
ins_latitude = data[:, np.where(header_arr == 'GPS - Latitude (deg)')[0][0]].astype(np.float64)
ins_longitude = data[:, np.where(header_arr == 'GPS - Longitude (deg)')[0][0]].astype(np.float64)
ins_altitude = data[:, np.where(header_arr == 'GPS - Altitude (m)')[0][0]].astype(np.float64)
beacon_ids = data[:, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(np.float64)
beacon_latitudes = data[:, np.where(header_arr == 'LBL - Latitude (deg)')[0][0]].astype(np.float64)
beacon_longitudes = data[:, np.where(header_arr == 'LBL - Longitude (deg)')[0][0]].astype(np.float64)
beacon_depths = data[:, np.where(header_arr == 'LBL - Altitude (m)')[0][0]].astype(np.float64)

# Convertir les coordonnées de l'INS en coordonnées cartésiennes
ins_x, ins_y = cartesian_proj(ins_longitude, ins_latitude)

# Convertir les coordonnées des balises en coordonnées cartésiennes
beacon_x, beacon_y = cartesian_proj(beacon_longitudes, beacon_latitudes)

# Créer les sous-graphiques pour chaque balise
unique_beacon_ids = np.unique(beacon_ids)
num_subplots = len(unique_beacon_ids)

# Créer les sous-graphiques pour chaque balise
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
fig2, axes2 = plt.subplots(2, 2, figsize=(10, 10))
date = header_lines[2].split("\t")[1]
fig.suptitle(f"{date}")
fig2.suptitle(f"{date}")

for i, beacon_id in enumerate(unique_beacon_ids):
    row = i // 2  # Rangée correspondante (0 ou 1)
    col = i % 2   # Colonne correspondante (0 ou 1)

    ax = axes[row, col]
    ax2 = axes2[row, col]

    # Filtrer les données pour le balise ID actuel
    mask = (beacon_ids == beacon_id)
    mask[0:10] = False
    
    current_beacon_x = beacon_x[mask]
    current_beacon_y = beacon_y[mask]
    current_beacon_depths = beacon_depths[mask]

    current_ins_x = ins_x[mask]
    current_ins_y = ins_y[mask]
    current_ins_altitude = ins_altitude[mask]

    # Calculer la distance entre l'INS et le balise actuel
    distance = np.sqrt((current_ins_x - current_beacon_x)**2 +
                       (current_ins_y - current_beacon_y)**2 +
                       (current_ins_altitude - current_beacon_depths)**2)


    # Tracer les estimations de distance pour le balise actuel
    ax.set_title(f'Beacon ID {hex(int(beacon_id))}')
    ax.scatter(time[mask], distance, label='d(GPS - anchor)', marker='x', color='blue', s=1)
    ax.scatter(time[mask], lbl_range[mask], label='LBL - Range (m)', marker='x', color='orange', s=1)

    ax2.set_title(f'Beacon ID {hex(int(beacon_id))}')
    ax2.scatter(time[mask], distance-lbl_range[mask], label='d(GPS - anchor) - LBL - Range (m)', marker='x', color='blue', s=1)

    # Configurer les propriétés du sous-graphique
    ax.set_ylabel('Distance (m)')
    ax.legend()

    ax2.set_ylabel('Distance (m)')
    ax2.legend()

    # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
    xticks_indices = np.linspace(0, np.sum(mask), num=5, dtype=int)
    ax.set_xticks(xticks_indices)
    ax.set_xticklabels(time[xticks_indices])

    ax2.set_xticks(xticks_indices)
    ax2.set_xticklabels(time[xticks_indices])
    ax2.set_ylim([-3*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),3*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])
    ax.set_ylim( [min(-3*np.std(distance) + np.mean(distance),-3*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])),\
                  max( 3*np.std(distance) + np.mean(distance), 3*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])) ] )

    print(f"For beacon {hex(int(beacon_id))} the mean error is {np.mean(distance - lbl_range[mask])}")

plt.tight_layout()
plt.show()