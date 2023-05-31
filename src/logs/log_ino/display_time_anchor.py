import numpy as np
import matplotlib.pyplot as plt
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# Charger les données depuis le fichier CSV
# data = np.genfromtxt(f'{THIS_FOLDER}/save_times.csv', delimiter=';', skip_header=1, dtype=str)
# data[:,1] = np.float(data[:,1])

# data = np.genfromtxt(f'{THIS_FOLDER}/17_05_2023_15_35_29_log-all-with-time.csv', delimiter=';', skip_header=1, dtype='str')
# data = np.genfromtxt(f'{THIS_FOLDER}/26_05_2023_17_20_07_log-all-with-time.csv', delimiter=';', skip_header=1)

filename = 'anchor/30_05_2023_17_07_35_log-all-with-time.csv'
data = np.genfromtxt(f'{THIS_FOLDER}/{filename}', delimiter=';', skip_header=1)
# data = np.genfromtxt(f'{THIS_FOLDER}/30_05_2023_17_07_39_log-all-with-time.csv', delimiter=';', skip_header=1)

# Extraire les colonnes pertinentes
names = data[:, 0]
values = data[:, 1].astype(float)

if np.unique(names).shape[0] > 1 :
    data = data[data[:, 0].astype(float) == 1780]
    names = data[:, 0]
    values = data[:, 1].astype(float)

print(f"Using tag 7D")

# # Trouver les indices correspondant aux noms des colonnes
# timeINO_indices = np.where(names == 'timeINO')[0]
# timeRangeSent_indices = np.where(names == 'timeRangeSent')[0]
# timePollSent_indices = np.where(names == 'timePollSent')[0]
# timePollAckReceived_indices = np.where(names == 'timePollAckReceived')[0]

# # Extraire les valeurs correspondantes aux indices trouvés
# timeINO = values[timeINO_indices]*10**(-3)
# timeRangeSent = values[timeRangeSent_indices]*10**(-6)
# timePollSent = values[timePollSent_indices]*10**(-6)
# timePollAckReceived = values[timePollAckReceived_indices]

timeINO = data[:,1].astype(float)*10**(-3)
timePollSent = data[:,6].astype(float)*10**(-6)
timePollReceived = data[:,7].astype(float)*10**(-6)
timePollAckSent = data[:,8].astype(float)*10**(-6)
timePollAckReceived = data[:,9].astype(float)*10**(-6)
timeRangeSent = data[:,10].astype(float)*10**(-6)
timeRangeReceived = data[:,11].astype(float)*10**(-6)

# print(f"Shape of timeINO: {timeINO.shape}")
# print(f"Shape of timePollSent: {timePollSent.shape}")
# print(f"Shape of timePollReceived: {timePollReceived.shape}")
# print(f"Shape of timePollAckSent: {timePollAckSent.shape}")
# print(f"Shape of timePollAckReceived: {timePollAckReceived.shape}")
# print(f"Shape of timeRangeSent: {timeRangeSent.shape}")
# print(f"Shape of timeRangeReceived: {timeRangeReceived.shape}")


######################### SAWTOOTH-1 #########################

timestamp = 1099511627775  # Valeur du timestamp
timeoverflow = 1099511627776
timeres = 0.000015650040064103
offset = (timestamp % timeoverflow) * timeres * 10 ** (-6)

k = 0
newtimeINO = np.zeros(timeINO.shape)
newtimeINO[0] = timeINO[0]
for i in range(1, timeINO.shape[0]):
    if timeINO[i] < timeINO[i - 1]:
        k += 1
    newtimeINO[i] = (k * offset + timeINO[i])

k = 0
newtimePollSent = np.zeros(timePollSent.shape)
newtimePollSent[0] = timePollSent[0]
for i in range(1, timePollSent.shape[0]):
    if timePollSent[i] < timePollSent[i - 1]:
        k += 1
    newtimePollSent[i] = (k * offset + timePollSent[i])

k = 0
newtimePollReceived = np.zeros(timePollReceived.shape)
newtimePollReceived[0] = timePollReceived[0]
for i in range(1, timePollReceived.shape[0]):
    if timePollReceived[i] < timePollReceived[i - 1]:
        k += 1
    newtimePollReceived[i] = (k * offset + timePollReceived[i])

k = 0
newtimePollAckSent = np.zeros(timePollAckSent.shape)
newtimePollAckSent[0] = timePollAckSent[0]
for i in range(1, timePollAckSent.shape[0]):
    if timePollAckSent[i] < timePollAckSent[i - 1]:
        k += 1
    newtimePollAckSent[i] = (k * offset + timePollAckSent[i])

k = 0
newtimePollAckReceived = np.zeros(timePollAckReceived.shape)
newtimePollAckReceived[0] = timePollAckReceived[0]
for i in range(1, timePollAckReceived.shape[0]):
    if timePollAckReceived[i] < timePollAckReceived[i - 1]:
        k += 1
    newtimePollAckReceived[i] = (k * offset + timePollAckReceived[i])

k = 0
newtimeRangeSent = np.zeros(timeRangeSent.shape)
newtimeRangeSent[0] = timeRangeSent[0]
for i in range(1, timeRangeSent.shape[0]):
    if timeRangeSent[i] < timeRangeSent[i - 1]:
        k += 1
    newtimeRangeSent[i] = (k * offset + timeRangeSent[i])

k = 0
newtimeRangeReceived = np.zeros(timeRangeReceived.shape)
newtimeRangeReceived[0] = timeRangeReceived[0]
for i in range(1, timeRangeReceived.shape[0]):
    if timeRangeReceived[i] < timeRangeReceived[i - 1]:
        k += 1
    newtimeRangeReceived[i] = (k * offset + timeRangeReceived[i])

print(f"Shape of newtimeINO: {newtimeINO.shape}")
print(f"Shape of newtimePollSent: {newtimePollSent.shape}")
print(f"Shape of newtimePollReceived: {newtimePollReceived.shape}")
print(f"Shape of newtimePollAckSent: {newtimePollAckSent.shape}")
print(f"Shape of newtimePollAckReceived: {newtimePollAckReceived.shape}")
print(f"Shape of newtimeRangeSent: {newtimeRangeSent.shape}")
print(f"Shape of newtimeRangeReceived: {newtimeRangeReceived.shape}")

from sklearn.metrics import r2_score
def plot_polynomial_regression(ax, x, y, degrees, label = ""):
    coeffs = [np.polyfit(x, y, degree) for degree in degrees]
    print(coeffs)
    ax.scatter(x, y, s = 1)
    for i, c in enumerate(coeffs):
        line_x = np.linspace(min(x), max(x), 10000)
        line_y = np.polyval(c, line_x)
        r_squared = r2_score(y, np.polyval(c, x))
        eqn = f"y = {c[-1]:.3f} + {' + '.join([f'{c[j]:.3f}x^{len(c)-j-1}' if len(c)-j-1 > 1 else f'{c[j]:.3f}x' if len(c)-j-1 == 1 else f'{c[j]:.3f}' for j in range(len(c)-2, -1, -1)])}" if len(c) > 1 else f"y = {c[-1]:.3f}"
        ax.plot(line_x, line_y, label=f'Degree {degrees[i]}: {eqn} (R² = {r_squared:.3f}) \n'+label)
    ax.legend(loc='upper left')



######################### ROGNAGE #########################
idx_start = np.where(timeINO/3600 >= 1)[0][0] #1 #151720
idx_end = -1000 # np.where(timeINO/3600 >= 4)[0][0] #-1 #151750

timeINO = timeINO[idx_start:idx_end]
newtimePollSent = newtimePollSent[idx_start:idx_end]
newtimeRangeSent = newtimeRangeSent[idx_start:idx_end]
newtimePollReceived = newtimePollReceived[idx_start:idx_end]
newtimePollAckSent = newtimePollAckSent[idx_start:idx_end]
newtimePollAckReceived = newtimePollAckReceived[idx_start:idx_end]
newtimeRangeReceived = newtimeRangeReceived[idx_start:idx_end]

print(f"Shape of newtimePollSent: {newtimePollSent.shape}")
print(f"Shape of newtimeRangeSent: {newtimeRangeSent.shape}")
print(f"Shape of timeINO: {timeINO.shape}")
print(f"Shape of timePollReceived: {timePollReceived.shape}")
print(f"Shape of timePollAckSent: {timePollAckSent.shape}")
print(f"Shape of timePollAckReceived: {timePollAckReceived.shape}")
print(f"Shape of timeRangeReceived: {timeRangeReceived.shape}")

it = np.arange(newtimeRangeSent.shape[0])
it_ino = np.arange(timeINO.shape[0])

# # mask = np.abs(timeINO - newtimeRangeSent) > 0.01
# mask = np.abs(timeINO - newtimeRangeSent) > 0.01
# print(f"We use {timeINO[~mask].shape[0]/timeINO.shape[0]*100}% of the data")

# newtimePollSent = newtimePollSent[~mask]
# newtimeRangeSent = newtimeRangeSent[~mask]
# timeINO = timeINO[~mask]
# it = it[~mask]

######################### POLYNOMIAL REGRESSION #########################


fig, ax = plt.subplots()
ax.set_title("Clocks")
ax.set_xlabel("it")
ax.set_ylabel("time [s]")
plot_polynomial_regression(ax, it, newtimeRangeSent,[1],"newtimeRangeSent")
plot_polynomial_regression(ax, it, newtimePollSent,[1],"newtimePollSent")
plot_polynomial_regression(ax, it_ino, timeINO,[1],"timeINO")
ax.set_xlabel("it")
ax.set_ylabel("time [s]")


######################### AFFICHAGE #########################
# Calculer la différence entre deux valeurs
timeRangeDiff = np.diff(newtimeRangeSent)
timeINODiff = np.diff(timeINO)
timePollDiff = np.diff(newtimeRangeSent)

# Pour afficher les transformées de dents de scie à linéaire
display_tf = 0
display_diff = 0
display_rest = 1

if display_tf:
    #Affiche les valeurs d'envoie et de reception en secondes
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.plot(timePollSent, 'r')
    plt.xlabel('it')
    plt.ylabel('timePollSent [s]')
    plt.title("Dent de scie")

    # Tracer les graphiques timePollSent, timePollAckReceived, timeRangeSent
    plt.subplot(2, 2, 2)
    plt.plot(timeRangeSent, 'g')
    plt.xlabel('it')
    plt.ylabel('timeRangeSent [s]')
    plt.title("Dent de scie")
    plt.tight_layout()

    #Affiche les valeurs d'envoie et de reception en secondes
    plt.subplot(2, 2, 3)
    plt.plot(newtimePollSent/3600, 'r')
    plt.xlabel('it')
    plt.ylabel('newtimePollSent [h]')
    plt.title("Sans dent de scie")

    # Tracer les graphiques newtimePollSent, timePollAckReceived, newtimeRangeSent
    plt.subplot(2, 2, 4)
    plt.plot(newtimeRangeSent/3600, 'g')
    plt.xlabel('it')
    plt.ylabel('newtimeRangeSent [h]')
    plt.title("Sans dent de scie")

if display_diff:
    plt.figure()
    plt.scatter(it[:-1], timeRangeDiff, s = 1, label = 'diff newtimeRangeSent [s]', color = 'red')
    plt.scatter(it[:-1], timePollDiff, s = 1, label = 'diff newtimePollSent [s]', color = 'green')
    plt.scatter(it_ino[:-1], timeINODiff, s = 1, label = 'diff timeINO [s]', color = 'black')
    plt.xlabel("it")
    plt.ylabel("time")
    plt.legend(loc='upper left')

print("Résultats : ")
print(f"Intervalle de temps pour une boucle : {np.mean(timePollSent)}")

print(f"shape of RS {newtimeRangeSent.shape}; shape of PS {newtimePollSent.shape}")

if display_rest:
    plt.figure()
    plt.title("timeRange - timePoll")
    plt.xlabel("it")
    plt.ylabel("time [s]")
    plt.plot(it, newtimeRangeSent - newtimePollSent)

    plt.figure()
    plt.title("timeRange - timeRangeReceived")
    plt.xlabel("it")
    plt.ylabel("time [s]")
    plt.plot(it, newtimeRangeReceived - newtimePollSent)
    # plt.show()

    plt.figure()
    plt.title("timeINO - timeRangeSent")
    plt.xlabel("it")
    plt.ylabel("time [s]")
    plt.scatter(it, timeINO - newtimeRangeSent, s = 1)

    plt.figure()
    plt.title("diff(timeINO - timeRangeSent)")
    plt.xlabel("it")
    plt.ylabel("time [s]")
    plt.scatter(it[1:], np.diff(timeINO - newtimeRangeSent), s = 1)



    fig,ax = plt.subplots()
    plot_polynomial_regression(ax, it, timeINO - newtimeRangeSent,[1],"diff(timeINO - timeRangeSent)")
    plt.show()