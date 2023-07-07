import os
import numpy as np
import pyproj
from xpf2py.xpf2py import xpf2py

# test = '28_06_2023'
# test = '03_07_2023'
test = '05_07_2023'

interpolate = 1
without_alignement = 1
whitout_jump = 0
print(f"We interpolate data : {interpolate==1}")
print(f"We compute with alignement : {without_alignement==0}")

sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))
# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='WGS84 ', datum='WGS84')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# test = '01_06_2023\\charieau2'
# file_name = f"{test}\\flo_PH-2248_R_PHINS_STANDARD.log"

# test = '06_06_2023\chariot_3roues'
# file_name = f"{test}\chariot_3roues_PH-2248_R_PHINS_STANDARD.log"


file_name = f"{current_directory}\\{test}\\{test}_PH-2248_R_PHINS_STANDARD.log"

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

time_s = np.array([float(t.split(":")[0])*3600 + float(t.split(":")[1])*60 + float(t.split(":")[2]) for t in time])

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

### EXTRACTION DES FACTEURS DE QUALITE ###
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


if whitout_jump:
    window_size = 50
    idx_start = np.where(time_s > (time_s[0] + 15*60))[0][0] #Les minutes d'alignement
    print(time_s[idx_start])
    try:
        idx_jump = np.where(np.diff(time_s) > 60)[0][0]
    except:
        idx_jump = -1
    time_s = time_s[idx_start:idx_jump,]
    gps_latitude = gps_latitude[idx_start:idx_jump,]
    gps_longitude = gps_longitude[idx_start:idx_jump,]
    gps_altitude = gps_altitude[idx_start:idx_jump,]
    beacon_ids = beacon_ids[idx_start:idx_jump,]
    beacon_latitudes = beacon_latitudes[idx_start:idx_jump,]
    beacon_longitudes = beacon_longitudes[idx_start:idx_jump,]
    beacon_depths = beacon_depths[idx_start:idx_jump,]
    lbl_range = lbl_range[idx_start:idx_jump,]

    time_dbm_s = time_dbm_s[idx_start:idx_jump,]
    RXPower_FPPower = RXPower_FPPower[idx_start:idx_jump,]
    beacon_ids_dbm = beacon_ids_dbm[idx_start:idx_jump,]
    RXPower = RXPower[idx_start:idx_jump,]
    FPPower = FPPower[idx_start:idx_jump,]
    Quality = Quality[idx_start:idx_jump,]

dbm_data = {}
for i in dbm_id:
    dbm_data[i] = {
        'time': time_dbm_s[beacon_ids_dbm == i],
        'RXPower_FPPower': RXPower_FPPower[beacon_ids_dbm == i],
        'RXPower': RXPower[beacon_ids_dbm == i],
        'FPPower': FPPower[beacon_ids_dbm == i],
        'Quality': Quality[beacon_ids_dbm == i]
    }

### EXTRACTION DE L'INNOVATION ###
# file_path = f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-replay.xpf"
file_path = f"{current_directory}\\{test}\\{test}_for_analize.xpf"
print(file_path)

xpf_content,py_fileOutPath = xpf2py(file_path, CheckExistence = True )
# print(xpf_content.keys())
# print(xpf_content["data"].keys())
# print(xpf_content["data"]["RANGE_KAL_MEAS"].keys())

date_s = xpf_content["data"]['RANGE_KAL_MEAS']["date"].astype(float)/10**7

# print(date_s)
# print(xpf_content["data"]['RANGE_KAL_MEAS']["lbl1DistOInnov"])
# print("\n####\n")
# print("Start of the data at ", xpf_content["data"]["UTC"])

utc_offset = (xpf_content["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_content["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_content["data"]["UTC"]["utcSecond"].astype(float)
innov_o = {6016 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl3DistOInnov"].astype(float).squeeze(), \
           6017 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl4DistOInnov"].astype(float).squeeze(), \
           6018 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl1DistOInnov"].astype(float).squeeze(), \
           6019 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl2DistOInnov"].astype(float).squeeze()}

d_meas_xpf = {6016 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl3distance"].astype(float).squeeze(), \
            6017 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl4distance"].astype(float).squeeze(), \
            6018 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl1distance"].astype(float).squeeze(), \
            6019 : xpf_content["data"]['RANGE_KAL_MEAS']["lbl2distance"].astype(float).squeeze()}

heading = xpf_content["data"]["primary_nav"]["heading"].squeeze()*np.pi/180
if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (3 + 7*365/12): 
    heading += np.pi
time_ins_s = (xpf_content["data"]["primary_nav"]["date"].astype(float)/10**7 + utc_offset).squeeze()

ins_latitude = (xpf_content["data"]["primary_nav"]["latitude"]).astype(float).squeeze()
ins_longitude = (xpf_content["data"]["primary_nav"]["longitude"]).astype(float).squeeze()
ins_altitude = (xpf_content["data"]["primary_nav"]["orthometricHeight"]).astype(float).squeeze()

time_innov_s = (utc_offset + date_s).squeeze()

def debug(args_s, args):
    for i in range(len(args)):
        print(args_s[i] + " : ", args[i])


WA_idx = {}
if interpolate:
    from scipy.interpolate import interp1d

    # Interpolation pour anchor_id
    anchor_interp_data = {}

    # Interpolation pour dbm_id
    dbm_interp_data = {}

    for id in anchor_id:

        id_data = beacon_data[id]
        id_data_dbm = dbm_data[id-6000]

        try :
            start_time = max(id_data['time'][0], id_data_dbm['time'][0],time_innov_s[0])
        except:
            print("No dBm data")
            break
        end_time = min(id_data['time'][-1], id_data_dbm['time'][-1],time_innov_s[-1])
        dt = 1 #min(min(np.mean(np.diff(id_data['time'])),np.mean(np.diff(id_data_dbm['time']))),np.mean(np.diff(time_innov_s)))
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

        f_RXPower_FPPower = interp1d(id_data_dbm['time'], id_data_dbm['RXPower_FPPower'])
        f_RXPower = interp1d(id_data_dbm['time'], id_data_dbm['RXPower'])
        f_FPPower = interp1d(id_data_dbm['time'], id_data_dbm['FPPower'])
        f_Quality = interp1d(id_data_dbm['time'], id_data_dbm['Quality'])
        RXPower_FPPower_interp = f_RXPower_FPPower(T_glob)
        RXPower_interp = f_RXPower(T_glob)
        FPPower_interp = f_FPPower(T_glob)
        Quality_interp = f_Quality(T_glob)

        f_innov_o = interp1d(time_innov_s, innov_o[id])
        f_d_meas_xpf = interp1d(time_innov_s, d_meas_xpf[id])
        Innov_o = f_innov_o(T_glob)
        d_meas_xpf_id = f_d_meas_xpf(T_glob)

        ### IMPORT INS DATA ###
        f_heading = interp1d(time_ins_s, heading)
        f_ins_latitude = interp1d(time_ins_s, ins_latitude)
        f_ins_longitude = interp1d(time_ins_s, ins_longitude)
        f_ins_altitude = interp1d(time_ins_s, ins_altitude)
        heading_interp = f_heading(T_glob)
        ins_longitude_interp = f_ins_latitude(T_glob)
        ins_latitude_interp = f_ins_longitude(T_glob)
        ins_altitude_interp = f_ins_altitude(T_glob)

        ins_x_interp, ins_y_interp = cartesian_proj(ins_longitude_interp, ins_latitude_interp)

        if without_alignement:
            val_to_mean = 20
            beta = 0.05
            diff_values = np.diff(d_meas_xpf_id)

            start_idx = 0
            for i in range(20 + val_to_mean, diff_values.shape[0],val_to_mean):
                d = np.mean(diff_values[i:i+val_to_mean,])
                if np.abs(d - np.mean(diff_values[val_to_mean:val_to_mean+20])) > beta and np.abs(d - np.mean(diff_values[val_to_mean:val_to_mean+20])) < 1:
                    start_idx = i
                    break

            end_idx = diff_values.shape[0]
            for i in range(diff_values.shape[0] - val_to_mean - 1, start_idx - val_to_mean - 1, -val_to_mean):
                d = np.mean(diff_values[i-val_to_mean:i])
                if np.abs(d - np.mean(diff_values[-val_to_mean:])) > beta and np.abs(d - np.mean(diff_values[-val_to_mean:])) < 1:
                    end_idx = i
                    break

            WA_idx[id] = [start_idx, end_idx]

        #     mask_start = np.concatenate((np.array([False] * start_idx), np.array([True] * (diff_values.shape[0] - start_idx + 1))))
        #     mask_end = np.concatenate((np.array([True] * end_idx), np.array([False] * (diff_values.shape[0] - end_idx + 1))))
        #     mask = mask_start & mask_end
        # else:
        #     mask = np.array([True]*time_interp.shape[0])


        anchor_interp_data[id] = {
            'time': time_interp,
            'gps_latitude': gps_latitude_interp,
            'gps_longitude': gps_longitude_interp,
            'gps_altitude': gps_altitude_interp,
            'beacon_latitudes': beacon_latitudes_interp,
            'beacon_longitudes': beacon_longitudes_interp,
            'beacon_depths': beacon_depths_interp,
            'lbl_range': lbl_range_interp,
            'ins_x' : ins_x_interp,
            'ins_y' : ins_y_interp,
            'ins_z' : ins_altitude_interp,
            'beacon_x' : beacon_x_interp,
            'beacon_y' : beacon_y_interp,
            'RXPower_FPPower': RXPower_FPPower_interp,
            'RXPower': RXPower_interp,
            'FPPower': FPPower_interp,
            'Quality': Quality_interp,
            'Innov_o' : Innov_o,
            "d_meas_xpf" : d_meas_xpf_id,
            "heading" : heading_interp,
        }

        
        # current_time = time_interp[mask_interp]
        print(f"End of interpolation for anchor {id}")

        if T_glob.shape[0] == 0:
            print("\n /!\ No data for interpolation /!\ ")
            import sys
            sys.exit()
    if without_alignement:
        values = np.array(list(WA_idx.values()))
        start_idx = np.max(values[:, 0])
        end_idx = np.min(values[:, 1])

        
        for id in anchor_id:
            mask_start = np.concatenate((np.array([False] * start_idx), np.array([True] * (anchor_interp_data[id]["time"].shape[0] - start_idx))))
            mask_end = np.concatenate((np.array([True] * end_idx), np.array([False] * (anchor_interp_data[id]["time"].shape[0] - end_idx))))
            mask = mask_start & mask_end
            for key in anchor_interp_data[id].keys():
                anchor_interp_data[id][key] = anchor_interp_data[id][key][mask]

