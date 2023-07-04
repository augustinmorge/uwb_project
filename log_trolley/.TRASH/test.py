import os
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from xpf2py.xpf2py import xpf2py
from sklearn.metrics import r2_score

def plot_polynomial_regression(ax, x, y, degrees, label = ""):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn}\n(R² = {r_squared:.3f}) \n'+label, color = 'red')
    ax.legend(loc='upper left')

def percent(array, mask, name = ""):
    print(f"Use {array[mask].shape[0]/array.shape[0]*100}% of data for {name}")

# Créer un objet de projection cartésienne
cartesian_proj = pyproj.Proj(proj='cart', ellps='WGS84 ', datum='WGS84')

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

# test = '01_06_2023\\charieau2'
# file_name = f"{test}\\flo_PH-2248_R_PHINS_STANDARD.log"

# test = '06_06_2023\chariot_3roues'
# file_name = f"{test}\chariot_3roues_PH-2248_R_PHINS_STANDARD.log"

# test = '28_06_2023'
test = '03_07_2023'
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


whithout_jump = True
if whithout_jump:
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
file_path = f"{current_directory}\\..\\{test}\\{test}_for_analize.xpf"
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



time_innov_s = (utc_offset + date_s).squeeze()

def debug(args_s, args):
    for i in range(len(args)):
        print(args_s[i] + " : ", args[i])

interpolate = 1
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

        f_T_innov = interp1d(time_innov_s, time_innov_s)
        f_innov_o = interp1d(time_innov_s, innov_o[id])
        f_d_meas_xpf = interp1d(time_innov_s, d_meas_xpf[id])
        T_innov = f_T_innov(T_glob)
        Innov_o = f_innov_o(T_glob)
        d_meas_xpf_id = f_d_meas_xpf(T_glob)
        

        anchor_interp_data[id] = {
            'time': time_interp,
            'gps_latitude': gps_latitude_interp,
            'gps_longitude': gps_longitude_interp,
            'gps_altitude': gps_altitude_interp,
            'beacon_latitudes': beacon_latitudes_interp,
            'beacon_longitudes': beacon_longitudes_interp,
            'beacon_depths': beacon_depths_interp,
            'lbl_range': lbl_range_interp,
            'gps_x' : gps_x_interp,
            'gps_y' : gps_y_interp,
            'beacon_x' : beacon_x_interp,
            'beacon_y' : beacon_y_interp,
            'time_dbm': time_dbm_interp,
            'RXPower_FPPower': RXPower_FPPower_interp,
            'RXPower': RXPower_interp,
            'FPPower': FPPower_interp,
            'Quality': Quality_interp,
            'T_innov' : T_innov,
            'Innov_o' : Innov_o,
            "d_meas_xpf" : d_meas_xpf_id,
        }

        
        # current_time = time_interp[mask_interp]
        print(f"End of interpolation for anchor {id}")

        if T_glob.shape[0] == 0:
            print("\n /!\ No data for interpolation /!\ ")
            import sys
            debug(["start", "end", "dt", "id_data['time']", "t_innov"], 
                [start_time, end_time, dt, id_data['time'], T_innov])
            sys.exit()

b = anchor_interp_data[6016]
diff_values = np.diff(b['d_meas_xpf'])

# Créer un masque pour exclure les valeurs aberrantes
mask_outliers = np.concatenate((np.array([True]), np.abs(diff_values) < 5))

# Trouver l'indice à partir duquel la valeur dépasse 1 mètre au début
start_idx = 0
for i in range(20, diff_values.shape[0],20):
    d = np.mean(diff_values[i:i+20,])
    if np.abs(d - np.mean(diff_values[:20])) > 0.5:
        print(i)
        start_idx = i
        break

mask_start = np.concatenate((np.array([False] * start_idx), np.array([True] * (diff_values.shape[0] - start_idx + 1))))

# Trouver l'indice à partir duquel la valeur dépasse 1 mètre à la fin
end_idx = diff_values.shape[0]
for i in range(diff_values.shape[0] - 21, start_idx - 21, -20):
    d = np.mean(diff_values[i-20:i])
    print(i - 20, i, d, np.abs(d - np.mean(diff_values[-20:])), np.mean(diff_values[-20:]))
    if np.abs(d - np.mean(diff_values[-20:])) > 0.5:
        end_idx = i + 1
        print(end_idx)
        break

mask_end = np.concatenate((np.array([True] * (diff_values.shape[0] - end_idx + 1)), np.array([False] * end_idx)))
print(diff_values.shape[0] - end_idx + 1)
# Combiner les masques pour obtenir le masque final
print(mask_outliers.shape, mask_start.shape, mask_end.shape)
mask = mask_outliers & mask_start & mask_end

# Tracer les données avec le masque appliqué
plt.figure()
plt.scatter(b['time'][mask], b['d_meas_xpf'][mask], s=1)
plt.figure()
plt.scatter(b['time'][mask_outliers], b['d_meas_xpf'][mask_outliers], s=1)
plt.show()



import sys
sys.exit()

def display_interp():

    # figrf, axsrf = plt.subplots(2,2)
    # figrf.suptitle("RX - FP")
    # figq, axsq = plt.subplots(2,2)
    # figq.suptitle("Quality")
    figd, axsd = plt.subplots(2,2)
    figd.suptitle("Distance")
    figrf2, axsrf2 = plt.subplots(2,2)
    figrf2.suptitle("RX - FP Histogramme")
    figq2, axsq2 = plt.subplots(2,2)
    figq2.suptitle("Quality Histogramme")

    fig_d, axes_d = plt.subplots(2, 4, figsize=(10, 10))
    fig_err, axes_err = plt.subplots(2,2)
    date = header_lines[2].split("\t")[1]
    fig_err.suptitle(f"{date}")
    fig_d.suptitle(f"{date}")
    figd2, axsd2 = plt.subplots(2,2)
    figd2.suptitle("d_meas_xpf Histogramme")

    for id in anchor_id:

        # The beacon used
        b = anchor_interp_data[id]

        # Calculer la distance entre l'gps et le balise actuel
        d_lbl = np.sqrt((b['gps_x'] - b['beacon_x'])**2 +
                        (b['gps_y'] - b['beacon_y'])**2 +
                        (b['gps_altitude'] - b['beacon_depths'])**2)
        
        nid = id - 6016
        
        # axrf = axsrf[nid//2, nid%2]
        # axrf.set_title(f"Erreur en fonction de la distance {id}")
        # axrf.scatter(b['RXPower_FPPower'], b['Innov_o'], label = 'f(err)', s = 0.5, color = 'black')
        # axrf.set_ylabel("Innovation [m]")
        # axrf.set_xlabel("RX - FP")

        # axq = axsq[nid//2, nid%2]
        # axq.set_title(f"Erreur en fonction de la distance {id}")
        # axq.scatter(b['Quality'], b['Innov_o'], label = 'f(err)', s = 0.5, color = 'black')
        # axq.set_ylabel("Innovation [m]")
        # axq.set_xlabel("Quality")

        axd = axsd[nid//2, nid%2]
        axd.set_title(f"Distance {id}")
        axd.plot(b['time'], d_lbl, label = 'distance')
        axd.set_ylabel("distance [m]")
        axd.set_xlabel("time [s]")

        # Create arrays to store binned values and quantiles
        alpha_rxfp = 5
        alpha_q = 100
        bins_rx_fp = np.arange(np.floor(min(b['RXPower_FPPower'])), np.ceil(max(b['RXPower_FPPower'])), alpha_rxfp)
        bins_quality = np.arange(np.floor(min(b['Quality'])), np.ceil(max(b['Quality'])), alpha_q)

        axrf2 = axsrf2[nid//2, nid%2]

        quantiles_rx_fp = []

        # Calculate the quantiles for each bin of RX - FP
        for i in range(len(bins_rx_fp) - 1):
            mask = np.logical_and(b['RXPower_FPPower'] >= bins_rx_fp[i], b['RXPower_FPPower'] < bins_rx_fp[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_rx_fp.append(quantiles)

        positions_rxfp = bins_rx_fp[:-1] + alpha_rxfp/2
        bp_rx_fp = axrf2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_rx_fp if len(q) > 0],
                                positions=positions_rxfp[:len(quantiles_rx_fp)],
                                widths=alpha_rxfp*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_rx_fp['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_rx_fp['medians']:
            median.set(color='red')

        axrf2.set_ylabel("Erreur")
        axrf2.set_xlabel("RX - FP")
        axrf2.set_title(f"{hex(int(id))}")

        axq2 = axsq2[nid//2, nid%2]

        quantiles_quality = []

        # Calculate the quantiles for each bin of Quality
        for i in range(len(bins_quality) - 1):
            mask = np.logical_and(b['Quality'] >= bins_quality[i], b['Quality'] < bins_quality[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_quality.append(quantiles)

        # Create the boxplot for Quality
        positions_q = bins_quality[:-1] + alpha_q/2
        bp_quality = axq2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_quality if len(q) > 0],
                                positions=positions_q[:len(quantiles_quality)],
                                widths=alpha_q*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_quality['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_quality['medians']:
            median.set(color='red')

        axq2.set_ylabel("Erreur")
        axq2.set_xlabel("Quality")
        axq2.set_title(f"{hex(int(id))}")


        ### Display the error with the distance ###
        
        ax_err = axes_err[nid//2, nid%2]
        fig_err.suptitle("Innovation en fonction de la distance")
        ax_err.set_title(f'Beacon ID {hex(int(id))}')
        ax_err.scatter(b['d_meas_xpf'], b['Innov_o'], label = 'Innov(d)', s = 1)
        ax_err.set_ylabel("Innovation [m]")
        ax_err.set_xlabel("distance [m]")
        ax_err.set_xlim([-2,175])
        ax_err.set_ylim([-5,5])
        # ax_err.set_ylim([-1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o']),1/2*np.std(b['Innov_o']) + np.mean(b['Innov_o'])])
        # plot_polynomial_regression(ax_err, b['d_meas_xpf'], b['Innov_o'], [1])
        alpha_d = 20
        # bins_d = np.arange(np.floor(min(b['d_meas_xpf'])), np.ceil(max(b['d_meas_xpf'])), alpha_d)
        bins_d = np.arange(0, 200, alpha_d)
        axd2 = axsd2[nid//2, nid%2]

        quantiles_d = []

        # Calculate the quantiles for each bin of d_meas_xpf
        for i in range(len(bins_d) - 1):
            mask = np.logical_and(b['d_meas_xpf'] >= bins_d[i], b['d_meas_xpf'] < bins_d[i+1])
            innov_ = b['Innov_o'][mask]
            if len(innov_) > 0:
                quantiles = np.percentile(innov_, [15, 33, 50, 66, 85])
                quantiles_d.append(quantiles)

        positions_d = bins_d[:-1] + alpha_d/2
        bp_d = axd2.boxplot([[q[0], q[1], q[2], q[3], q[4]] for q in quantiles_d if len(q) > 0],
                                positions=positions_d[:len(quantiles_d)],
                                widths=alpha_d*0.7,
                                showfliers=False,
                                patch_artist=True)

        for box in bp_d['boxes']:
            box.set(facecolor='lightyellow')

        for median in bp_d['medians']:
            median.set(color='red')

        axd2.set_ylabel("Erreur")
        axd2.set_xlabel("d_meas_xpf")
        axd2.set_title(f"{hex(int(id))}")








        ax_d = axes_d[0,id - 6016]
        ax2_d = axes_d[1,id - 6016]

        # Tracer les estimations de distance pour le balise actuel
        ax_d.set_title(f'Beacon ID {hex(int(id))}')
        ax_d.scatter(b['time'], b['d_meas_xpf'] - b["Innov_o"], label='d(GPS - anchor)', marker='x', color='blue', s=1)
        ax_d.scatter(b['time'], b['d_meas_xpf'], label='LBL - Range (m)', marker='x', color='orange', s=1)

        mask = (np.abs(b["Innov_o"] - np.mean(b["Innov_o"])) < 3*np.std(b["Innov_o"]))
        ax2_d.scatter(b['time'][mask], b["Innov_o"][mask], label='Innovation (m)', marker='x', color='black', s=1)
        ax2_d.plot(b['time'][mask], np.mean(b["Innov_o"][mask])*np.ones(b['time'][mask].shape[0]), label=f'mean = {int(np.mean(b["Innov_o"][mask])*100)/100}', color='red')
        ax2_d.set_ylim([-5,5])
        ax2_d.set_xlabel("Time [s]")

        # Configurer les propriétés du sous-graphique
        ax_d.set_ylabel('Distance (m)')
        ax_d.legend()

        ax2_d.set_ylabel('Distance (m)')
        ax2_d.legend()

        # Définir les marques sur l'axe des abscisses uniquement pour le dernier axe
        N = b['d_meas_xpf'].shape[0]
        print(f"For beacon {hex(int(id))} the mean error is {np.mean(b['Innov_o'][:N,])}; the sd of {np.std(b['Innov_o'][:N,])}")

        plt.figure()
        plt.plot(b['time'], b['d_meas_xpf'], label = id)
        plt.legend()

display_interp()


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
# gps_x -= -0.698
# gps_y -= 0.2
# gps_altitude -= 1.170

# beacon_x -= -1.444
# beacon_y -= -0.173
# beacon_depths -= 0.672

# plt.figure()
# plt.plot(time[100:], gps_altitude[100:])
# plt.show()

# Créer les sous-graphiques pour chaque balise
unique_beacon_ids = np.unique(beacon_ids)
num_subplots = len(unique_beacon_ids)

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