import numpy as np
import sys, os
import matplotlib.pyplot as plt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
import numpy as np

def noise_sensor(n, sigma_bb, sigma_rw):#, measure = np.random.randint(0,10)):
    """Simule les mesures d'un capteur avec bruit blanc et random walk
    
    Args:
    n (int): nombre de mesures
    sigma_bb (float): écart type du bruit blanc
    sigma_rw (float): écart type du random walk
    
    Returns:
    numpy.array: vecteur des mesures simulées
    """
    
    # génération du bruit blanc
    bb = np.random.normal(scale=sigma_bb, size=n)
    
    # génération du random walk
    rw = np.zeros(n)
    for i in range(1, n):
        rw[i] = rw[i-1] + np.random.normal(scale=sigma_rw)
        
    return bb + rw


if __name__ == "__main__":
    # paramètres du capteur
    sigma_bb = 0.05
    sigma_rw = 0.00015

    # nombre de mesures
    nb_j = 1
    N = int(nb_j*24*60*60)

    # simulation du capteur 
    # mesures = noise_sensor(N, sigma_bb, sigma_rw)
    mesures = np.floor((1 + noise_sensor(N, sigma_bb, sigma_rw))*1000)/1000

    T = np.linspace(0,N,N)

    sys.path.insert(1, os.path.join(THIS_FOLDER, '../logs/log_long'))
    from display_long_log import plot_data
    plot_data(np.array([0]), T, np.array(mesures), np.array([]), False, np.array([]), np.array([]), False)
    plt.show()