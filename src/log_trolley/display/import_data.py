import os
import numpy as np
# import pyproj
from xpf2py.xpf2py import xpf2py
from scipy.interpolate import interp1d
import copy, sys
import bisect
    
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

# TEST = ['28_06_2023'] 
# TEST = ['03_07_2023']
# TEST = ['05_07_2023']
# TEST = ['11_07_2023']
# TEST = ['17_07_2023_2']
# TEST = ['17_07_2023']
TEST = ['26_07_2023']
# TEST = ['28_06_2023', '03_07_2023', '05_07_2023', '11_07_2023', '17_07_2023_2', "26_07_2023"]


for test in TEST:
    for switch in [0,1]:
        print(test)
        # if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (5 + 7*365/12):
        #     print("For RX - FP we use DW1000Ranging.getDistantDevice()->getRXPower() - DW1000.getFirstPathPower()")
        # else:
        #     print("For RX - FP we use DW1000.getReceivePower() - DW1000.getFirstPathPower()")

        print(f"We interpolate data : {interpolate==1}")
        print(f"We compute with alignement : {without_alignement==0}")

        sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))

        # Chemin absolu du fichier
        current_directory = os.path.dirname(__file__)
        if switch:
            name_saved = f"{test}_anchor_interp_data.pkl"
            file_xpf = f"{current_directory}\\..\\{test}\\{test}_for_analize.xpf"
            # xpf_content,py_fileOutPath = xpf2py(file_xpf, CheckExistence = False)            
            xpf_content,py_fileOutPath = xpf2py(file_xpf)
        else:
            name_saved = f"{test}_anchor_interp_data_std_10cm.pkl"
            file_xpf = f"{current_directory}\\..\\{test}\\{test}_for_analize_std_10cm.xpf"
            # xpf_content,py_fileOutPath = xpf2py(file_xpf, CheckExistence = False)         
            xpf_content,py_fileOutPath = xpf2py(file_xpf)

        file_anchor = f"{current_directory}\\..\\{test}\\anchor_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"
        # xpf_anchor,py_fileOutPath_anchor = xpf2py(file_anchor, CheckExistence = False)        
        xpf_anchor,py_fileOutPath_anchor = xpf2py(file_anchor)

        file_dbm = f"{current_directory}\\..\\{test}\\dbm_{test}_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"
        # xpf_dbm,py_fileOutPath_dbm = xpf2py(file_dbm, CheckExistence = False)        
        xpf_dbm,py_fileOutPath_dbm = xpf2py(file_dbm)

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

        RXPower = RXPower.astype(int) + (RXPower - RXPower.astype(int))*60
        FPPower = FPPower.astype(int) + (FPPower - FPPower.astype(int))*60
        mask_rx = np.where(RXPower < 45)
        RXPower[mask_rx] = RXPower[mask_rx] + 90

        if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (5 + 7*365/12):
            print(" /!\ Change RX-FP /!\ ")
            corrFac = 2.3334
            for i in range(RXPower.shape[0]):
                if -RXPower[i] > -88:
                    RXPower[i] = (-RXPower[i] - 88*corrFac)/(1 + corrFac)
                else:
                    RXPower[i] = -RXPower[i]
            for i in range(FPPower.shape[0]):
                if -FPPower[i] > -88:
                    FPPower[i] = (-FPPower[i] - 88*corrFac)/(1 + corrFac)
                else:
                    FPPower[i] = -FPPower[i]
            RXPower_FPPower = np.abs(RXPower - FPPower)

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
                'none' : none_dbm(i),
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

        time_ins_anchor = {6016 : (xpf_content["data"]['RANGE_KAL_MEAS']["lbl3Time"].astype(float) + utc_offset).squeeze(), \
                    6017 : (xpf_content["data"]['RANGE_KAL_MEAS']["lbl4Time"].astype(float) + utc_offset).squeeze(), \
                    6018 : (xpf_content["data"]['RANGE_KAL_MEAS']["lbl1Time"].astype(float) + utc_offset).squeeze(), \
                    6019 : (xpf_content["data"]['RANGE_KAL_MEAS']["lbl2Time"].astype(float) + utc_offset).squeeze()}

        heading = xpf_content["data"]["primary_nav"]["heading"].squeeze()*np.pi/180
        if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (3 + 7*365/12): 
            heading += np.pi

        ins_latitude = (xpf_content["data"]["primary_nav"]["latitude"]).astype(float).squeeze()
        ins_longitude = (xpf_content["data"]["primary_nav"]["longitude"]).astype(float).squeeze()
        ins_altitude = (xpf_content["data"]["primary_nav"]["orthometricHeight"]).astype(float).squeeze()
        ins_x, ins_y = coord2cart((ins_latitude, ins_longitude))


        time_ins_s = (date_ins_s + utc_offset).squeeze()
        time_innov_s = (date_innov_s + utc_offset).squeeze()

        # print(date_innov_s.shape)
        # print(date_innov_s[0])
        # print(date_innov_s[-1])
        # print(date_ins_s.shape)
        # print(date_ins_s[0])
        # print(date_ins_s[-1])
        # import matplotlib.pyplot as plt
        # plt.plot(time_innov_s)
        # plt.plot(time_ins_s)
        # plt.show()

        #Bizarre, demander à Thomas pourquoi je suis obligé de faire ça..
        if time_innov_s.shape[0] > time_ins_s.shape[0]:
            print("Pas la même taille de données entre primary_nav et RANGE_KAL_MEAS")
            time_innov_s = time_innov_s[:-1]
            for key in innov_o.keys():
                innov_o[key] = innov_o[key][:-1]
                d_meas_xpf[key] = d_meas_xpf[key][:-1]
                time_ins_anchor[key] = time_ins_anchor[key][:-1]

        speedEast = xpf_content["data"]["primary_nav"]["speedEast"].astype(float).squeeze()
        speedNorth = xpf_content["data"]["primary_nav"]["speedNorth"].astype(float).squeeze()
        speedVertical = xpf_content["data"]["primary_nav"]["speedVertical"].astype(float).squeeze()

        def debug(args_s, args):
            for i in range(len(args)):
                print(args_s[i] + " : ", args[i])

        if __name__ == "__main__":
            print(f"Size of RANGE_KAL_MEAS : {time_ins_s.shape}")
            print(f"Size of primary_nav : {ins_latitude.shape}")
            print(f"Size of Range Meter : {time_s.shape}")
            print(f"Size of Dbm : {time_dbm_s.shape}")

            # import matplotlib.pyplot as plt
            # Initialisation du dictionnaire num_lbl pour stocker les correspondances
            num_lbl = {}
            # Parcourir tous les numéros dans beacon_data
            for num in beacon_data.keys():
                min_corr = 0
                min_num_xpf = None

                for num_xpf in beacon_data.keys():

                    start_time = max(beacon_data[num]['time'][0],time_innov_s[0])
                    end_time = min(beacon_data[num]['time'][-1],time_innov_s[-1])
                    T_glob = np.arange(start_time, end_time, 1)

                    f_d_meas_xpf = interp1d(time_innov_s, d_meas_xpf[num_xpf])
                    d_meas_xpf_id = f_d_meas_xpf(T_glob)

                    f_lbl_range = interp1d(beacon_data[num]['time'], beacon_data[num]['lbl_range'])
                    lbl_range_interp = f_lbl_range(T_glob)


                    # Calculer la corrélation entre les deux tableaux interpolés
                    correlation_matrix = np.corrcoef(d_meas_xpf_id, lbl_range_interp)
                    # Extraire la valeur de corrélation entre les deux tableaux (en supposant que c'est la valeur en haut à droite de la matrice)
                    corr = correlation_matrix[0, 1]

                    # Trouver la valeur de corrélation minimale
                    if np.abs(corr) > min_corr:
                        min_corr = np.abs(corr)
                        min_num_xpf = num_xpf

                # Enregistrer la correspondance trouvée dans le dictionnaire num_lbl
                num_lbl[num] = min_num_xpf

            # Vérifier s'il y a des doublons dans num_lbl
            seen_values = set()
            for num_xpf in num_lbl.values():
                if num_xpf in seen_values:
                    print("Erreur : Deux fois le même item trouvé dans num_lbl.")
                    sys.exit(1)
                seen_values.add(num_xpf)

            # Maintenant, num_lbl contient les correspondances entre les numéros de courbe et leurs étiquettes respectives.
            new_d_meas_xpf = copy.deepcopy(d_meas_xpf)
            new_innov_o = copy.deepcopy(innov_o)
            new_time_ins_anchor = copy.deepcopy(time_ins_anchor)

            corres = {6016 : 'lbl3', 6017 : 'lbl4', 6018 : 'lbl1', 6019 : 'lbl2'}
            for num in num_lbl.keys():
                print(f"{num} correspond to {corres[num_lbl[num]]}")
                new_d_meas_xpf[num] = d_meas_xpf[num_lbl[num]]
                new_innov_o[num] = innov_o[num_lbl[num]]

                new_time_ins_anchor[num] = time_ins_anchor[num_lbl[num]]

            #########################
            anchor_interp_data = {}


            for id in anchor_id:
                corresponding_idx = []
                time_beacon = beacon_data[id]['time']
                time_dbm = dbm_data[id - 6000]['time']
                time_ins = (new_time_ins_anchor[id])
                tolerance = 0.5

                corresponding_idx = []
                
                # for (i,t_dbm) in enumerate(time_dbm):
                #     idx_corr = bisect.bisect(time_beacon, t_dbm)
                #     if idx_corr == time_beacon.shape[0] : idx_corr -= 1
                #     if np.abs(time_beacon[idx_corr] - t_dbm) < tolerance:
                #         # with the INS
                #         idx_corr_ins = bisect.bisect(time_ins, t_dbm)
                #         if idx_corr_ins == time_ins.shape[0] : idx_corr_ins -= 1
                #         if np.abs(time_ins[idx_corr_ins] - t_dbm) < 0.5:
                #             corresponding_idx.append((idx_corr, i, idx_corr_ins))

                for (i,t_ins) in enumerate(time_ins):
                    idx_corr = bisect.bisect(time_beacon, t_ins)
                    if idx_corr == time_beacon.shape[0] : idx_corr -= 1
                    if np.abs(time_beacon[idx_corr] - t_ins) < tolerance:
                        # with the INS
                        idx_corr_dbm = bisect.bisect(time_dbm, t_ins)
                        if idx_corr_dbm == time_dbm.shape[0] : idx_corr_dbm -= 1
                        if np.abs(time_dbm[idx_corr_dbm] - t_ins) < tolerance:
                            corresponding_idx.append((idx_corr, idx_corr_dbm, i))

                corresponding_idx = np.array(corresponding_idx)


                mask_beacon = corresponding_idx[:,0]
                mask_dbm = corresponding_idx[:,1]
                mask_ins = corresponding_idx[:,2]

                print(f"Using time correlation, we loose : {(1-(ins_x)[mask_ins].shape[0]/(ins_x).shape[0])*100}% for INS")
                print(f"Using time correlation, we loose : {(1-beacon_data[id]['lbl_range'][mask_beacon].shape[0]/beacon_data[id]['lbl_range'].shape[0])*100}% for BEA")
                print(f"Using time correlation, we loose : {(1-dbm_data[id - 6000]['RXPower'][mask_dbm].shape[0]/dbm_data[id - 6000]['RXPower'].shape[0])*100}% for DBM")
                
                ### Conversion en cartésien
                beacon_x, beacon_y = coord2cart(((beacon_data[id]['beacon_latitudes']),beacon_data[id]['beacon_longitudes']))   #cartesian_proj(beacon_longitudes_interp, beacon_latitudes_interp)
            
                ## DELETE ALIGNEMENT
                val_to_mean = 20
                beta = 0.1
                diff_dep = np.sqrt(np.diff((ins_x)[mask_ins])**2 + np.diff((ins_y)[mask_ins])**2 + np.diff((ins_altitude)[mask_ins])**2)
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
                    mask_start = np.concatenate((np.array([False] * start_idx_ali), np.array([True] * ((diff_dep.shape[0]+1) - start_idx_ali))))
                    mask_end = np.concatenate((np.array([True] * end_idx_ali), np.array([False] * ((diff_dep.shape[0]+1) - end_idx_ali))))
                    mask_ali = mask_start & mask_end

                else:
                    mask_ali = np.array([True]*(diff_dep.shape[0]+1))

                
                anchor_interp_data[id] = {
                    'time': (new_time_ins_anchor[id])[mask_ins][mask_ali],
                    'beacon_latitudes': beacon_data[id]['beacon_latitudes'][mask_beacon][mask_ali],
                    'beacon_longitudes': beacon_data[id]['beacon_longitudes'][mask_beacon][mask_ali],
                    'beacon_depths': beacon_data[id]['beacon_depths'][mask_beacon][mask_ali],
                    'lbl_range': beacon_data[id]['lbl_range'][mask_beacon][mask_ali],
                    'ins_x' : (ins_x)[mask_ins][mask_ali],
                    'ins_y' : (ins_y)[mask_ins][mask_ali],
                    'ins_z' : (ins_altitude)[mask_ins][mask_ali],
                    'beacon_x' : beacon_x[mask_beacon][mask_ali],
                    'beacon_y' : beacon_y[mask_beacon][mask_ali],
                    'RXPower_FPPower': dbm_data[id - 6000]['RXPower_FPPower'][mask_dbm][mask_ali],
                    'RXPower': dbm_data[id - 6000]['RXPower'][mask_dbm][mask_ali],
                    'FPPower': dbm_data[id - 6000]['FPPower'][mask_dbm][mask_ali],
                    'Quality': dbm_data[id - 6000]['Quality'][mask_dbm][mask_ali],
                    'Innov_o' : (new_innov_o[id])[mask_ins][mask_ali],
                    "d_meas_xpf" : (new_d_meas_xpf[id])[mask_ins][mask_ali],
                    "heading" : (heading)[mask_ins][mask_ali],
                    "speedEast" : (speedEast)[mask_ins][mask_ali],
                    "speedNorth" : (speedNorth)[mask_ins][mask_ali],
                    "speedVertical" : (speedVertical)[mask_ins][mask_ali],
                    "FullCompensatedRotRateGeoX" : xpf_content["data"]["ACCEL_ROT"]["FullCompensatedRotRateGeoX"][mask_ins][mask_ali].squeeze(),
                    "FullCompensatedRotRateGeoY" : xpf_content["data"]["ACCEL_ROT"]["FullCompensatedRotRateGeoY"][mask_ins][mask_ali].squeeze(),
                    "FullCompensatedRotRateGeoZ" : xpf_content["data"]["ACCEL_ROT"]["FullCompensatedRotRateGeoZ"][mask_ins][mask_ali].squeeze(),

                    # 'time_intertial': (new_time_ins_anchor[id])[~mask],
                    # 'ins_x_intertial' : (ins_x)[~mask],
                    # 'ins_y_intertial' : (ins_y)[~mask],
                    # 'ins_z_intertial' : (ins_altitude)[~mask],

                    'start_idx_ali' : start_idx_ali,
                    'end_idx_ali' : end_idx_ali,

                }
                print(f"End of interpolation for anchor {id}\n~~~~~~~~~~~~")

                if anchor_interp_data[id]['time'].shape[0] == 0:
                    print("\n /!\ No data for interpolation /!\ ")
                    import sys
                    sys.exit()
                
                # if id==6017:
                #     import matplotlib.pyplot as plt
                #     plt.figure()
                #     plt.plot(time_innov_s, innov_o[6017],label='before')
                #     plt.plot(anchor_interp_data[6017]['time'], anchor_interp_data[6017]['Innov_o'],label='after')
                #     plt.ylim([-1,1])
                #     plt.legend()
                #     plt.show()
                #     import sys
                #     sys.exit()

            import os
            import pickle

            # Nom du fichier de sauvegarde
            filename = f"\\..\\{test}\\{name_saved}"

            # Chemin complet vers le fichier de sauvegarde en joignant le chemin absolu du répertoire de travail avec le nom du fichier
            filepath = current_directory + filename

            # Sauvegarder le dictionnaire dans le fichier
            with open(filepath, 'wb') as file:
                pickle.dump(anchor_interp_data, file)

            print("Le dictionnaire a été sauvegardé avec succès dans le fichier :", filepath)

            # import matplotlib.pyplot as plt
            # plt.figure()
            # plt.plot(anchor_interp_data[id]['RXPower'])
            # # plt.plot(anchor_interp_data[id]['FPPower'])
            # plt.show()
