import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from import_data import ins_latitude, ins_longitude, coord2cart, sawtooth

# test = '28_06_2023'
# test = '03_07_2023'
# test = '05_07_2023'
test = '11_07_2023'
# test = '17_07_2023_2'
# test = '17_07_2023'
# test = '26_07_2023'

# Charger le dictionnaire à partir du fichier
filename = f"\\..\\{test}\\{test}_anchor_interp_data.pkl"
current_directory = os.path.dirname(__file__)
filepath = current_directory + filename
with open(filepath, 'rb') as file:
    anchor_interp_data = pickle.load(file)
    
# Convertir les coordonnées de la centrale en coordonnées cartésiennes
ins_x, ins_y = coord2cart((ins_latitude, ins_longitude))

data = list(anchor_interp_data.items())

from matplotlib.widgets import Slider


### Draw a slider for quality factor
Q_max = 120
Q_max_min = 0
Q_max_max = 500
fig, axs = plt.subplots(nrows=2, ncols=2)
fig.suptitle("if Quality > val then LOS")
plt.subplots_adjust(bottom=0.25)
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'threshold', Q_max_min, Q_max_max, valinit=Q_max)

def update_quality(val):
    Q_max = slider.val

    for (id, b) in data:
        # b["Innov_o"] -= np.mean(b["Innov_o"])
        nid = id - 6016
        ax1 = axs[nid // 2, nid % 2]

        INN_LOS = []
        INN_NLOS = []
        INS_LOS = []
        INS_NLOS = []
        ORI_LOS = []
        ORI_NLOS = []

        d = np.sqrt((b['ins_x'] - b['beacon_x'])**2 + (b['ins_y'] - b['beacon_y'])**2)
        orientation = sawtooth(np.arctan2((b["beacon_y"] - b["ins_y"]), (b["beacon_x"] - b["ins_x"])) - np.pi / 2 - b["heading"])

        # Filtered indices based on condition
        los_indices = np.where(b["Quality"] >= Q_max)[0]
        nlos_indices = np.where(b["Quality"] < Q_max)[0]

        INS_LOS = np.stack([b['ins_x'][los_indices], b['ins_y'][los_indices]], axis=1)
        INN_LOS = b["Innov_o"][los_indices]
        ORI_LOS = orientation[los_indices]

        INS_NLOS = np.stack([b['ins_x'][nlos_indices], b['ins_y'][nlos_indices]], axis=1)
        INN_NLOS = b["Innov_o"][nlos_indices]
        ORI_NLOS = orientation[nlos_indices]

        # Global display
        ax1.clear()
        ax1.scatter(b['beacon_x'], b['beacon_y'], color='green', marker='x', label=f"anchor n°{id}")
        ax1.scatter(ins_x, ins_y, color='blue', s=0.5, label='all trajectory')
        # ax1.scatter(b['ins_x'][:i], b['ins_y'][:i], color='black', s=3, label="NLOS")

        try:
            ax1.scatter(INS_LOS[:, 0], INS_LOS[:, 1], color='red', label='LOS', s=3)
            # ax.scatter(ORI_LOS, INN_LOS, s=1.5, label='data innov(orientation) LOS', color='red')
        except:
            print("No LOS data")

        try:
            ax1.scatter(INS_NLOS[:, 0], INS_NLOS[:, 1], color='black', label='NLOS', s=3)
            # ax.scatter(ORI_NLOS, INN_NLOS, s=1.5, label='data innov(orientation) NLOS', color='black')
        except:
            print("No NLOS data")

        # ax.set_ylim([-2, 2])
        # ax.legend()
        ax1.legend()
        ax1.set_xlabel("longitude")
        ax1.set_ylabel("latitude")

    fig.canvas.draw_idle()

slider.on_changed(update_quality)


### Draw Slider for RX - FP
rxpower_max = 6
rxpower_max_min = 0
rxpower_max_max = 30
fig_rxfp, axs_rxfp = plt.subplots(nrows=2, ncols=2)
fig_rxfp.suptitle("If RX - FP < val then LOS")
plt.subplots_adjust(bottom=0.25)

# Create the slider
ax_slider_rxfp = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_rxfp = Slider(ax_slider_rxfp, 'threshold', rxpower_max_min, rxpower_max_max, valinit=rxpower_max)

# Update the plot when the slider value changes
def update_rxfp(val):
    # rxpower_max = slider.val
    rxpower_max = slider_rxfp.val

    for (id, b) in data:
        nid = id - 6016
        ax1 = axs_rxfp[nid // 2, nid % 2]

        INS_LOS = []
        INS_NLOS = []

        # Filtered indices based on condition
        los_indices = np.where(b["RXPower_FPPower"] <= rxpower_max)[0]
        nlos_indices = np.where(b["RXPower_FPPower"] > rxpower_max)[0]

        INS_LOS = np.stack([b['ins_x'][los_indices], b['ins_y'][los_indices]], axis=1)

        INS_NLOS = np.stack([b['ins_x'][nlos_indices], b['ins_y'][nlos_indices]], axis=1)

        # Global display
        ax1.clear()
        ax1.scatter(b['beacon_x'], b['beacon_y'], color='green', marker='x', label=f"anchor n°{id}")
        ax1.scatter(ins_x, ins_y, color='blue', s=0.5, label='all trajectory')
        # ax1.scatter(b['ins_x'][:i], b['ins_y'][:i], color='black', s=3, label="NLOS")

        try:
            ax1.scatter(INS_LOS[:, 0], INS_LOS[:, 1], color='red', label='LOS', s=3)
        except:
            print("No LOS data")

        try:
            ax1.scatter(INS_NLOS[:, 0], INS_NLOS[:, 1], color='black', label='NLOS', s=3)
        except:
            print("No NLOS data")

        ax1.legend()
        ax1.set_xlabel("longitude")
        ax1.set_ylabel("latitude")

    fig_rxfp.canvas.draw_idle()

slider_rxfp.on_changed(update_rxfp)
plt.show()