"""
This program is used to separate the data :
    - Beacon id staring with 6016 + N (dec) = 0x1780 + N (hex) and correspond to the real lat/lon/depth
    - Beacon id staring with 16 + N (dec) is used to create dbm values in delphINS

        Store as                        Correspond to
        ----------------------------------------------
        Longitude [m]                   -FPPower (10log((f1^2 + f2^2 + f3^2)/N^2) - A) [dbm]
        Latitude [m]                    -RXPower (10log(C/N^2)-A) [dbm]
        Depth [m]                       Quality (f2/std_noise) [dbm]
        Range  [m]                      RXPower - FPPower [dbm]
        Beacon_range_std_dev            FPPower/std_noise

This was created in order to characterize LOS/NLOS on RLTS.
"""

import os
import numpy as np

# Chemin absolu du fichier
current_directory = os.path.dirname(__file__)

filename = 'dbm_19_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.txt'
file_path = current_directory+f"\\19_06_2023\\{filename}"

data = np.genfromtxt(file_path, delimiter='\t', skip_header = 12, dtype='<U15')

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

latitude = data[:, 3].astype(float)
longitude = data[:, 4].astype(float)

times = [value.split(":") for value in data[:, 1].astype(str)]
times = [float(value[1])*60 + float(value[2]) for value in times]
times = (np.array(times) - np.array(times[0]))/60

beacon_id = '17'
mask = np.where(data[:, 2] == beacon_id)[0]  # Use np.where to create the mask

sigma = 2.3334
f_inv = lambda x : (x - 88*sigma)/(1 + sigma)

# for i in range(latitude.shape[0]):
#     if -latitude[i] > -88:
#         latitude[i] = -f_inv(-latitude[i])

for i in range(latitude.shape[0]):
    if latitude[i] < 50:
        latitude[i] += 90

plt.figure()
plt.title('dbm_' + filename + '\n' + "LATITUDE" + f" for n°{beacon_id}")
plt.xlabel("Time [min]")
plt.ylabel("Latitude")
plt.scatter(times[mask], (latitude[mask] - longitude[mask]), s=1, label='data')
plt.plot(times[mask], [88]*latitude[mask].shape[0], color = 'red', label='limit')
plt.legend()

# range = data[:, 6].astype(float)
# plt.figure()
# plt.title('dbm_' + filename + '\n' + "RANGE" + f" for n°{beacon_id}")
# plt.xlabel("Time [min]")
# plt.ylabel("range")
# plt.scatter(times[mask], range[mask], s=1)

plt.show()
