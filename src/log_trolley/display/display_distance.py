import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib.colors as mcolors
import os
from import_data import ins_latitude, ins_longitude, coord2cart, sawtooth

# test = '28_06_2023'
# test = '03_07_2023'
# test = '05_07_2023'
# test = '11_07_2023'
# test = '17_07_2023_2'
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
import numpy as np
import matplotlib.pyplot as plt

# ... (votre code existant) ...

fig, axs = plt.subplots(nrows=2, ncols=2)
fig.suptitle("Erreur en fonction de la distance")

fig1, axs1 = plt.subplots(nrows=2, ncols=2)
fig1.suptitle("Erreur en fonction de la distance")

limite_innov = 0.5

for (id, b) in data:
    nid = id - 6016
    ax = axs[nid // 2, nid % 2]
    ax1 = axs1[nid // 2, nid % 2]

    mask = np.abs(b["Innov_o"]) < limite_innov
    # mask = np.array([True]*b["Innov_o"].shape[0])

    print("before ",np.mean(b["Innov_o"][mask]))
    b["Innov_o"] -= np.mean(b["Innov_o"][mask])
    print("after ",np.mean(b["Innov_o"][mask]),"\n")

    ax.scatter(b['beacon_x'], b['beacon_y'], color='green', marker='x', label=f"anchor n°{id}")
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")

    cmap = 'RdBu'
    cax = ax.scatter(b['ins_x'][mask], b['ins_y'][mask], c=(b["Innov_o"][mask]), cmap=cmap, s=1, label='data received and innov < thresold')
    
    ax1.set_title(hex(int(id)))
    ax1.plot(b['time'], b["Innov_o"])
    ax1.set_ylim([-2, 2])
    
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array((b["Innov_o"][mask]))
    
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label('Innovation [m]', rotation=270, labelpad=15)
    
    sm.set_clim(-limite_innov, limite_innov)  # Définir les limites de la colorbar
    
    ax.legend()

plt.show()
