import numpy as np
import sys, os
import matplotlib.pyplot as plt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def random_noise(G, n_iter,sigma=0.00005):
    n = len(G)
    gaussian_vector = np.random.default_rng().multivariate_normal(np.zeros(n), sigma*np.eye(*G.shape), size=n_iter+1)
    random_noise = np.sum(gaussian_vector, axis=0).reshape(-1,1)
    return random_noise

#Génération d'un vecteur gaussien
def mvnrnd(G, n_iter):
    noise = random_noise(G, n_iter, sigma=0.00005)
    err = np.cumsum(noise)
    return np.random.normal(loc=err, scale=np.sqrt(G[0, 0]), size=(1, len(noise)))



if __name__ == "__main__":
    T = []
    err = []
    from tqdm import tqdm
    N = 10000
    Γβ_1uwb = np.array([[0.01665937281279768]])
    for i in tqdm(range(N)):
        T.append(i)
        err.append((mvnrnd(Γβ_1uwb, i))[0]) # + random_noise(Γβ_1uwb, int(i)))[0])

    sys.path.insert(1, os.path.join(THIS_FOLDER, '../logs/log_long'))
    from display_long_log import plot_data
    plot_data(np.array([0]), np.array(T), np.array(err), np.array([]), with_dbm=False)
