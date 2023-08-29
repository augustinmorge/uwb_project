import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import os
from xpf2py.xpf2py import xpf2py
import pickle
from import_data import *

# Charger le dictionnaire à partir du fichier
current_directory = os.path.dirname(__file__)
filename = f"\\..\\{test}\\{test}_anchor_interp_data.pkl"
filepath = current_directory + filename
with open(filepath, 'rb') as file:
    anchor_interp_data = pickle.load(file)

filename = f"\\..\\{test}\\{test}_anchor_interp_data_std_10cm.pkl"
filepath = current_directory + filename
with open(filepath, 'rb') as file:
    anchor_interp_data_10cm = pickle.load(file)

extract_global_10cm = True
if extract_global_10cm:
    ### EXTRACTION DE L'INNOVATION AVEC UWB ###
    file_xpf = f"{current_directory}\\..\\{test}\\{test}_for_analize_std_10cm.xpf"
    xpf_content_uwb,py_fileOutPath = xpf2py(file_xpf, CheckExistence = True )
    date_innov_s_uwb = xpf_content_uwb["data"]['RANGE_KAL_MEAS']["date"].astype(float)*10**(-7)
    date_ins_s_uwb = xpf_content_uwb["data"]["primary_nav"]["date"].astype(float)*10**(-7)
    utc_offset_uwb = (xpf_content_uwb["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_content_uwb["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_content_uwb["data"]["UTC"]["utcSecond"].astype(float)

    innov_o_uwb = {6016 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl3DistOInnov"].astype(float).squeeze(), \
            6017 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl4DistOInnov"].astype(float).squeeze(), \
            6018 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl1DistOInnov"].astype(float).squeeze(), \
            6019 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl2DistOInnov"].astype(float).squeeze()}

    d_meas_xpf_uwb = {6016 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl3distance"].astype(float).squeeze(), \
                6017 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl4distance"].astype(float).squeeze(), \
                6018 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl1distance"].astype(float).squeeze(), \
                6019 : xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl2distance"].astype(float).squeeze()}

    time_ins_anchor_uwb = {6016 : (xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl3Time"].astype(float) + utc_offset).squeeze(), \
                6017 : (xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl4Time"].astype(float) + utc_offset).squeeze(), \
                6018 : (xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl1Time"].astype(float) + utc_offset).squeeze(), \
                6019 : (xpf_content_uwb["data"]['RANGE_KAL_MEAS']["lbl2Time"].astype(float) + utc_offset).squeeze()}

    heading_uwb = xpf_content_uwb["data"]["primary_nav"]["heading"].squeeze()*np.pi/180
    if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (3 + 7*365/12): 
        heading += np.pi

    ins_latitude_uwb = (xpf_content_uwb["data"]["primary_nav"]["latitude"]).astype(float).squeeze()
    ins_longitude_uwb = (xpf_content_uwb["data"]["primary_nav"]["longitude"]).astype(float).squeeze()
    ins_altitude_uwb = (xpf_content_uwb["data"]["primary_nav"]["orthometricHeight"]).astype(float).squeeze()
    ins_x_uwb, ins_y_uwb = coord2cart((ins_latitude_uwb, ins_longitude_uwb))

    time_ins_s_uwb = (date_ins_s + utc_offset).squeeze()
    time_innov_s_uwb = (date_innov_s + utc_offset).squeeze()

    speedEast_uwb = xpf_content_uwb["data"]["primary_nav"]["speedEast"].astype(float).squeeze()
    speedNorth_uwb = xpf_content_uwb["data"]["primary_nav"]["speedNorth"].astype(float).squeeze()
    speedVertical_uwb = xpf_content_uwb["data"]["primary_nav"]["speedVertical"].astype(float).squeeze()

extract_global_mix = False
if extract_global_mix:
    ### EXTRACTION DE L'INNOVATION AVEC UWB ###
    file_xpf = f"{current_directory}\\..\\{test}\\{test}_for_analize_std_mix.xpf"
    xpf_content_mix,py_fileOutPath = xpf2py(file_xpf, CheckExistence = True )
    date_innov_s_mix = xpf_content_mix["data"]['RANGE_KAL_MEAS']["date"].astype(float)*10**(-7)
    date_ins_s_mix = xpf_content_mix["data"]["primary_nav"]["date"].astype(float)*10**(-7)
    utc_offset_mix = (xpf_content_mix["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_content_mix["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_content_mix["data"]["UTC"]["utcSecond"].astype(float)

    innov_o_mix = {6016 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl3DistOInnov"].astype(float).squeeze(), \
            6017 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl4DistOInnov"].astype(float).squeeze(), \
            6018 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl1DistOInnov"].astype(float).squeeze(), \
            6019 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl2DistOInnov"].astype(float).squeeze()}

    d_meas_xpf_mix = {6016 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl3distance"].astype(float).squeeze(), \
                6017 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl4distance"].astype(float).squeeze(), \
                6018 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl1distance"].astype(float).squeeze(), \
                6019 : xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl2distance"].astype(float).squeeze()}

    time_ins_anchor_mix = {6016 : (xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl3Time"].astype(float) + utc_offset).squeeze(), \
                6017 : (xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl4Time"].astype(float) + utc_offset).squeeze(), \
                6018 : (xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl1Time"].astype(float) + utc_offset).squeeze(), \
                6019 : (xpf_content_mix["data"]['RANGE_KAL_MEAS']["lbl2Time"].astype(float) + utc_offset).squeeze()}

    heading_mix = xpf_content_mix["data"]["primary_nav"]["heading"].squeeze()*np.pi/180
    if (float(test.split("_")[0])+float(test.split("_")[1])*365/12) < (3 + 7*365/12): 
        heading += np.pi

    ins_latitude_mix = (xpf_content_mix["data"]["primary_nav"]["latitude"]).astype(float).squeeze()
    ins_longitude_mix = (xpf_content_mix["data"]["primary_nav"]["longitude"]).astype(float).squeeze()
    ins_altitude_mix = (xpf_content_mix["data"]["primary_nav"]["orthometricHeight"]).astype(float).squeeze()
    ins_x_mix, ins_y_mix = coord2cart((ins_latitude_mix, ins_longitude_mix))

    time_ins_s_mix = (date_ins_s + utc_offset).squeeze()
    time_innov_s_mix = (date_innov_s + utc_offset).squeeze()

    speedEast_mix = xpf_content_mix["data"]["primary_nav"]["speedEast"].astype(float).squeeze()
    speedNorth_mix = xpf_content_mix["data"]["primary_nav"]["speedNorth"].astype(float).squeeze()
    speedVertical_mix = xpf_content_mix["data"]["primary_nav"]["speedVertical"].astype(float).squeeze()

for id in np.arange(6016,6020,1):
    anchor_interp_data[id]['Innov_o'] = anchor_interp_data[id]['Innov_o']*100
    anchor_interp_data[id]['lbl_range'] = anchor_interp_data[id]['lbl_range']*100
    # anchor_interp_data[id]['d_meas_xpf'] = anchor_interp_data[id]['d_meas_xpf']*100

    # anchor_interp_data_10cm[id]['Innov_o'] = anchor_interp_data_10cm[id]['Innov_o']*100
    # anchor_interp_data_10cm[id]['lbl_range'] = anchor_interp_data_10cm[id]['lbl_range']*100
    # # anchor_interp_data_10cm[id]['d_meas_xpf'] = anchor_interp_data_10cm[id]['d_meas_xpf']*100


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

sawtooth = lambda theta : (2*np.arctan(np.tan(theta/2)))

fig_rel, axs_rel = plt.subplots(2,2)
fig_rel.suptitle("Erreur absolue après algorithme en (x,y,z)")

for id in np.arange(6016, 6020):
    id_dbm = id - 6016
    ax = axs_rel[id_dbm//2, id_dbm%2]

    t = anchor_interp_data[id]['time']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x = anchor_interp_data[id]['ins_x']
    v1_ins_y = anchor_interp_data[id]['ins_y']
    v1_ins_z = anchor_interp_data[id]['ins_z']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x = anchor_interp_data_10cm[id]['ins_x']
    v2_ins_y = anchor_interp_data_10cm[id]['ins_y']
    v2_ins_z = anchor_interp_data_10cm[id]['ins_z']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins = np.array([v1_ins_x, v1_ins_y, v1_ins_z])
    v2_ins = np.array([v2_ins_x, v2_ins_y, v2_ins_z])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    norm_ins = np.linalg.norm(v1_ins - v2_ins, axis=0)
    ax.scatter(t, norm_ins, s=1, color = 'blue', label = 'get uwb data')

    t_intertial = anchor_interp_data[id]['time_intertial']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x_intertial = anchor_interp_data[id]['ins_x_intertial']
    v1_ins_y_intertial = anchor_interp_data[id]['ins_y_intertial']
    v1_ins_z_intertial = anchor_interp_data[id]['ins_z_intertial']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x_intertial = anchor_interp_data_10cm[id]['ins_x_intertial']
    v2_ins_y_intertial = anchor_interp_data_10cm[id]['ins_y_intertial']
    v2_ins_z_intertial = anchor_interp_data_10cm[id]['ins_z_intertial']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins_intertial = np.array([v1_ins_x_intertial, v1_ins_y_intertial, v1_ins_z_intertial])
    v2_ins_intertial = np.array([v2_ins_x_intertial, v2_ins_y_intertial, v2_ins_z_intertial])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    mask = np.concatenate((np.array([True]), np.diff(t_intertial)>0.01))
    norm_ins_intertial = np.linalg.norm(v1_ins_intertial - v2_ins_intertial, axis=0)
    ax.scatter(t_intertial[mask], norm_ins_intertial[mask], s=1, color = 'red',label='intertial navigation (no uwb)')

    ax.legend()
    ax.set_xlabel("time [s]")
    ax.set_ylabel("Erreur absolue après algorithme [m]")


fig_rel1, axs_rel1 = plt.subplots(2,2)
fig_rel1.suptitle("Erreur absolue après algorithme en (x,y)")

for id in np.arange(6016, 6020):
    id_dbm = id - 6016
    ax = axs_rel1[id_dbm//2, id_dbm%2]

    t = anchor_interp_data[id]['time']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x = anchor_interp_data[id]['ins_x']
    v1_ins_y = anchor_interp_data[id]['ins_y']
    v1_ins_z = anchor_interp_data[id]['ins_z']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x = anchor_interp_data_10cm[id]['ins_x']
    v2_ins_y = anchor_interp_data_10cm[id]['ins_y']
    v2_ins_z = anchor_interp_data_10cm[id]['ins_z']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins = np.array([v1_ins_x, v1_ins_y])
    v2_ins = np.array([v2_ins_x, v2_ins_y])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    norm_ins = np.linalg.norm(v1_ins - v2_ins, axis=0)
    ax.scatter(t, norm_ins, s=1, color = 'blue', label = 'get uwb data')

    t_intertial = anchor_interp_data[id]['time_intertial']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x_intertial = anchor_interp_data[id]['ins_x_intertial']
    v1_ins_y_intertial = anchor_interp_data[id]['ins_y_intertial']
    v1_ins_z_intertial = anchor_interp_data[id]['ins_z_intertial']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x_intertial = anchor_interp_data_10cm[id]['ins_x_intertial']
    v2_ins_y_intertial = anchor_interp_data_10cm[id]['ins_y_intertial']
    v2_ins_z_intertial = anchor_interp_data_10cm[id]['ins_z_intertial']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins_intertial = np.array([v1_ins_x_intertial, v1_ins_y_intertial])
    v2_ins_intertial = np.array([v2_ins_x_intertial, v2_ins_y_intertial])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    mask = np.concatenate((np.array([True]), np.diff(t_intertial)>0.01))
    norm_ins_intertial = np.linalg.norm(v1_ins_intertial - v2_ins_intertial, axis=0)
    ax.scatter(t_intertial[mask], norm_ins_intertial[mask], s=1, color = 'red',label='intertial navigation (no uwb)')

    ax.legend()
    ax.set_xlabel("time [s]")
    ax.set_ylabel("Erreur absolue après algorithme [m]")

plt.figure()
plt.title("Erreur global Intertielle et non Intertielle")
for id in np.arange(6016, 6020):
    t = anchor_interp_data[id]['time']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x = anchor_interp_data[id]['ins_x']
    v1_ins_y = anchor_interp_data[id]['ins_y']
    v1_ins_z = anchor_interp_data[id]['ins_z']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x = anchor_interp_data_10cm[id]['ins_x']
    v2_ins_y = anchor_interp_data_10cm[id]['ins_y']
    v2_ins_z = anchor_interp_data_10cm[id]['ins_z']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins = np.array([v1_ins_x, v1_ins_y])
    v2_ins = np.array([v2_ins_x, v2_ins_y])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    norm_ins = np.linalg.norm(v1_ins - v2_ins, axis=0)
    if id==6016:
        plt.scatter(t, norm_ins, s=1, color = 'blue', label = 'get uwb data')
    else:
        plt.scatter(t, norm_ins, s=1, color = 'blue')

    t_intertial = anchor_interp_data[id]['time_intertial']
    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data
    v1_ins_x_intertial = anchor_interp_data[id]['ins_x_intertial']
    v1_ins_y_intertial = anchor_interp_data[id]['ins_y_intertial']
    v1_ins_z_intertial = anchor_interp_data[id]['ins_z_intertial']

    # Extrait les vecteurs 'ins_x', 'ins_y', et 'ins_z' de anchor_interp_data_10cm
    v2_ins_x_intertial = anchor_interp_data_10cm[id]['ins_x_intertial']
    v2_ins_y_intertial = anchor_interp_data_10cm[id]['ins_y_intertial']
    v2_ins_z_intertial = anchor_interp_data_10cm[id]['ins_z_intertial']

    # Concatène les vecteurs pour obtenir le vecteur complet pour chaque position (x, y, z)
    v1_ins_intertial = np.array([v1_ins_x_intertial, v1_ins_y_intertial])
    v2_ins_intertial = np.array([v2_ins_x_intertial, v2_ins_y_intertial])

    # Calcule la norme euclidienne entre les deux vecteurs 'ins'
    mask = np.concatenate((np.array([True]), np.diff(t_intertial)>0.01))
    norm_ins_intertial = np.linalg.norm(v1_ins_intertial - v2_ins_intertial, axis=0)
    if id==6016:
        plt.scatter(t_intertial[mask], norm_ins_intertial[mask], s=1, color = 'red',label='intertial navigation (no uwb)')
    else:
        plt.scatter(t_intertial[mask], norm_ins_intertial[mask], s=1, color = 'red')

    plt.legend()
    plt.xlabel("time [s]")
    plt.ylabel("Erreur absolue après algorithme [m]")

plt.figure()
plt.title("Erreur absolue après algo")
v1_ins = np.array([ins_x, ins_y, ins_altitude])
v1_ins_uwb = np.array([ins_x_uwb, ins_y_uwb, ins_altitude_uwb])
norm_ins = np.linalg.norm(v1_ins - v1_ins_uwb, axis=0)
plt.scatter(time_ins_s, norm_ins, s=1,label='en (x,y,z)')

#find alignement
val_to_mean = 20
beta = 0.1
diff_dep = np.sqrt(np.diff(ins_x)**2 + np.diff(ins_y)**2 + np.diff(ins_altitude)**2)
print(diff_dep)
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

plt.plot(time_ins_s[start_idx_ali:end_idx_ali], np.mean(norm_ins)*np.ones(time_ins_s[start_idx_ali:end_idx_ali].shape), label = f"mean = {np.mean(norm_ins)}")

v1_ins = np.array([ins_x, ins_y])
v1_ins_uwb = np.array([ins_x_uwb, ins_y_uwb])
norm_ins = np.linalg.norm(v1_ins - v1_ins_uwb, axis=0)
plt.scatter(time_ins_s, norm_ins, s=1, label='en (x,y)')
plt.plot(time_ins_s[start_idx_ali:end_idx_ali], np.mean(norm_ins)*np.ones(time_ins_s[start_idx_ali:end_idx_ali].shape), label = f"mean = {np.mean(norm_ins)}")
plt.xlabel("Time [s]")
plt.ylabel("||d_ref - d_uwb|| [m]")
plt.legend()

plt.figure()
plt.title("INS error (x)")
plt.plot(anchor_interp_data[6016]['time'], anchor_interp_data[6016]['ins_x'],label='uwb')
plt.plot(anchor_interp_data_10cm[6016]['time_intertial'], anchor_interp_data_10cm[6016]['ins_x_intertial'],label='intertial')
if switch:
    plt.plot(time_ins_s, ins_x, label='reference')
plt.xlabel("Time [s]")
plt.ylabel("ins_x [m]")
plt.plot()
plt.legend()
plt.show()