from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f_circle(x):
    return -(x[0, 0] ** 2 + x[1, 0] ** 2 - 1) * x + array([[-x[1, 0]], [x[0, 0]]])


A1 = diag((2, 2))
A2 = diag((2, -2))


def f1(x):
    return A1 @ f_circle(inv(A1) @ x + array([[-1], [0]]))


def f2(x):
    return A2 @ f_circle(inv(A2) @ x + array([[1], [0]]))


def draw_field(f):
    X, Y, U, V = [], [], [], []
    for i in linspace(-s, s, 20):
        for j in linspace(-s, s, 20):
            x = array([[i], [j]])
            X.append(i)
            Y.append(j)
            U.append(f(x)[0, 0] / norm(f(x)))
            V.append(f(x)[1, 0] / norm(f(x)))
    quiver(X, Y, U, V)


def f_tank(x, f):
    vector = f(x[0:2])
    direction = angle(vector)
    u = 5 * sawtooth(direction - x[2, 0])
    return array([[cos(x[2, 0])], [sin(x[2, 0])], [u]])


Goals = [array([[0], [0]]), array([[-4], [0]]), array([[0], [0]]), array([[4], [0]])]
Fields = [f1, f2, f2, f1]
i = 0

x_tank = array([[0], [-3], [1]])
dt, s = 0.1, 5
ax = init_figure(-s, s, -s, s)
# States :
# State 1 : Going to (0, 0) on right vector field (f1)
# State 2 : Going to (-4, 0) on left vector field (f2)
# State 3 : Going to (0, 0) on left vector field (f2)
# State 4 : Going to (4, 0) on right vector field (f1)
for t in arange(0, 30, dt):
    if norm(Goals[i] - x_tank[0:2]) < 0.5:
        i += 1
        i %= 4
    x_tank = x_tank + dt * f_tank(x_tank, Fields[i])
    clear(ax)
    draw_tank(x_tank, r=0.1)
    draw_field(Fields[i])
    draw_disk(ax, Goals[i], 0.5, "red", 0.5)
    pause(0.0001)

pause(2)
