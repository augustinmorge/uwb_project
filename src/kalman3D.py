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
    
    w=L*np.array([[np.cos(f*t)],[np.sin(f*nb*t)]])  
    dw=L*np.array([[-f*np.sin(f*t)],[nb*f*np.cos(f*nb*t)]])  
    ddw=L*np.array([[-f**2*np.cos(f*t)],[-nb**2*f**2*np.sin(f*nb*t)]])
    
    Ax = np.array([[np.cos(x3), np.sin(x3)],
                [np.sin(x3), -np.cos(x3)]])
    
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
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation])

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

        Fk = np.eye(9) + dt * np.array([[0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 1, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 1],
                                        [0, 0, -u2*np.sin(θ) + u3*np.cos(θ), 0, 0],
                                        [0, 0, u2*np.cos(θ) + u3*np.sin(θ), 0, 0]])
        
        Gk = dt * np.array([[0, 0, 0],
                            [0, 0, 0],
                            [1, 0, 0],
                            [0, np.cos(θ), np.sin(θ)],
                            [0, np.sin(θ), -np.cos(θ)]])


        if i%0==0: #each second we get a new value of GNSS data
            sigm_measure = 0.01
            R_gps = np.diag([sigm_measure, sigm_measure])

            Y_gps = np.array([[x], [y]]) #+ tool.mvnrnd1(R)
            Hk_gps = np.array([[1, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0]])
            
            Xhat, P, ytilde, inv_norm_S = Kalman(Xhat, P, u, Y_gps, Q, R_gps, Fk, Gk, Hk_gps)

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
        T.append(i)
        i = int(i/dt)
        for j in range(5):
            for k in range(5):
                PMatrix[i,k+5*j] = P[j,k]
        
        ERR.append(tool.norm(Xhat[0:2] - X[0:2]))
        YTILDE.append(tool.norm(ytilde))

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