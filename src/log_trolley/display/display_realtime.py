import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from import_data import coord2cart, ins_latitude, ins_longitude
import os
import pickle

# test = '03_07_2023'
# test = '05_07_2023'
# test = '11_07_2023'
# test = '17_07_2023_2'
# test = '17_07_2023'
test = '26_07_2023'

# Charger le dictionnaire à partir du fichier
filename = f"\\..\\{test}\\{test}_anchor_interp_data.pkl"
current_directory = os.path.dirname(__file__)
filepath = current_directory + filename
with open(filepath, 'rb') as file:
    anchor_interp_data = pickle.load(file)
# Convertir les coordonnées de la centrale en coordonnées cartésiennes
ins_x, ins_y = coord2cart((ins_latitude, ins_longitude))

data = list(anchor_interp_data.items())

### EN MOUVEMENT ###
fig, ax = plt.subplots()
fig.suptitle("Evolution of LOS/NLOS")
id = 6017
b = anchor_interp_data[id]

INS_LOS = []; INS_NLOS = []
d = np.sqrt((b['ins_x'] - b['beacon_x'])**2 + (b['ins_y'] - b["beacon_y"])**2)

print(b['time'])
plt.ion()
for i in range(b['time'].shape[0]):
    # if d[i] < 20:
    # if (b["RXPower"] - b["FPPower"])[i] > 12: 
    
    # if (b["RXPower_FPPower"])[i] > 12:
    # if b["Quality"][i] > 200:
    if (b['RXPower_FPPower'])[i] < 6:
        INS_LOS.append([b['ins_x'][i,], b['ins_y'][i,]])

    else:
        INS_NLOS.append([b['ins_x'][i,], b['ins_y'][i,]])

    if i % 10 == 0:
        ax.cla()
        # fig.clf()
        #Global display
        ax.scatter(b['beacon_x'], b['beacon_y'], color = 'green', marker = 'x', label = f"anchor n°{id}")

        ax.scatter(ins_x, ins_y,color='blue',s=0.5,label='all trajectry')
        # ax.scatter(b['ins_x'][:i,], b['ins_y'][:i,],color='black',s=3,label="NLOS")
        try:
            ax.scatter(np.array(INS_LOS)[:,0], np.array(INS_LOS)[:,1],color='red',label='LOS', s=3)
        except:
            print("No LOS data")

        try:
            ax.scatter(np.array(INS_NLOS)[:,0], np.array(INS_NLOS)[:,1],color='black',label='NLOS', s=3)
        except:
            print("No NLOS data")

        ax.legend()
        plt.pause(0.001)


plt.pause(100)