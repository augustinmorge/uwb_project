import os
import numpy as np
import matplotlib.pyplot as plt
import pyproj

def percent(array, mask, name = ""):
    print(f"Use {array[mask].shape[0]/array.shape[0]*100}% of data for {name}")

# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='WGS84', datum='WGS84')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# test = '01_06_2023\\charieau2'
# file_name = f"{test}\\flo_PH-2248_R_PHINS_STANDARD.log"

# test = '06_06_2023\chariot_3roues'
# file_name = f"{test}\chariot_3roues_PH-2248_R_PHINS_STANDARD.log"

test = '28_06_2023'
file_name = f"{current_directory}\\..\\{test}\\{test}_PH-2248_R_PHINS_STANDARD.log"

# file_path = os.path.join(current_directory, file_name)

######################### RECUPERATION DU HEADER #########################

with open(file_name, 'r') as file:
    header_lines = [next(file) for _ in range(4)]
header = ''.join(header_lines).rstrip('\t\n')
header_arr = np.array(header_lines[-1].split("\t"))

######################### RECUPERATION DES DONNES UTILES #########################

# Charger les données à partir du fichier en utilisant genfromtxt de numpy
data = np.genfromtxt(file_name, delimiter='\t', skip_header = 4, dtype='<U15')
anchor_id = np.arange(6016, 6020)
idx = np.isin(data[:, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(float), anchor_id)

# Extraire les colonnes correspondantes aux variables d'intérêt et les convertir en float64
time = data[idx, np.where(header_arr == 'Pc - HH:MM:SS.SSS')[0][0]]
gps_latitude = data[idx, np.where(header_arr == 'GPS - Latitude (deg)')[0][0]].astype(np.float64)
gps_longitude = data[idx, np.where(header_arr == 'GPS - Longitude (deg)')[0][0]].astype(np.float64)
gps_altitude = data[idx, np.where(header_arr == 'GPS - Altitude (m)')[0][0]].astype(np.float64)
beacon_ids = data[idx, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(np.float64)
beacon_latitudes = data[idx, np.where(header_arr == 'LBL - Latitude (deg)')[0][0]].astype(np.float64)
beacon_longitudes = data[idx, np.where(header_arr == 'LBL - Longitude (deg)')[0][0]].astype(np.float64)
beacon_depths = data[idx, np.where(header_arr == 'LBL - Altitude (m)')[0][0]].astype(np.float64)
lbl_range = np.float64(data[idx, np.where(header_arr == 'LBL - Range (m)')[0][0]])

time_s = np.array(list(map(lambda t: sum(float(x) * coef for x, coef in zip(t.split(':')[:-1], [3600, 60, 1]))
                              + float(t.split(':')[-1]) / 1000, time)))
                              
beacon_data = {}
for i in anchor_id:
    beacon_data[i] = {
        'time': time_s[beacon_ids == i],
        'gps_latitude': gps_latitude[beacon_ids == i],
        'gps_longitude': gps_longitude[beacon_ids == i],
        'gps_altitude': gps_altitude[beacon_ids == i],
        'beacon_latitudes': beacon_latitudes[beacon_ids == i],
        'beacon_longitudes': beacon_longitudes[beacon_ids == i],
        'beacon_depths': beacon_depths[beacon_ids == i],
        'lbl_range': lbl_range[beacon_ids == i]
    }

### EXTRACTION DE PUISSAAAAANCE ###
dbm_id = np.arange(16, 20)
idx_dbm = np.isin(data[:, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(float), dbm_id)

time_dbm_s = data[idx_dbm, np.where(header_arr == 'Pc - HH:MM:SS.SSS')[0][0]]
RXPower_FPPower = data[idx_dbm, np.where(header_arr == 'LBL - Range (m)')[0][0]].astype(np.float64)
beacon_ids_dbm = data[idx_dbm, np.where(header_arr == 'LBL - Beacon ID')[0][0]].astype(np.float64)
RXPower = -data[idx_dbm, np.where(header_arr == 'LBL - Latitude (deg)')[0][0]].astype(np.float64)
FPPower = -data[idx_dbm, np.where(header_arr == 'LBL - Longitude (deg)')[0][0]].astype(np.float64)
Quality = -data[idx_dbm, np.where(header_arr == 'LBL - Altitude (m)')[0][0]].astype(np.float64)

time_dbm_s = np.array(list(map(lambda t: sum(float(x) * coef for x, coef in zip(t.split(':')[:-1], [3600, 60, 1]))
                              + float(t.split(':')[-1]) / 1000, time_dbm_s)))

dbm_data = {}
for i in dbm_id:
    dbm_data[i] = {
        'time': time_dbm_s[beacon_ids_dbm == i],
        'RXPower_FPPower': RXPower_FPPower[beacon_ids_dbm == i],
        'RXPower': RXPower[beacon_ids_dbm == i],
        'FPPower': FPPower[beacon_ids_dbm == i],
        'Quality': Quality[beacon_ids_dbm == i]
    }


interpolate = 1
if interpolate:
    from scipy.interpolate import interp1d

    # # Interpolation pour anchor_id
    # anchor_interp_data = {}

    # # Interpolation pour dbm_id
    # dbm_interp_data = {}

    figrf, axsrf = plt.subplots(2,2)
    figrf.suptitle("RX - FP")
    figq, axsq = plt.subplots(2,2)
    figq.suptitle("Quality")
    figd, axsd = plt.subplots(2,2)
    figd.suptitle("Distance")
    for id in anchor_id:

        id_data = beacon_data[id]
        id_data_dbm = dbm_data[id-6000]

        start_time = max(min(id_data['time']), min(id_data_dbm['time']))
        end_time = min(max(id_data['time']), max(id_data_dbm['time']))
        dt = np.mean(np.diff(id_data_dbm['time']))

        T_glob = np.arange(start_time, end_time, dt)

        f_time = interp1d(id_data['time'], id_data['time'])
        time_interp = f_time(T_glob)

        f_gps_latitude = interp1d(id_data['time'], id_data['gps_latitude'])
        f_gps_longitude = interp1d(id_data['time'], id_data['gps_longitude'])
        f_gps_altitude = interp1d(id_data['time'], id_data['gps_altitude'])
        gps_latitude_interp = f_gps_latitude(T_glob)
        gps_longitude_interp = f_gps_longitude(T_glob)
        gps_altitude_interp = f_gps_altitude(T_glob)

        f_beacon_latitudes = interp1d(id_data['time'], id_data['beacon_latitudes'])
        f_beacon_longitudes = interp1d(id_data['time'], id_data['beacon_longitudes'])
        f_beacon_depths = interp1d(id_data['time'], id_data['beacon_depths'])
        f_lbl_range = interp1d(id_data['time'], id_data['lbl_range'])
        beacon_latitudes_interp = f_beacon_latitudes(T_glob)
        beacon_longitudes_interp = f_beacon_longitudes(T_glob)
        beacon_depths_interp = f_beacon_depths(T_glob)
        lbl_range_interp = f_lbl_range(T_glob)

        # Convertir les coordonnées de l'gps en coordonnées cartésiennes
        gps_x_interp, gps_y_interp = cartesian_proj(gps_longitude_interp, gps_latitude_interp)

        # Convertir les coordonnées des balises en coordonnées cartésiennes
        beacon_x_interp, beacon_y_interp = cartesian_proj(beacon_longitudes_interp, beacon_latitudes_interp)

        # anchor_interp_data[id] = {
        #     'time_interp': time_interp,
        #     'gps_latitude_interp': gps_latitude_interp,
        #     'gps_longitude_interp': gps_longitude_interp,
        #     'gps_altitude_interp': gps_altitude_interp,
        #     'beacon_latitudes_interp': beacon_latitudes_interp,
        #     'beacon_longitudes_interp': beacon_longitudes_interp,
        #     'beacon_depths_interp': beacon_depths_interp,
        #     'lbl_range_interp': lbl_range_interp,
        #     'gps_x' : gps_x,
        #     'gps_y' : gps_y,
        #     'beacon_x' : beacon_x,
        #     'beacon_y' : beacon_y,
        # }

        f_time_dbm = interp1d(id_data_dbm['time'], id_data_dbm['time'])
        time_dbm_interp = f_time_dbm(T_glob)

        f_RXPower_FPPower = interp1d(id_data_dbm['time'], id_data_dbm['RXPower_FPPower'])
        f_RXPower = interp1d(id_data_dbm['time'], id_data_dbm['RXPower'])
        f_FPPower = interp1d(id_data_dbm['time'], id_data_dbm['FPPower'])
        f_Quality = interp1d(id_data_dbm['time'], id_data_dbm['Quality'])
        RXPower_FPPower_interp = f_RXPower_FPPower(T_glob)
        RXPower_interp = f_RXPower(T_glob)
        FPPower_interp = f_FPPower(T_glob)
        Quality_interp = f_Quality(T_glob)

        # dbm_interp_data[id-6000] = {
        #     'time_dbm_interp': time_dbm_interp,
        #     'RXPower_FPPower_interp': RXPower_FPPower_interp,
        #     'RXPower_interp': RXPower_interp,
        #     'FPPower_interp': FPPower_interp,
        #     'Quality_interp': Quality_interp
        # }

        
        # current_time = time_interp[mask_interp]

        # Calculer la distance entre l'gps et le balise actuel
        distance_interp = np.sqrt((gps_x_interp - beacon_x_interp)**2 +
                                (gps_y_interp - beacon_y_interp)**2 +
                                (gps_altitude_interp - beacon_depths_interp)**2)
        
        nid = id - 6016
        axrf = axsrf[nid//2, nid%2]
        axrf.set_title(f"Erreur en fonction de la distance {id}")
        axrf.scatter(RXPower_FPPower_interp, distance_interp-lbl_range_interp, label = 'f(err)', s = 0.5, color = 'black')
        axrf.set_ylabel("erreur [m]")
        axrf.set_xlabel("RX - FP")

        axq = axsq[nid//2, nid%2]
        axq.set_title(f"Erreur en fonction de la distance {id}")
        axq.scatter(Quality_interp, distance_interp-lbl_range_interp, label = 'f(err)', s = 0.5, color = 'black')
        axq.set_ylabel("erreur [m]")
        axq.set_xlabel("Quality")

        axd = axsd[nid//2, nid%2]
        axd.set_title(f"Distance {id}")
        axd.plot(T_glob, distance_interp, label = 'distance', color = 'black')
        axd.set_ylabel("distance [m]")
        axd.set_xlabel("time [s]")

        # plt.figure()
        # plt.title(id)
        # plt.plot(T_glob, distance)


# Convertir les coordonnées de l'gps en coordonnées cartésiennes
gps_x, gps_y = cartesian_proj(gps_longitude, gps_latitude)

# Convertir les coordonnées des balises en coordonnées cartésiennes
beacon_x, beacon_y = cartesian_proj(beacon_longitudes, beacon_latitudes)

# #Ajout des bras de levier
print("ATTENTION : Bras de levier à voir en fonction !!")

# gps_x += -0.492
# gps_y += 0.169
# gps_altitude += 0.728

# beacon_x += 0.080
# beacon_y += 0.211
# beacon_depths += 1.183

#Ajout des bras de levier
gps_x -= -0.698
gps_y -= 0.2
gps_altitude -= 1.170

beacon_x -= -1.444
beacon_y -= -0.173
beacon_depths -= 0.672

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

        ax_err1 = axes1[i]

        # Filtrer les données pour le balise ID actuel
        mask = (beacon_ids == beacon_id)
        mask_dbm = (beacon_ids_dbm == beacon_id - 6000)

        mask[0:10] = False
        mask_dbm[0:10] = False
        
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

        N = distance.shape[0]
        print(f"For beacon {hex(int(beacon_id))} the mean error is {np.mean(distance[:N,] - lbl_range[mask][:N,])}; the sd of {np.std(distance[:N,] - (lbl_range[mask][:N,]))}")


        ## f(err) ##
        fig1.suptitle("Erreur en fonction de la distance")
        ax_err1.set_title(f'Beacon ID {hex(int(beacon_id))}')
        ax_err1.scatter(distance, distance-lbl_range[mask], label = 'f(err)', s = 1, color = 'black')
        ax_err1.set_ylabel("erreur [m]")
        ax_err1.set_xlabel("distance (vraie) [m]")
        ax_err1.set_ylim([-alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask]),alph*np.std(distance - lbl_range[mask]) + np.mean(distance - lbl_range[mask])])

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

# etalonnage()

with open(os.path.join(current_directory,f"offset.txt"),"w") as file:
    file.write("Beacon ID : offset\n")
    for elem in list_offset:
        file.write(str(elem[0]) + ":" + str(elem[1]) + "\n")
    file.close()

if __name__ == "__main__":
    plt.show()