import matplotlib.pyplot as plt
import numpy as np
import sys, os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(THIS_FOLDER, '../libraries'))
from sensor import noise_sensor
import toolbox_kalman as tool

# List of waypoints

# Wps = np.array([[0, 10 , -10],
#               [0, 0, 0]])

Wps = np.array([[0, 10, -10, 0],
              [-10, 0, 0, 10]])

# Wps = np.array([[1],
#               [0]])

# Wps = np.array([[10000],
#               [1]])

# Wps = np.array([[]])

# a = -20
# b = 20
# N = 10
# Wps = np.random.uniform(low=a, high=b, size=(2, N))

def plot_covariance(PMatrix, T):
    """
    Fonction pour afficher la matrice de covariance P(t) au fil du temps
    """
    plt.figure()
    plt.suptitle(f"P(t) Matrix")
    for i in range(5):
        for j in range(5):
            ax = plt.subplot2grid((5, 5), (i, j))
            ax.scatter(T/60/60, PMatrix[:,i+5*j],color='darkblue',s=1)
            ax.set_xlabel("Hours [h]")
            ax.set_title(f"P_{i},{j}")

def plot_error(YTILDE, ERR, T, col, UWB):
    """
    Fonction pour afficher l'erreur et la norme de la mesure innovante
    """
    plt.figure()
    plt.suptitle("Get(UWB) : red; else : blue")
    ax = plt.subplot2grid((2, 1), (0, 0))
    if UWB:
        ax.scatter(T/60/60, ERR, color=np.array(col), s=1, label="balise UWB détectée")
    else:
        ax.scatter(T/60/60, ERR, color='blue', s=1, label="pas de balise UWB détectée")
    ax.set_xlabel("Hours [h]")
    ax.set_ylabel("Error [m]")
    ax.set_title("Error")
    ax.legend()

    ax1 = plt.subplot2grid((2, 1), (1, 0))
    ax1.scatter(T/60/60, YTILDE, color=np.array(col), s=1)
    ax1.set_xlabel("Hours [h]")
    ax1.set_ylabel("||Ytilde|| [m]")

def plot_noise(noise, Wps, T, tmax):
    """
    Fonction pour afficher les bruits de mesure pour chaque ancre UWB
    """
    fig, axs = plt.subplots(1, Wps.shape[1]);
    fig.suptitle("noise")
    T = np.linspace(0,tmax,tmax)
    for i in range(Wps.shape[1]):
        axs[i].set_xlabel("[h]")
        axs[i].set_ylabel("[m]")
        axs[i].scatter(T/60/60, noise[i], label=f"noise for anchor {i}", s=1)
        axs[i].legend()
    
i_ = 0
def display_results(X, Xhat, P, Wps, L, wp_detected = []):
    global i_, ax
    if i_ == 0:
        ax = tool.init_figure(-L*1.1, L*1.1, -L*1.1, L*1.1)
        i_ += 1
    # Affichage du tank
    tool.draw_tank(X)

    # Affichage de l'ellipse de covariance
    tool.draw_ellipse_cov(ax, Xhat[0:2], P[0:2, 0:2], 0.9, col='black')

    # Affichage de l'estimation de position
    ax.scatter(Xhat[0, 0], Xhat[1, 0], color='green', label='Estimation of position', s=5)

    # Affichage des points d'ancrage UWB
    if Wps.shape[0] != 0 and Wps.shape[1] != 0:
        ax.scatter(Wps[0], Wps[1], label='anchors UWB')

    for elem in wp_detected:
        ax.plot(np.array([elem[0],X[0,0]]),np.array([elem[1],X[1,0]]),"red",1)

    plt.pause(0.001)

    # Nettoyage de l'affichage
    tool.clear(ax)
    tool.legende(ax)

    
