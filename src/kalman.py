#!/usr/bin/python3
import libraries.toolbox_kalman as tool

import matplotlib.pyplot as plt
import numpy as np
import sys, time
from get_data import *

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
    for id in anchors.keys():
        time, dist = anchors[id]['Time'], anchors[id]['Range']
        a = anchors[id]['Coords']
        wp_detected = True
        plt.plot(np.array([a[0],x[0]]),np.array([a[1],x[1]]),"red",1)

        dist_hat = np.linalg.norm(a - (x[0:2]).flatten())**2
        Hi = np.array([[-2*(a[0] - Xhat[0,0]), -2*(a[1] - Xhat[1,0]), 0, 0, 0]])
        yi = dist - dist_hat + Hi@Xhat

        if not wp_detected:
            H = Hi; y = yi; 
        else:
            H = np.vstack((H,Hi)); y = np.vstack((y,yi))

        Beta.append(0.1)

    R = np.diag(Beta)
    if len(Beta) != 0:
        y = y + tool.mvnrnd1(R)
    
    return H, y, R, wp_detected

def Kalman(xbar, P, u, y, Q, R, F, G, H):
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