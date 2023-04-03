from kalman import *

def main(X,u):
    global anchors
    anchors = anchors.anchors
    global dt, P, Q
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

    Hk,Y,R,wp_detected = g(anchors, X)
    
    if wp_detected:
        X, P, ytilde, inv_norm_S = Kalman(X, P, u, Y, Q, R, Fk, Gk, Hk, dt)
    else:
        X = X + dt*f(X,u) #+ tool.mvnrnd1(Gk @ Q @ Gk.T) #Fk @ X + Gk @ u
        P = Fk @ P @ Fk.T + Gk @ Q @ Gk.T

    if display_bot:
        # Display the results
        tool.draw_tank(X)
        tool.draw_ellipse_cov(ax, X[0:2], P[0:2, 0:2], 0.9, col='black')
        ax.scatter(X[0, 0], X[1, 0], color='green', label = 'Estimation of position', s = 5)
        ax.legend()

        for id in anchors.keys():
            try:
                ax.scatter(anchors[id]['Coords'][0], anchors['Coords'][1], label = 'anchors UWB')
            except:
                pass

        plt.pause(0.001)

        tool.clear(ax)
        tool.legende(ax)
    
        
if __name__ == "__main__":
    display_bot = 1

    L = 20
    if display_bot:
        ax = tool.init_figure(-L*1.1, L*1.1, -L*1.1, L*1.1)

    P = 10 * np.eye(5)
    X = np.array([[1], [0], [0], [0], [0]])

    wp_detected = False

    u = np.zeros((3,1))
    t0 = time.time()
    global dt
    dt = t0

    

    print("Everything working.. Starting the main program in 5.."); time.sleep(1)
    print("..4.."); time.sleep(1); print("..3..");time.sleep(1); print("..2..");time.sleep(1)
    print("..1");time.sleep(1)
    while True:
        sigm_equation = dt*0.1
        Q = np.diag([sigm_equation, sigm_equation, sigm_equation])
        # Change time step
        t0 = time.time()
        mutex.acquire()
        main(X,u)
        mutex.release()
        dt = time.time() - t0
        time.sleep(0.5)