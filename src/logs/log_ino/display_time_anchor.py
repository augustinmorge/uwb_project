import numpy as np
import matplotlib.pyplot as plt
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# Charger les données depuis le fichier CSV
# data = np.genfromtxt(f'{THIS_FOLDER}/save_times.csv', delimiter=';', skip_header=1, dtype=str)
# data[:,1] = np.float(data[:,1])

# data = np.genfromtxt(f'{THIS_FOLDER}/17_05_2023_15_35_29_log-all-with-time.csv', delimiter=';', skip_header=1, dtype='str')
# data = np.genfromtxt(f'{THIS_FOLDER}/26_05_2023_17_20_07_log-all-with-time.csv', delimiter=';', skip_header=1)

# filename = f'{THIS_FOLDER}/anchor/30_05_2023_17_07_35_log-all-with-time.csv'
filename = f'{THIS_FOLDER}/anchor/05_06_2023_11_58_37_log-all-with-time.csv'

data = np.genfromtxt(f'{filename}', delimiter=';', skip_header=1)
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

print(f"Shape of timeINO: {timeINO.shape}")
print(f"Shape of timePollSent: {timePollSent.shape}")
print(f"Shape of timePollReceived: {timePollReceived.shape}")
print(f"Shape of timePollAckSent: {timePollAckSent.shape}")
print(f"Shape of timePollAckReceived: {timePollAckReceived.shape}")
print(f"Shape of timeRangeSent: {timeRangeSent.shape}")
print(f"Shape of timeRangeReceived: {timeRangeReceived.shape}")


######################### SAWTOOTH-1 #########################

timestamp = 1099511627775  # Valeur du timestamp
timeoverflow = 1099511627776
timeres = 0.000015650040064103
offset = (timestamp % timeoverflow) * timeres * 10 ** (-6)

def adjust_time_array(time_array):
    k = 0
    new_time_array = np.zeros(time_array.shape)
    new_time_array[0] = time_array[0]

    for i in range(1, time_array.shape[0]):
        if time_array[i] < time_array[i - 1]:
            k += 1
        new_time_array[i] = (k * offset + time_array[i])

    # new_time_array = np.cumsum((time_array < np.roll(time_array, 1)).astype(int) * offset) + time_array

    return new_time_array

newtimeINO = adjust_time_array(timeINO)
newtimePollSent = adjust_time_array(timePollSent)
newtimePollReceived = adjust_time_array(timePollReceived)
newtimePollAckSent = adjust_time_array(timePollAckSent)
newtimePollAckReceived = adjust_time_array(timePollAckReceived)
newtimeRangeSent = adjust_time_array(timeRangeSent)
newtimeRangeReceived = adjust_time_array(timeRangeReceived)


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


def wrap(time):
    for i in range(time.shape[0]):
        if time[i] < 0:
            time[i] += offset
    return time

######################### ROGNAGE #########################
idx_start = np.where(timeINO/3600 >= 0.5)[0][0] #1 #151720
idx_end = -1000 # np.where(timeINO/3600 >= 4)[0][0] #-1 #151750

timeINO = timeINO[idx_start:idx_end]
newtimePollSent = newtimePollSent[idx_start:idx_end]
newtimeRangeSent = newtimeRangeSent[idx_start:idx_end]
newtimePollReceived = newtimePollReceived[idx_start:idx_end]
newtimePollAckSent = newtimePollAckSent[idx_start:idx_end]
newtimePollAckReceived = newtimePollAckReceived[idx_start:idx_end]
newtimeRangeReceived = newtimeRangeReceived[idx_start:idx_end]

# print(f"Shape of newtimePollSent: {newtimePollSent.shape}")
# print(f"Shape of newtimeRangeSent: {newtimeRangeSent.shape}")
# print(f"Shape of timeINO: {timeINO.shape}")
# print(f"Shape of timePollReceived: {timePollReceived.shape}")
# print(f"Shape of timePollAckSent: {timePollAckSent.shape}")
# print(f"Shape of timePollAckReceived: {timePollAckReceived.shape}")
# print(f"Shape of timeRangeReceived: {timeRangeReceived.shape}")

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
plot_polynomial_regression(ax, it, newtimeRangeReceived,[1],"newtimeRangeReceived")
plot_polynomial_regression(ax, it_ino, timeINO,[1],"timeINO")
ax.set_xlabel("it")
ax.set_ylabel("time [s]")


######################### AFFICHAGE #########################
# Calculer la différence entre deux valeurs
timeRangeDiff = np.diff(newtimeRangeSent)
timeINODiff = np.diff(timeINO)
timePollDiff = np.diff(newtimeRangeSent)

# Pour afficher les transformées de dents de scie à linéaire
display_tf = 1
display_diff = 0
display_rest = 0

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

    # fig,ax = plt.subplots()
    # plot_polynomial_regression(ax, it, timeINO - newtimeRangeSent,[1],"diff(timeINO - timeRangeSent)")
    # plt.show()



# Données des variables
time_diffs_1 = [
    newtimePollReceived - newtimePollSent,
    newtimePollAckSent - newtimePollSent,
    newtimePollAckReceived - newtimePollSent,
    newtimeRangeSent - newtimePollSent,
    newtimeRangeReceived - newtimePollSent,
    ((newtimeRangeReceived - newtimePollAckSent) + (newtimePollReceived - newtimePollSent)) - (newtimeRangeSent - newtimePollSent),
]

from display_long_log import load_data
_, dist, ids, _, _, _, _, _ = load_data(filename)
dist = dist #[idx_start:idx_end]
# dist = dist[ids == np.unique(names)[0]]
round1 = (timePollAckReceived-timePollSent) #[idx_start:idx_end]
reply1 = (timePollAckSent-timePollReceived) #[idx_start:idx_end]
round2 = (timeRangeReceived-timePollAckSent) #[idx_start:idx_end]
reply2 = (timeRangeSent-timePollAckReceived) #[idx_start:idx_end]
tof = (round1*round2-reply1*reply2)/(round1+round2+reply1+reply2)
full_it = np.arange(0,timePollSent.shape[0],1)


time_diffs_2 = [
    # round1,
    # reply1,
    # round2,
    # reply2,
    # tof,
    # dist,
    # timeRangeReceived - timeRangeSent,

    wrap(timePollReceived - timePollSent),
    wrap(timePollAckSent - timePollSent),
    wrap(timePollAckReceived - timePollSent),
    wrap(timeRangeSent - timePollSent),
    wrap(timeRangeReceived - timePollSent),
    wrap(timeRangeReceived - timeRangeSent),

    # newtimePollReceived - timeINO,
    # newtimePollAckSent - timeINO,
    # newtimePollAckReceived - timeINO,
    # newtimeRangeSent - timeINO,
    # newtimeRangeReceived - timeINO,
    # (newtimeRangeSent - timeINO) + (newtimePollSent - timeINO),
    # np.zeros((newtimeRangeReceived - timeINO).shape),
]

round1 = wrap(round1)
reply1 = wrap(reply1)
round2 = wrap(round2)
reply2 = wrap(reply2)
tof = (round1*round2-reply1*reply2)/(round1+round2+reply1+reply2)

time_diffs_3 = [

    wrap(timePollReceived - timePollReceived),
    wrap(timePollAckSent - timePollReceived),
    wrap(timePollAckReceived - timePollReceived),
    wrap(timeRangeSent - timePollReceived),
    wrap(timeRangeReceived - timePollReceived),
    wrap(timeRangeReceived - timeRangeSent),

    # round1,
    # reply1,
    # round2,
    # reply2,
    # tof,
    # dist,

    # timePollSent,
    # timePollReceived,
    # timePollAckSent,
    # timePollAckReceived,
    # timeRangeSent,
    # timeRangeReceived,
]

print(f"max timePollSent : {np.max(timePollSent)}")
print(f"max timePollReceived : {np.max(timePollReceived)}")
print(f"max timePollAckSent : {np.max(timePollAckSent)}")
print(f"max timePollAckReceived : {np.max(timePollAckReceived)}")
print(f"max timeRangeSent : {np.max(timeRangeSent)}")
print(f"max timeRangeReceived : {np.max(timeRangeReceived)}")


# Titres et labels
variable_names = [
    "newtimePollReceived",
    "newtimePollAckSent",
    "newtimePollAckReceived",
    "newtimeRangeSent",
    "newtimeRangeReceived",
    "Test"
]

fig, axs = plt.subplots(len(time_diffs_1), 3, figsize=(12, 15))
axs[0, 0].set_title("Plot de X - newtimePollSent")
axs[0, 1].set_title("Plot de X - timeINO")
axs[-1,0].set_xlabel("iteration")
axs[-1,1].set_xlabel("iteration")
# Tracer les sous-graphiques
for i in range(len(time_diffs_1)):
    axs[i, 0].plot(it, time_diffs_1[i])
    axs[i, 1].plot(full_it, time_diffs_2[i])
    axs[i, 2].plot(full_it, time_diffs_3[i])
    axs[i, 0].set_ylabel(f"X = {variable_names[i]} [s]")

plt.tight_layout()
# plt.show()

plt.figure()
plt.scatter(it, (newtimeRangeSent - newtimePollSent), s = 1)
print(np.mean((newtimeRangeSent - newtimePollSent)))
plt.show()