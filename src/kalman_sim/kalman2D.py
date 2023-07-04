#!/usr/bin/python3
import os, sys
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(THIS_FOLDER, '../libraries'))
from sensor import noise_sensor
import toolbox_kalman as tool

import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys

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
# sawtooth = lambda x : (2*arctan(tan(x/2)))

max_ctrl_y = 0
max_ctrl_x = 0
L = 20
def control(x,t,nb=3,display=True):
    
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
    # u = ddy
    u1 = K*sawtooth((np.pi/2 - np.arctan2(w[1,0]-x2,w[0,0] - x1)) - x3)
    u = np.vstack((u1,u))



    if np.linalg.norm(u) > 500:
        sys.exit()

    if display:
        plt.scatter(w[0,0],w[1,0], color = 'red', label = 'point to follow')
        W = lambda f : np.array([L*np.cos(f*t), L*np.sin(nb*f*t)])
        plt.scatter(W(np.linspace(0,100,1100))[0],W(np.linspace(0,100,1100))[1], s = 0.1, label='trajectory to follow')

    return u 

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

# def random_noise(G, n_iter,sigma=0.00005):
#     n = len(G)
#     gaussian_vector = np.random.multivariate_normal(np.zeros(n), sigma*np.eye(*G.shape), size=n_iter+1)
#     random_noise = np.sum(gaussian_vector, axis = 0).reshape(-1,1)
#     return random_noise


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
def g(x, Xhat, t):
    global err, col
    x=x.flatten()
    wp_detected = False
    H = np.zeros((1,5))
    y = np.zeros((1,1))
    Beta = []; A = []
    for i in range(Wps.shape[1]):
        a=Wps[:,i].flatten() #wps(i) in (xi,yi)
        da = a-(x[0:2]).flatten()
        dist = np.linalg.norm(da)**2
        if np.sqrt(dist) < 10: #On considère qu'on a capté la balise
            
            plt.plot(np.array([a[0],x[0]]),np.array([a[1],x[1]]),"red",1)

            dist_hat = np.linalg.norm(a - (Xhat[0:2]).flatten())**2
            Hi = np.array([[-2*(a[0] - Xhat[0,0]), -2*(a[1] - Xhat[1,0]), 0, 0, 0]])
            yi = dist - dist_hat + Hi@Xhat 

            # Près au cm
            yi = int(yi[0,0]*100)/100

            # Ajout du bruit
            yi = noise_sensor(int(t/dt)+1, sigma_bb, sigma_rw, yi)[-1]

            if not wp_detected:
                H = Hi; y = yi; 
            else:
                H = np.vstack((H,Hi)); y = np.vstack((y,yi))

            Beta.append(np.sqrt(sigma_bb**2 + sigma_rw**2))
            wp_detected = True

    if not wp_detected: col.append('blue')
    else: col.append('red')

    Γβ = np.diag(Beta)
    # if len(Beta) != 0:
    #     y = y + noise_sensor(int(t/dt), sigma_bb, sigma_rw) #, mvnrnd(Γβ) + random_noise(Γβ, int(t/dt))
    
    return H, y, Γβ, wp_detected

def Kalman(xbar, P, u, y, Q, R, F, G, H):
    # Prédiction
    xbar = xbar + dt*f(xbar,u) #F @ xbar + G @ u
    P = F @ P @ F.T + G @ Q @ G.T

    # Correction
    ytilde = y - H @ xbar
    S = H @ P @ H.T + R
    inv_norm_S = scipy.linalg.sqrtm(np.linalg.inv(S))@ytilde

    K = P @ H.T @ np.linalg.inv(S)
    xbar = xbar + K @ ytilde
    P = P - K @ H @ P

    return xbar, P, ytilde, inv_norm_S

if __name__ == "__main__":
    global col
    col = []
    display_bot = 1
    UWB = 0
    GNSS = 1
    odometer = 0

    if display_bot:
        ax = tool.init_figure(-L*1.1, L*1.1, -L*1.1, L*1.1)
    T = []

    import sys
    from tqdm import tqdm
    N = 1000
    PMatrix = np.zeros((N,25))

    P = 10 * np.eye(5)
    X = np.array([[1], [0], [0], [0], [0]])
    Xhat = X

    sigma_bb = 0.01665937281279768
    sigma_rw = 0.00005
    sigm_equation = dt*0.1
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation])

    ERR = []
    YTILDE = []
    ytilde = np.array([[0],[0]])

    wp_detected = False
    
    
    sigm_equation = dt*0.01
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation])
    
    for t in tqdm(np.arange(0, N*dt, dt)):

        # Real state
        u = control(X,t)
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

        if UWB :
            Hk,Y,R,wp_detected = g(X, Xhat, t)
            if wp_detected and not GNSS:
                Xhat, P, ytilde, inv_norm_S = Kalman(Xhat, P, u, Y, Q, R, Fk, Gk, Hk)
            if not wp_detected and not GNSS and not odometer:
                Xhat = Xhat + dt*f(Xhat,u) + mvnrnd(Gk @ Q @ Gk.T)
                P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T

        if GNSS:
            if t%1==0: #each second we get a new value of GNSS data
                sigm_measure = 0.01
                R_gps = np.diag([sigm_measure, sigm_measure])

                Y_gps = np.array([[x], [y]])
                Hk_gps = np.array([[1, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0]])

                # Correction
                ytilde = Y_gps - Hk_gps @ Xhat
                S = Hk_gps @ P @ Hk_gps.T + R_gps
                inv_norm_S = scipy.linalg.sqrtm(np.linalg.inv(S))@ytilde

                K = P @ Hk_gps.T @ np.linalg.inv(S)
                Xhat = Xhat + K @ ytilde
                P = P - K @ Hk_gps @ P

            if not odometer:
                Xhat = Xhat + dt*f(Xhat,u)
                P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T

        if odometer:
            sigm_measure = 0.00001
            R_odo = np.diag([sigm_measure, sigm_measure])
            Y_odo = np.array([[vx], [vy]])
            Hk_odo = np.array([[0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 1]])

            # Correction
            ytilde = Y_odo - Hk_odo @ Xhat
            S = Hk_odo @ P @ Hk_odo.T + R_odo
            np.linalg.inv_np.linalg.norm_S = scipy.linalg.sqrtm(np.linalg.inv(S))@ytilde

            K = P @ Hk_odo.T @ np.linalg.inv(S)
            Xhat = Xhat + K @ ytilde
            P = P - K @ Hk_odo @ P

            Xhat = Xhat + dt*f(Xhat,u)
            P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T

        if display_bot:

        
            # Display the results
            tool.draw_tank(X)
            tool.draw_ellipse_cov(ax, Xhat[0:2], P[0:2, 0:2], 0.9, col='black')
            ax.scatter(Xhat[0, 0], Xhat[1, 0], color='green', label = 'Estimation of position', s = 5)
            ax.legend()

            if Wps.shape[0] != 0 and Wps.shape[1] != 0:
                ax.scatter(Wps[0], Wps[1], label = 'anchors UWB')

            plt.pause(0.001)

            tool.clear(ax)
            tool.legende(ax)

        # Append lists to visualize our covariance model
        T.append(t)
        t = int(t/dt)
        for j in range(5):
            for k in range(5):
                PMatrix[t,k+5*j] = P[j,k]
        
        ERR.append(np.linalg.norm(Xhat[0:2] - X[0:2]))
        YTILDE.append(np.linalg.norm(ytilde))

    print(max(PMatrix[:,0])) #x
    print(max(PMatrix[:,6])) #y

    
    def final_display():

            plt.close()
            plt.figure()
            plt.suptitle(f"P(t) Matrix")
            AX = []
            for i in range(5):
                for j in range(5):
                    ax = plt.subplot2grid((5, 5), (i, j))
                    ax.scatter(T,PMatrix[:,i+5*j],color='darkblue',s=1)
                    ax.set_xlabel("Time [s]")
                    # ax.set_ylabel("Error")
                    ax.set_title(f"P_{i},{j}")

            plt.figure()
            plt.suptitle("Get(UWB) : red; else : blue")
            ax = plt.subplot2grid((2, 1), (0, 0))
            if UWB:
                ax.scatter(T,ERR, color = np.array(col),s=1, label = "balise UWB détectée")
            else:
                ax.scatter(T,ERR, color = 'blue', s = 1, label = "pas de balise UWB détectée")
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Error [m]")
            ax.set_title("Error")

            ax1 = plt.subplot2grid((2, 1), (1, 0))
            ax1.scatter(T, YTILDE, color = np.array(col), s=1)
            ax1.set_title("||Ytilde||")
            ax1.set_xlabel("Time [s]")
            ax1.set_ylabel("||Ytilde|| [m]")
            plt.show()
    final_display()
