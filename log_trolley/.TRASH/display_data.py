import os
import numpy as np
import matplotlib.pyplot as plt
import pyproj

def percent(array, mask, name = ""):
    print(f"Use {array[mask].shape[0]/array.shape[0]*100}% of data for {name}")

# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='ECEF', datum='ECEF')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# test = '01_06_2023\\charieau2'
# file_name = f"{test}\\flo_PH-2248_R_PHINS_STANDARD.log"

# test = '06_06_2023\chariot_3roues'
# file_name = f"{test}\chariot_3roues_PH-2248_R_PHINS_STANDARD.log"

test = '12_06_2023'
file_name = f"{current_directory}\\..\\{test}\{test}_PH-2248_R_PHINS_STANDARD.log"

# file_path = os.path.join(current_directory, file_name)

######################### RECUPERATION DU HEADER #########################

with open(file_name, 'r') as file:
    header_lines = [next(file) for _ in range(4)]
header = ''.join(header_lines).rstrip('\t\n')
header_arr = np.array(header_lines[-1].split("\t"))

######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_name, delimiter='\t', skip_header = 4, dtype='<U15')
lbl_range = np.float64(data[:, np.where(header_arr == 'LBL - Range (m)')[0][0]])
for i in range(1,lbl_range.shape[0]): 
    if lbl_range[i] < 0 : lbl_range[i] = lbl_range[i - 1]

# Extraire les colonnes correspondantes aux variables d'intérêt et les convertir en float64
time = data[:, np.where(header_arr == 'Pc - HH:MM:SS.SSS')[0][0]]
gps_latitude = data[:, np.where(header_arr == 'GPS - Latitude (deg)')[0][0]].astype(np.float64)
gps_longitude = data[:, np.where(header_arr == 'GPS - Longitude (deg)')[0][0]].astype(np.float64)
gps_altitude = data[:, np.where(header_arr == 'GPS - Altitude (m)')[0][0]].astype(np.float64)
beacon_ids = data[:, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(np.float64)
beacon_latitudes = data[:, np.where(header_arr == 'LBL - Latitude (deg)')[0][0]].astype(np.float64)
beacon_longitudes = data[:, np.where(header_arr == 'LBL - Longitude (deg)')[0][0]].astype(np.float64)
beacon_depths = data[:, np.where(header_arr == 'LBL - Altitude (m)')[0][0]].astype(np.float64)

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


print(np.unique(gps_altitude).shape[0]/gps_altitude.shape[0])
print(np.unique(gps_altitude).shape)
print(gps_altitude.shape)

# plt.figure()
# plt.plot(time[100:], gps_altitude[100:])
# plt.show()

# Créer les sous-graphiques pour chaque balise
unique_beacon_ids = np.unique(beacon_ids)
num_subplots = len(unique_beacon_ids)

def show_results():
    # Créer les sous-graphiques pour chaque balise
    fig, axes = plt.subplots(2, 4, figsize=(10, 10))
    fig1, axes1 = plt.subplots(1, 4, figsize=(10, 10))
    date = header_lines[2].split("\t")[1]
    fig.suptitle(f"{date}")

    for i, beacon_id in enumerate(unique_beacon_ids):
        ax = axes[0,i]
        ax2 = axes[1,i]

        ax_err = axes1[i]

        # Filtrer les données pour le balise ID actuel
        mask = (beacon_ids == beacon_id)

        mask[0:10] = False
        
        current_time = time[mask]
        current_beacon_x = beacon_x[mask]
        current_beacon_y = beacon_y[mask]
        current_beacon_depths = beacon_depths[mask]

        current_gps_x = gps_x[mask]
        current_gps_y = gps_y[mask]
        current_gps_altitude = gps_altitude[mask]

        # Calculer la distance entre l'gps et le balise actuel
        distance = np.sqrt((current_gps_x - current_beacon_x)**2 +
                        (current_gps_y - current_beacon_y)**2 +
                        (current_gps_altitude - current_beacon_depths)**2)


        # Tracer les estimations de distance pour le balise actuel
        ax.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax.scatter(current_time, distance, label='d(GPS - anchor)', marker='x', color='blue', s=1)
        ax.scatter(current_time, lbl_range[mask], label='LBL - Range (m)', marker='x', color='orange', s=1)

        ax2.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax2.scatter(current_time, distance-lbl_range[mask], label='d(GPS - anchor) - LBL - Range (m)', marker='x', color='black', s=1)
        ax2.plot(current_time, np.mean(distance-lbl_range[mask])*np.ones(current_time.shape[0]), label=f'mean = {int(np.mean(distance-lbl_range[mask])*100)/100}', color='red')

        # Configurer les propriétés du sous-graphique
        ax.set_ylabel('Distance (m)')
        ax.legend()

        ax2.set_ylabel('Distance (m)')
        ax2.legend()

        # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
        xticks_indices = np.linspace(0, np.sum(mask), num=4, dtype=int)
        ax.set_xticks(xticks_indices)
        ax.set_xticklabels(time[xticks_indices])

        ax2.set_xticks(xticks_indices)
        ax2.set_xticklabels(time[xticks_indices])

        alph = 3
        ax2.set_ylim([-alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])
        ax.set_ylim( [min(-alph*np.std(distance) + np.mean(distance),-alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])),\
                    max( alph*np.std(distance) + np.mean(distance), alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])) ] )

        N = distance.shape[0]//4
        print(f"For beacon {hex(int(beacon_id))} the mean error is {np.mean(distance[:N,] - lbl_range[mask][:N,])}; the sd of {np.std(distance[:N,] - (lbl_range[mask][:N,]))}")


        ## f(err) ##
        fig1.suptitle("Erreur en fonction de la distance")
        ax_err.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax_err.scatter(distance, distance-lbl_range[mask], label = 'f(err)', s = 1, color = 'black')
        ax_err.set_ylabel("erreur [m]")
        ax_err.set_xlabel("distance (vraie) [m]")
        ax_err.set_ylim([-alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])

show_results()

from datetime import datetime

def select_time_idx(starting_values_idx, time):
    datetime_objects = [datetime.strptime(t, '%H:%M:%S.%f') for t in time]
    np_datetime_objects = np.array(datetime_objects, dtype='datetime64')
    elapsed_times = np_datetime_objects - np_datetime_objects[0]
    desired_duration = np.timedelta64(starting_values_idx, 's')
    index = np.where(elapsed_times >= desired_duration)[0][0]
    return index

list_offset = []
def etalonnage():
    ## ETALONNAGE ##
    
    starting_values_idx = int(input("Combien de temps pour l'étalonnage [s] ? "))
    # datetime_objects = [datetime.strptime(t, '%H:%M:%S.%f') for t in time]
    # np_datetime_objects = np.array(datetime_objects, dtype='datetime64')
    # elapsed_times = np_datetime_objects - np_datetime_objects[0]
    # desired_duration = np.timedelta64(starting_values_idx, 's')
    # index = np.where(elapsed_times >= desired_duration)[0][0]
    # print("L'index correspondant à une durée de", starting_values_idx, "secondes est :", index)

    fig, axes = plt.subplots(2, 4, figsize=(10, 10))
    date = header_lines[2].split("\t")[1]
    fig.suptitle(f"{date} avec étalonnage de {starting_values_idx}s")

    for i, beacon_id in enumerate(unique_beacon_ids):
        ax = axes[0,i]
        ax2 = axes[1,i]

        # Filtrer les données pour le balise ID actuel
        mask = (beacon_ids == beacon_id)

        mask[0:10] = False
        
        current_time = time[mask]
        index = select_time_idx(starting_values_idx, current_time)

        current_beacon_x = beacon_x[mask]
        current_beacon_y = beacon_y[mask]
        current_beacon_depths = beacon_depths[mask]

        current_gps_x = gps_x[mask]
        current_gps_y = gps_y[mask]
        current_gps_altitude = gps_altitude[mask]

        # Calculer la distance entre l'gps et le balise actuel
        distance = np.sqrt((current_gps_x - current_beacon_x)**2 +
                        (current_gps_y - current_beacon_y)**2 +
                        (current_gps_altitude - current_beacon_depths)**2)


        ## SET THE OFFSET ##
        # offset = np.mean(distance[:index,]-lbl_range[mask][:index,])

        diff_indices = np.concatenate(([True], np.diff(lbl_range[:index]) != 0))
        offset = np.mean(distance[:index][diff_indices] - lbl_range[mask][:index][diff_indices])



        list_offset.append([beacon_id, offset])

        # Tracer les estimations de distance pour le balise actuel
        ax.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax.scatter(current_time, distance, label='d(GPS - anchor)', marker='x', color='blue', s=1)
        ax.scatter(current_time, lbl_range[mask] + offset, label='LBL - Range (m) + offset', marker='x', color='green', s=1)
        ax.plot([current_time[index]]*current_time.shape[0], np.linspace(np.min(distance)-50,np.max(distance)+50,current_time.shape[0]),color='purple')

        ax2.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax2.scatter(current_time, distance-(lbl_range[mask]+offset), label='d(GPS - anchor) - LBL - Range (m) + offset', marker='x', color='green', s=1)
        ax2.plot(current_time, np.mean(distance-(lbl_range[mask]+offset))*np.ones(current_time.shape[0]), label=f'mean = {int(np.mean(distance-(lbl_range[mask]+offset))*100)/100}', color='red')

        # Configurer les propriétés du sous-graphique
        ax.set_ylabel('Distance (m)')
        ax.legend()

        ax2.set_ylabel('Distance (m)')
        ax2.legend()

        # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
        xticks_indices = np.linspace(0, np.sum(mask), num=4, dtype=int)
        ax.set_xticks(xticks_indices)
        ax.set_xticklabels(time[xticks_indices])

        ax2.set_xticks(xticks_indices)
        ax2.set_xticklabels(time[xticks_indices])

        alph = 3
        ax2.set_ylim([-alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])
        ax.set_ylim( [min(-alph*np.std(distance) + np.mean(distance),-alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])),\
                    max( alph*np.std(distance) + np.mean(distance), alph*np.std(lbl_range[mask]) + np.mean(lbl_range[mask])) ] )

        N = distance.shape[0]//4
        print(f"For beacon {hex(int(beacon_id))} the mean error is {np.mean(distance[N:,] - (lbl_range[mask][N:,]+offset))}; the sd of {np.std(distance[N:,] - (lbl_range[mask][N:,]+offset))} and the offset is {offset}")

    # plt.tight_layout()

etalonnage()

with open(os.path.join(current_directory,f"offset.txt"),"w") as file:
    file.write("Beacon ID : offset\n")
    for elem in list_offset:
        file.write(str(elem[0]) + ":" + str(elem[1]) + "\n")
    file.close()

if __name__ == "__main__":
    plt.show()