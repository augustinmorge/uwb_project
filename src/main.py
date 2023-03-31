from kalman import *

def main():
    u1, u2, u3 = u.flatten() ## TODO : Récupérer les données de la centrale pour wz, ax, ay
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

    Hk,Y,R,wp_detected = g(anchors, Xhat)
    if wp_detected:
        Xhat, P, ytilde, inv_norm_S = Kalman(Xhat, P, u, Y, Q, R, Fk, Gk, Hk)
    else:
        Xhat = Xhat + dt*f(Xhat,u) #+ tool.mvnrnd1(Gk @ Q @ Gk.T) #Fk @ Xhat + Gk @ u
        P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T

    if display_bot:
        # Display the results
        tool.draw_tank(X)
        tool.draw_ellipse_cov(ax, Xhat[0:2], P[0:2, 0:2], 0.9, col='black')
        ax.scatter(Xhat[0, 0], Xhat[1, 0], color='green', label = 'Estimation of position', s = 5)
        ax.legend()

        for id in anchors.keys():
            ax.scatter(anchors[id]['Coords'][0], anchors['Coords'][1], label = 'anchors UWB')

        plt.pause(0.001)

        tool.clear(ax)
        tool.legende(ax)

    # Change time step
    dt = time.time() - t0
    t0 = time.time()
        
if __name__ == "__main__":
    display_bot = 1

    L = 20
    if display_bot:
        ax = tool.init_figure(-L*1.1, L*1.1, -L*1.1, L*1.1)

    P = 10 * np.eye(5)
    X = np.array([[1], [0], [0], [0], [0]])

    wp_detected = False

    u = np.zeros((5,1))
    t0 = time.time()
    global dt
    dt = t0

    sigm_equation = dt*0.1
    Q = np.diag([sigm_equation, sigm_equation, sigm_equation])

    anchors = Anchor()

    while True:
        main()