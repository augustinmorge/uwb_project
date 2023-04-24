#!/usr/bin/python3
import os, sys
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(THIS_FOLDER, '../libraries'))
from sensor import noise_sensor
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys
from toolbox import *
import sys, time
from tqdm import tqdm

global dt
dt = 0.1

def f(X, u):
    
    u1, u2, u3 = u.flatten()
    x, y, θ, vx, vy = X.flatten()
    x_dot = np.array([[vx],
                      [vy],
                      [u1],
                      [u2*np.sin(θ) - u3*np.cos(θ)],
                      [u2*np.cos(θ) + u3*np.sin(θ)]])
    return x_dot

def sawtooth(x):
    return (x+np.pi)%(2*np.pi)-np.pi   # or equivalently   2*arctan(tan(x/2))

max_ctrl_y = 0
max_ctrl_x = 0
L = 20
def control(x,t,nb=3):
    
    x1, x2, x3, x4, x5 = x.flatten()
    
    K = 1
    f = 0.1
    
    w=L*np.array([[np.cos(f*t)],[np.sin(f*nb*t)]])  
    dw=L*np.array([[-f*np.sin(f*t)],[nb*f*np.cos(f*nb*t)]])  
    ddw=L*np.array([[-f**2*np.cos(f*t)],[-nb**2*f**2*np.sin(f*nb*t)]])
    
    Ax = np.array([[np.sin(x3), -np.cos(x3)],
                [np.cos(x3), np.sin(x3)]])
    
    y = np.array([[x1],
               [x2]])
    
    dy = np.array([[x4],
                [x5]])
    
    ddy = w-y + 2*(dw-dy) + ddw
    
    u = np.linalg.inv(Ax)@ddy
    u1 = K*sawtooth((np.pi/2 - np.arctan2(w[1,0]-x2,w[0,0] - x1)) - x3)
    u = np.vstack((u1,u))

    # if display:
    #     plt.scatter(w[0,0],w[1,0], color = 'red', label = 'point to follow')
    #     W = lambda f : np.array([L*np.cos(f*t), L*np.sin(nb*f*t)])
    #     plt.scatter(W(np.linspace(0,100,1100))[0],W(np.linspace(0,100,1100))[1], s = 0.1, label='trajectory to follow')
    #     plt.clf()

    return u 

# #Génération d'un vecteur gaussien
def mvnrnd(G):
    n = len(G)
    if n == 0:
        return np.zeros((0, 1))
    elif n == 1:
        return np.random.normal(scale=np.sqrt(G[0, 0]), size=(1, 1))
    else:
        y = np.random.multivariate_normal(np.zeros(n), G)
        return y.reshape(n, 1)
    
# Observation function
def g(x, Xhat, t, L_detect = 20):
    global err, col
    x=x.flatten()
    wp_detected = []
    H = np.zeros((1,5))
    y = np.zeros((1,1))
    Beta = []; A = []
    for i in range(Wps.shape[1]):
        a=Wps[:,i].flatten() #wps(i) in (xi,yi)
        da = a-(x[0:2]).flatten()

        #On aquière la distance
        dist = np.linalg.norm(da)
        
        #Cette distance est bruitée
        dist += noise[i][int(t)]

        #Cette distance est au cm
        dist = int(dist*100)/100

        if dist < L_detect and t%1 == 0: #On considère qu'on a capté la balise
            
            dist_hat = np.linalg.norm(a - (Xhat[0:2]).flatten())
            Hi = -np.array([[(a[0] - Xhat[0,0])/dist_hat, (a[1] - Xhat[1,0])/dist_hat, 0, 0, 0]])
            yi = dist - dist_hat + Hi@Xhat 

            if not wp_detected:
                H = Hi; y = yi; 
            else:
                H = np.vstack((H,Hi)); y = np.vstack((y,yi))

            # Beta.append(noise[i][int(t)])
            Beta.append(np.sqrt(sigma_bb**2))
            wp_detected.append(a)

    col.append('red' if wp_detected else 'blue')

    R = np.diag(Beta)
    return H, y, R, wp_detected

def Kalman(xbar, P, u, y, Q, R, F, G, H):
    # Prédiction
    xbar = xbar + dt*f(xbar,u)
    P = F @ P @ F.T + G @ Q @ G.T

    # Correction
    ytilde = y - H @ xbar
    S = H @ P @ H.T + R
    innov_norm = scipy.linalg.sqrtm(np.linalg.inv(S))@ytilde

    K = P @ H.T @ np.linalg.inv(S)
    xbar = xbar + K @ ytilde
    P = P - K @ H @ P

    return xbar, P, innov_norm

if __name__ == "__main__":
    display_bot = 0

    display_allan = 1
    display_dbm = 0
    display_quality = 1

    UWB = 1
    # Size of simu
    day = 0.1
    tmax = int(day*24*60*60)
    T = np.arange(0, tmax, dt)
    N = len(T)

    # Variables for Kalman
    P = 100 * np.eye(5)

    X = np.array([[0.], [0.], [0.], [0.], [0.]])
    Xhat = X

    sigma_bb = 0.05
    sigma_rw = 0.0001
    noise = [noise_sensor(tmax, sigma_bb, sigma_rw) for _ in range(Wps.shape[1])]

    ytilde = np.array([[0],[0]])

    sigm_equation = sigma_rw
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation])

    #Lists to display results

    col = []; ERR = []
    INNOV_NORM = []
    PMatrix = np.zeros((N,25))
    
    for t in tqdm(T):
        u = control(X,t)
        # u = np.array([[0],[0],[0]])

        X = X + dt*f(X,u)
        
        u1, u2, u3 = u.flatten()
        x, y, θ, vx, vy = X.flatten()

        Fk = np.eye(5) + dt * np.array([[0, 0, 0, 1, 0],
                                        [0, 0, 0, 0, 1],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, u2*np.cos(θ) + u3*np.sin(θ), 0, 0],
                                        [0, 0, -u2*np.sin(θ) + u3*np.cos(θ), 0, 0]])
        
        Gk = dt * np.array([[0, 0, 0],
                            [0, 0, 0],
                            [1, 0, 0],
                            [0, np.sin(θ), -np.cos(θ)],
                            [0, np.cos(θ), np.sin(θ)]])
        
        Hk,Y,R,wp_detected = g(X, Xhat, t)

        if wp_detected :
            Xhat, P, innov_norm = Kalman(Xhat, P, u, Y, Q, R, Fk, Gk, Hk)
            INNOV_NORM.append(innov_norm[0,0])
        else:
            Xhat = Xhat + dt*f(Xhat,u)
            P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T
            INNOV_NORM.append(None)

        if display_bot: display_results(X, Xhat, P, Wps, L, wp_detected)

        # Variables to visualize
        PMatrix[int(t/dt),:] = np.ravel(P)
        ERR.append(np.linalg.norm(Xhat[0:2] - X[0:2]))

    
    plt.close()
    # plot_noise(noise, Wps, T, tmax)
    # plot_covariance(PMatrix, T)
    plot_error(INNOV_NORM, ERR, T, col, UWB)

    sys.path.insert(1, os.path.join(THIS_FOLDER, '../logs/log_long'))
    from display_long_log import plot_data

    INNOV_NORM = np.array(INNOV_NORM)
    # Enlever les valeurs 'None' dans INNOV_NORM et les indices correspondants dans T
    indices = [i for i, x in enumerate(INNOV_NORM) if x is None]
    INNOV_NORM = np.delete(INNOV_NORM, indices)
    T = np.delete(T, indices)

    plot_data(np.array([0]), T, INNOV_NORM, np.array([]), False, np.array([]), np.array([]), False, sigma_rw, display_allan, display_dbm, display_quality)
    plt.show()