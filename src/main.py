from kalman import *

def main(X,u):
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
        tool.draw_tank(X,col='darkblue',r=0.1) #,w=2)
        tool.draw_ellipse_cov(ax, X[0:2], P[0:2, 0:2], 0.9, col='black')
        ax.scatter(X[0, 0], X[1, 0], color='green', label = 'Estimation of position', s = 5)
        ax.legend()
        ids = anchors.anchors.keys()
        for id in ids:
            try:
                ax.scatter(anchors.anchors[id]['Coords'][0], anchors.anchors['Coords'][1], label = 'anchors UWB')
            except:
                pass

        plt.pause(0.001)

        tool.clear(ax)
        tool.legende(ax)
    
        
if __name__ == "__main__":

    # Start the threads
    anchors = Anchor()

    data, addr = connect_to_tag()

    # # Create a thread that runs the get_data function
    # get_data_thread = lambda : get_data(anchors, data)
    # t_get_data = threading.Thread(target=get_data)

    # # Start the thread
    # t_get_data.start()

    # Create a thread that runs the get_data function
    get_data_thread = threading.Thread(target=get_data, args=(anchors,data,))

    # Start the thread
    get_data_thread.start()

    # Start the display
    display_bot = 1

    L = 20
    if display_bot:
        ax = tool.init_figure(-5, 5, -5, 5)

    P = 10 * np.eye(5)
    X = np.array([[1], [0], [0], [0], [0]])

    wp_detected = False

    u = np.zeros((3,1))
    dt = 0.1

    while True:
        sigm_equation = dt*0.1
        Q = np.diag([sigm_equation, sigm_equation, sigm_equation])
        # Change time step
        t0 = time.time()
        main(X,u)
        dt = time.time() - t0