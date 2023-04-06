#!/usr/bin/python3
import libraries.toolbox_kalman as tool

import matplotlib.pyplot as plt
import numpy as np
import sys, time
from get_data import *

def sawtooth(x):
    return (x+np.pi)%(2*np.pi)-np.pi   # or equivalently   2*arctan(tan(x/2))

def mvnrnd(G):
    n = len(G)
    if n == 0:
        return np.zeros((0, 1))
    elif n == 1:
        return np.random.normal(scale=np.sqrt(G[0, 0]), size=(1, 1))
    else:
        y = np.random.multivariate_normal(np.zeros(n), G)
        return y.reshape(n, 1)

def f(X, u):
    
    u1, u2, u3 = u.flatten()
    x, y, θ, vx, vy = X.flatten()
    x_dot = np.array([[vx],
                      [vy],
                      [u1],
                      [u2*np.sin(θ) - u3*np.cos(θ)],
                      [u2*np.cos(θ) + u3*np.sin(θ)]])
    return x_dot


# Observation function
def g(anchors, x):
    wp_detected = False
    H = np.zeros((1,5))
    y = np.zeros((1,1))
    Beta = []
    mutex.acquire()
    ids = anchors.anchors.keys()
    mutex.release()
    for id in ids:
        mutex.acquire()
        dist = anchors.anchors[id]['Range']
        a = anchors.anchors[id]['Coords']
        mutex.release()
        
        plt.plot(np.array([a[0],x[0,0]]),np.array([a[1],x[1,0]]),"red",1)

        dist_hat = np.linalg.norm(a - (x[0:2]).flatten())
        Hi = np.array([[-2*(a[0] - x[0,0]), -2*(a[1] - x[1,0]), 0, 0, 0]])
        yi = dist**2 - dist_hat**2 + Hi@x

        if not wp_detected:
            H = Hi; y = yi; 
        else:
            H = np.vstack((H,Hi)); y = np.vstack((y,yi))

        wp_detected = True
        Beta.append(0.1)
    R = np.diag(Beta)
    if len(Beta) != 0:
        y = y + mvnrnd(R)
    
    return H, y, R, wp_detected

def Kalman(xbar, P, u, y, Q, R, F, G, H, dt=0.1):
    # Prédiction
    xbar = xbar + dt*f(xbar,u) #F @ xbar + G @ u
    P = F @ P @ F.T + G @ Q @ G.T

    # Correction
    ytilde = y - H @ xbar
    S = H @ P @ H.T + R
    inv_norm_S = tool.sqrtm(np.linalg.inv(S))@ytilde

    K = P @ H.T @ np.linalg.inv(S)
    xbar = xbar + K @ ytilde
    P = P - K @ H @ P

    return xbar, P, ytilde, inv_norm_S