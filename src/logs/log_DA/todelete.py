import numpy as np
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_receiverTime = np.genfromtxt(os.path.join(THIS_FOLDER, "charieau.sbf_SBF_ReceiverTime.txt"), skip_header=7, dtype='<U2', delimiter=",")
data_utc = np.array(["20" + a for a in data_receiverTime[:, 10]])

for i in range(1, 7):
    if i < 3 :car = ":"
    elif i == 3: car = "T"
    else: car = ":"
    data_utc = np.array([a + car + b for a, b in zip(data_utc, data_receiverTime[:, 10 + i])])

print(data_utc)
