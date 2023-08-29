import os
import numpy as np
# import pyproj
from xpf2py.xpf2py import xpf2py

wpt_parking = (48.900140, 2.063867)
def coord2cart(coords,coords_ref=wpt_parking):
    R = 6372800
    ly,lx = coords
    lym,lxm = coords_ref
    x_tilde = R * np.cos(ly*np.pi/180)*(lx-lxm)*np.pi/180
    y_tilde = R * (ly-lym)*np.pi/180
    return np.array([x_tilde,y_tilde])

interpolate = 1
without_alignement = 0
whitout_jump = 0

# test = '03_07_2023'
# test = '05_07_2023'
test = '11_07_2023'
# test = '17_07_2023'
# test = '17_07_2023_2'

if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (5 + 7*365/12):
    print("For RX - FP we use DW1000Ranging.getDistantDevice()->getRXPower() - DW1000.getFirstPathPower()")
else:
    print("For RX - FP we use DW1000.getReceivePower() - DW1000.getFirstPathPower()")

print(f"We interpolate data : {interpolate==1}")
print(f"We compute with alignement : {without_alignement==0}")

sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

file_xpf = f"{current_directory}\\..\\{test}\\{test}_for_analize.xpf"
xpf_content,py_fileOutPath = xpf2py(file_xpf, CheckExistence = True )

file_anchor = f"{current_directory}\\..\\{test}\\anchor_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"
xpf_anchor,py_fileOutPath_anchor = xpf2py(file_anchor, CheckExistence = True)

file_dbm = f"{current_directory}\\..\\{test}\\dbm_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"
xpf_dbm,py_fileOutPath_dbm = xpf2py(file_dbm, CheckExistence = True)

######################### RECUPERATION DES DONNES UTILES #########################
anchor_id = np.arange(6016, 6020)

# Extraire les colonnes correspondantes aux variables d'intérêt et les convertir en float64
utc_offset_anchor = (xpf_anchor["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_anchor["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_anchor["data"]["UTC"]["utcSecond"].astype(float)
time_s = (xpf_anchor['data']['LBL']['date'].astype(float)*10**(-7) + utc_offset_anchor).squeeze()
beacon_ids = xpf_anchor['data']['LBL']['beaconId'].astype(float).squeeze()
beacon_latitudes = xpf_anchor['data']['LBL']['latitude'].astype(float).squeeze()
beacon_longitudes = xpf_anchor['data']['LBL']['longitude'].astype(float).squeeze()
beacon_depths = xpf_anchor['data']['LBL']['depth'].astype(float).squeeze()
lbl_range = xpf_anchor['data']['LBL']['range'].astype(float).squeeze()

def none(id):
    idx = np.where(np.diff(time_s[beacon_ids == id].astype(float)) > 5.4)[0]
    T = []
    for i in idx:
        T.append([time_s[beacon_ids == id][i], time_s[beacon_ids == id][i+1]])
    return(T)

beacon_data = {}
for i in anchor_id:
    beacon_data[i] = {
        'time': time_s[beacon_ids == i],
        'beacon_latitudes': beacon_latitudes[beacon_ids == i],
        'beacon_longitudes': beacon_longitudes[beacon_ids == i],
        'beacon_depths': beacon_depths[beacon_ids == i],
        'lbl_range': lbl_range[beacon_ids == i],
        'none' : none(i),
    }

### EXTRACTION DES FACTEURS DE QUALITE ###
dbm_id = np.arange(16, 20)
utc_offset_dbm = (xpf_dbm["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_dbm["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_dbm["data"]["UTC"]["utcSecond"].astype(float)
time_dbm_s = (xpf_dbm['data']['LBL']['date'].astype(float)*10**(-7) + utc_offset_dbm).squeeze()
RXPower_FPPower = xpf_dbm['data']['LBL']['range'].astype(float).squeeze()
beacon_ids_dbm = xpf_dbm['data']['LBL']['beaconId'].astype(float).squeeze()
RXPower = xpf_dbm['data']['LBL']['latitude'].astype(float).squeeze()
FPPower = xpf_dbm['data']['LBL']['longitude'].astype(float).squeeze()
Quality = xpf_dbm['data']['LBL']['depth'].astype(float).squeeze()

RXPower = np.floor(RXPower) + (RXPower - np.floor(RXPower))*60
FPPower = np.floor(FPPower) + (FPPower - np.floor(FPPower))*60

# ## Transformation 
# corrFac = 2.3334
# for i in range(RXPower.shape[0]):
#     if RXPower[i] > -88:
#         RXPower[i] = RXPower[i]/(1+corrFac) - 88*corrFac
# for i in range(RXPower.shape[0]):
#     if FPPower[i] > -88:
#         FPPower[i] = FPPower[i]/(1+corrFac) - 88*corrFac

# if whitout_jump:
#     window_size = 50
#     idx_start = np.where(time_s > (time_s[0] + 15*60))[0][0] #Les minutes d'alignement
#     try:
#         idx_jump = np.where(np.diff(time_s) > 60)[0][0]
#     except:
#         idx_jump = -1
#     time_s = time_s[idx_start:idx_jump,]
#     beacon_ids = beacon_ids[idx_start:idx_jump,]
#     beacon_latitudes = beacon_latitudes[idx_start:idx_jump,]
#     beacon_longitudes = beacon_longitudes[idx_start:idx_jump,]
#     beacon_depths = beacon_depths[idx_start:idx_jump,]
#     lbl_range = lbl_range[idx_start:idx_jump,]

#     time_dbm_s = time_dbm_s[idx_start:idx_jump,]
#     RXPower_FPPower = RXPower_FPPower[idx_start:idx_jump,]
#     beacon_ids_dbm = beacon_ids_dbm[idx_start:idx_jump,]
#     RXPower = RXPower[idx_start:idx_jump,]
#     FPPower = FPPower[idx_start:idx_jump,]
#     Quality = Quality[idx_start:idx_jump,]

dbm_data = {}

def none_dbm(id):
    idx = np.where(np.diff(time_dbm_s[beacon_ids_dbm == id].astype(float)) > 5.4)[0]
    T = []
    for i in idx:
        T.append([time_dbm_s[beacon_ids_dbm == id][i], time_dbm_s[beacon_ids_dbm == id][i+1]])
    return(T)

for i in dbm_id:
    dbm_data[i] = {
        'time': time_dbm_s[beacon_ids_dbm == i],
        'RXPower_FPPower': RXPower_FPPower[beacon_ids_dbm == i],
        'RXPower': RXPower[beacon_ids_dbm == i],
        'FPPower': FPPower[beacon_ids_dbm == i],
        'Quality': Quality[beacon_ids_dbm == i],
        'none_dbm' : none_dbm(i),
    }

### EXTRACTION DE L'INNOVATION ###
date_innov_s = xpf_content["data"]['RANGE_KAL_MEAS']["date"].astype(float)*10**(-7)
date_ins_s = xpf_content["data"]["primary_nav"]["date"].astype(float)*10**(-7)
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

ins_latitude = (xpf_content["data"]["primary_nav"]["latitude"]).astype(float).squeeze()
ins_longitude = (xpf_content["data"]["primary_nav"]["longitude"]).astype(float).squeeze()
ins_altitude = (xpf_content["data"]["primary_nav"]["orthometricHeight"]).astype(float).squeeze()

time_ins_s = (date_ins_s + utc_offset).squeeze()
time_innov_s = (date_innov_s + utc_offset).squeeze()

speedEast = xpf_content["data"]["primary_nav"]["speedEast"].astype(float).squeeze()
speedNorth = xpf_content["data"]["primary_nav"]["speedNorth"].astype(float).squeeze()
speedVertical = xpf_content["data"]["primary_nav"]["speedVertical"].astype(float).squeeze()

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
    print("~~~~~~~~~~~~")
    for id in anchor_id:

        id_data = beacon_data[id]
        id_data_dbm = dbm_data[id-6000]

        try :
            start_time = max(id_data['time'][0], id_data_dbm['time'][0],time_innov_s[0],time_ins_s[0])
        except:
            print("No dBm data")
            break
        end_time = min(id_data['time'][-1], id_data_dbm['time'][-1],time_innov_s[-1],time_ins_s[-1])
        dt = min(min(np.mean(np.diff(id_data['time'])),np.mean(np.diff(id_data_dbm['time']))),np.mean(np.diff(time_innov_s)))
        
        # debug(["id_data['time'][0]", "id_data_dbm['time'][0]","time_innov_s[0]","time_ins_s[0]"],[id_data['time'][0], id_data_dbm['time'][0],time_innov_s[0],time_ins_s[0]])
        # debug(["id_data['time'][-1]", "id_data_dbm['time'][-1]",'time_innov_s[-1]','time_ins_s[-1]'],[id_data['time'][-1], id_data_dbm['time'][-1],time_innov_s[-1],time_ins_s[-1]])
        # debug(["start_time", "end_time", "dt"],[start_time, end_time, dt])
        T_glob = np.arange(start_time, end_time, dt)

        f_beacon_latitudes = interp1d(id_data['time'], id_data['beacon_latitudes'])
        f_beacon_longitudes = interp1d(id_data['time'], id_data['beacon_longitudes'])
        f_beacon_depths = interp1d(id_data['time'], id_data['beacon_depths'])
        f_lbl_range = interp1d(id_data['time'], id_data['lbl_range'])
        beacon_latitudes_interp = f_beacon_latitudes(T_glob)
        beacon_longitudes_interp = f_beacon_longitudes(T_glob)
        beacon_depths_interp = f_beacon_depths(T_glob)
        lbl_range_interp = f_lbl_range(T_glob)

        # Convertir les coordonnées des balises en coordonnées cartésiennes
        beacon_x_interp, beacon_y_interp = coord2cart((beacon_latitudes_interp,beacon_longitudes_interp))   #cartesian_proj(beacon_longitudes_interp, beacon_latitudes_interp)
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
        f_speedEast = interp1d(time_ins_s,speedEast)
        f_speedNorth = interp1d(time_ins_s,speedNorth)
        f_speedVertical = interp1d(time_ins_s,speedVertical)
        heading_interp = f_heading(T_glob)
        ins_longitude_interp = f_ins_longitude(T_glob)
        ins_latitude_interp = f_ins_latitude(T_glob)
        ins_altitude_interp = f_ins_altitude(T_glob)
        speedEast_interp = f_speedEast(T_glob)
        speedNorth_interp = f_speedNorth(T_glob)
        speedVertical_interp = f_speedVertical(T_glob)


        ins_x_interp, ins_y_interp = coord2cart((ins_latitude_interp, ins_longitude_interp)) #cartesian_proj(ins_longitude_interp, ins_latitude_interp)

        mask_nodata = np.zeros_like(T_glob, dtype=bool)

        for interval in np.array(id_data['none']):
            mask_interval = np.logical_and(T_glob >= interval[0], T_glob <= interval[1])
            mask_nodata = np.logical_or(mask_nodata, mask_interval)

        for interval in np.array(id_data_dbm['none_dbm']):
            mask_interval = np.logical_and(T_glob >= interval[0], T_glob <= interval[1])
            mask_nodata = np.logical_or(mask_nodata, mask_interval)

        ## DELETE ALIGNEMENT
        val_to_mean = 20
        beta = 0.1
        diff_dep = np.sqrt(np.diff(ins_x_interp[~mask_nodata])**2 + np.diff(ins_y_interp[~mask_nodata])**2 + np.diff(ins_altitude_interp[~mask_nodata])**2)
        start_idx_ali = 0
        end_idx_ali = diff_dep.shape[0]

        
        for i in range(20 + val_to_mean, diff_dep.shape[0],val_to_mean):
            if np.mean(diff_dep[i:i+val_to_mean,]) > beta:
                start_idx_ali = i
                break
        
        for i in range(diff_dep.shape[0] - val_to_mean - 1, start_idx_ali - val_to_mean - 1, -val_to_mean):
            if np.mean(diff_dep[i-val_to_mean:i]) > beta:
                end_idx_ali = i
                break

        if without_alignement:
            mask_start = np.concatenate((np.array([False] * start_idx_ali), np.array([True] * (T_glob[~mask_nodata].shape[0] - start_idx_ali))))
            mask_end = np.concatenate((np.array([True] * end_idx_ali), np.array([False] * (T_glob[~mask_nodata].shape[0] - end_idx_ali))))
            mask_ali = mask_start & mask_end

        else:
            mask_ali = np.array([True]*T_glob[~mask_nodata].shape[0])
        
        # print(f"Remove {(1 - T_glob[~mask_nodata].shape[0]/T_glob.shape[0])*100}% of data with mask of no data")
        # print(f"Remove {(1 - T_glob[~mask_nodata][mask_ali].shape[0]/T_glob[~mask_nodata].shape[0])*100}% of data without alignement from no data")
        anchor_interp_data[id] = {
            'time': T_glob[~mask_nodata][mask_ali],
            'beacon_latitudes': beacon_latitudes_interp[~mask_nodata][mask_ali],
            'beacon_longitudes': beacon_longitudes_interp[~mask_nodata][mask_ali],
            'beacon_depths': beacon_depths_interp[~mask_nodata][mask_ali],
            'lbl_range': lbl_range_interp[~mask_nodata][mask_ali],
            'ins_x' : ins_x_interp[~mask_nodata][mask_ali],
            'ins_y' : ins_y_interp[~mask_nodata][mask_ali],
            'ins_z' : ins_altitude_interp[~mask_nodata][mask_ali],
            'beacon_x' : beacon_x_interp[~mask_nodata][mask_ali],
            'beacon_y' : beacon_y_interp[~mask_nodata][mask_ali],
            'RXPower_FPPower': RXPower_FPPower_interp[~mask_nodata][mask_ali],
            'RXPower': RXPower_interp[~mask_nodata][mask_ali],
            'FPPower': FPPower_interp[~mask_nodata][mask_ali],
            'Quality': Quality_interp[~mask_nodata][mask_ali],
            'Innov_o' : Innov_o[~mask_nodata][mask_ali],
            "d_meas_xpf" : d_meas_xpf_id[~mask_nodata][mask_ali],
            "heading" : heading_interp[~mask_nodata][mask_ali],
            "speedEast" : speedEast_interp[~mask_nodata][mask_ali],
            "speedNorth" : speedNorth_interp[~mask_nodata][mask_ali],
            "speedVertical" : speedVertical_interp[~mask_nodata][mask_ali],
        }

        # current_time = time_interp[mask_interp]
        print(f"End of interpolation for anchor {id}\n~~~~~~~~~~~~")

        if T_glob.shape[0] == 0:
            print("\n /!\ No data for interpolation /!\ ")
            import sys
            sys.exit()
