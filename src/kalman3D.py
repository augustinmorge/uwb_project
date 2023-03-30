#!/usr/bin/python3
import toolbox_kalman as tool
import matplotlib.pyplot as plt
import numpy as np
import sys

global dt
dt = 0.1

def f(X, u):
    u1, u2, u3, u4, u5, u6 = u.flatten()
    x, y, z, φ, θ, ψ, vx, vy, vz = X.flatten()

    dp = np.array([[vx], [vy], [vz]])
    dv = tool.eulermat(np.pi/2-φ, θ, ψ)@np.array([[u1],[u2],[u3]])
    w = tool.eulerderivative(np.pi/2-φ,θ,ψ)@np.array([[u4], [u5], [u6]]) #Comme le 0 est au nord et tourne dans le sens anti-trigo

    x_dot = np.vstack((dp, w, dv))
    return x_dot

# sawtooth = lambda x : (2*arctan(tan(x/2)))

L = 20
def control(x,t,nb=3,display=True):

    x1, x2, x3, x4, x5 = x.flatten()

    K = 1
    f = 0.1

    w=L*np.array([[np.cos(f*t)],[np.sin(f*nb*t)],[np.sin(f*nb*t + np.pi/4)]])
    dw=L*np.array([[-f*np.sin(f*t)],[nb*f*np.cos(f*nb*t)], [f*nb*np.cos(f*nb*t + np.pi/4)]])
    ddw=L*np.array([[-f**2*np.cos(f*t)],[-nb**2*f**2*np.sin(f*nb*t)], [-(f*nb)**2*np.sin(f*nb*t + np.pi/4)]])

    Ak = tool.eulermat(np.pi/2 - φ, θ, ψ)

    y = np.array([[x1],
               [x2]])

    dy = np.array([[x4],
                [x5]])

    ddy = w-y + 2*(dw-dy) + ddw

    u = np.linalg.inv(Ax)@ddy
    # u = ddy
    u1 = K*tool.sawtooth((np.pi/2 - np.arctan2(w[1,0]-x2,w[0,0] - x1)) - x3)
    u = np.vstack((u1,u))



    if tool.norm(u) > 500:
        sys.exit()

    if display:
        plt.scatter(w[0,0],w[1,0], color = 'red', label = 'point to follow')
        W = lambda f : np.array([L*np.cos(f*t), L*np.sin(nb*f*t)])
        plt.scatter(W(np.linspace(0,100,1100))[0],W(np.linspace(0,100,1100))[1], s = 0.1, label='trajectory to follow')

    return u


def Kalman(xbar, P, u, y, Q, R, F, G, H, all = True):
    # Prédiction
    xbar = xbar + dt*f(xbar,u) #F @ xbar + G @ u
    P = F @ P @ F.T + G @ Q @ G.T

    if all:
        # Correction
        ytilde = y - H @ xbar
        S = H @ P @ H.T + R
        inv_norm_S = tool.sqrtm(np.linalg.inv(S))@ytilde

        K = P @ H.T @ np.linalg.inv(S)
        xbar = xbar + K @ ytilde
        P = P - K @ H @ P

        return xbar, P #, ytilde, inv_norm_S

    else:
        return xbar, P


if __name__ == "__main__":
    global col
    col = []
    display_bot = 0
    GNSS = 0

    if display_bot:
        ax = tool.init_figure(-L*1.1, L*1.1, -L*1.1, L*1.1)
    T = []

    import sys
    from tqdm import tqdm
    N = 1000
    PMatrix = np.zeros((N,9**2))

    P = 10 * np.eye(9)
    X = np.array([[0.1], [0.2], [0.3], [0], [0], [0], [0], [0], [0]])
    Xhat = X

    sigm_equation = 0 #dt*0.1
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation, sigm_equation, sigm_equation, sigm_equation])

    ERR = []
    YTILDE = []
    ytilde = np.array([[0],[0]])

    wp_detected = False

    for i in tqdm(np.arange(0, N*dt, dt)):
        # Real state
        # u = control(X,i)
        u = np.zeros((6,1))
        X = X + dt*f(X,u)

        u1, u2, u3, u4, u5, u6 = u.flatten()
        x, y, z, φ, θ, ψ, vx, vy, vz = X.flatten()

        CBE = tool.eulermat(np.pi/2 - φ, θ, ψ)
        DBE = tool.eulerderivative(np.pi/2 - φ, θ, ψ)
        gamma_matrix = np.vstack((np.zeros((6,3)), DBE))
        v_matrix = np.vstack((np.eye(3), np.zeros((6,3))))

        Fk = np.eye(9) + dt * np.hstack((np.zeros((9,3)), gamma_matrix, v_matrix))

        IO = np.hstack((np.eye(3), np.zeros((3,3))))
        OCBE = np.hstack((np.zeros((3,3)), CBE))
        Gk = dt * np.vstack((np.zeros((3,6)),\
                             IO,\
                             OCBE))

        sigm_measure = 0.01
        R_gps = np.diag([sigm_measure, sigm_measure, sigm_measure])

        Y_gps = np.array([[x], [y], [z]]) #+ tool.mvnrnd1(R)
        Hk_gps = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0, 0]])

        if i%10 == 0:
            Xhat, P = Kalman(Xhat, P, u, Y_gps, Q, R_gps, Fk, Gk, True)
        else:
            Xhat, P = Kalman(Xhat, P, u, Y_gps, Q, R_gps, Fk, Gk, False)
