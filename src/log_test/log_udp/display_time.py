import numpy as np
import matplotlib.pyplot as plt
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# Charger les données depuis le fichier CSV
# data = np.genfromtxt(f'{THIS_FOLDER}/save_times.csv', delimiter=';', skip_header=1, dtype=str)
# data[:,1] = np.float(data[:,1])

data = np.genfromtxt(f'{THIS_FOLDER}/save_times_ms2.csv', delimiter=';', skip_header=1, dtype='str')
print(data)
# Extraire les colonnes pertinentes
names = data[:, 0]
values = data[:, 1].astype(float)

# Trouver les indices correspondant aux noms des colonnes
timeINO_indices = np.where(names == 'timeINO')[0]
timeRangeSent_indices = np.where(names == 'timeRangeSent')[0]
timePollSent_indices = np.where(names == 'timePollSent')[0]
timePollAckReceived_indices = np.where(names == 'timePollAckReceived')[0]

# Extraire les valeurs correspondantes aux indices trouvés
timeINO = values[timeINO_indices]*10**(-3)
timeRangeSent = values[timeRangeSent_indices]*10**(-6)
timePollSent = values[timePollSent_indices]*10**(-6)
# timePollAckReceived = values[timePollAckReceived_indices]

#Start from 0
# timeINO -= (timeINO[0] - timePollSent[0])
# timePollSent += timeINO[0]
# timeRangeSent += timeINO[0]
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

#Transforme les dents de scie en fonction linéaire
timestamp = 1099511627775  # Valeur du timestamp
timeoverflow = 1099511627776
timeres = 0.000015650040064103
offset = (timestamp % timeoverflow) * timeres * 10 ** (-6)

k = 0
newtimeRangeSent = np.zeros(timeRangeSent.shape)
newtimeRangeSent[0] = timeRangeSent[0]
for i in range(1, timeRangeSent.shape[0]):
    if timeRangeSent[i] < timeRangeSent[i - 1]:
        k += 1
    newtimeRangeSent[i] = k * offset + timeRangeSent[i]

k = 0
newtimePollSent = np.zeros(timePollSent.shape)
newtimePollSent[0] = timePollSent[0]
for i in range(1, timePollSent.shape[0]):
    if timePollSent[i] < timePollSent[i - 1]:
        k += 1

    newtimePollSent[i] = k * offset + timePollSent[i]

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

it_rs = [i for i in range(newtimeRangeSent.shape[0])]
it_ps = [i for i in range(newtimePollSent.shape[0])]
it_ino = [i for i in range(timeINO.shape[0])]
fig, ax = plt.subplots()
plot_polynomial_regression(ax, it_rs, newtimeRangeSent,[1],"newtimeRangeSent")
plot_polynomial_regression(ax, it_ps, newtimePollSent,[1],"newtimePollSent")
plot_polynomial_regression(ax, it_ino, timeINO,[1],"timeINO")
ax.set_xlabel("it")
ax.set_ylabel("time [s]")

# Calculer la différence newtimeRangeSent
timeRangeDiff = np.diff(newtimeRangeSent)
timeINODiff = np.diff(timeINO)
timePollDiff = np.diff(newtimePollSent)

plt.figure()
plt.scatter(it_rs[:-1], timeRangeDiff, s = 1, label = 'diff newtimeRangeSent [s]')
plt.scatter(it_ps[:-1], timePollDiff, s = 1, label = 'diff newtimePollSent [s]')
plt.scatter(it_ino[:-1], timeINODiff, s = 1, label = 'diff timeINO [s]')
plt.xlabel("it")
plt.ylabel("time")
plt.legend()
plt.show()

print("Résultats : ")
print(f"Intervalle de temps pour une boucle : {np.mean(timePollSent)}")