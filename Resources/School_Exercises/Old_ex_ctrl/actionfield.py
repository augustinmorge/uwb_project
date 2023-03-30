from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f(x):
    return -(x[0, 0] ** 2 + x[1, 0] ** 2 - 1) * x + array([[-x[1, 0]], [x[0, 0]]])


A1 = diag((1, -1))
A2 = diag((1, 0.5))
A3 = array([[cos(pi / 3), -sin(pi / 3)],
            [sin(pi / 3), cos(pi / 3)]]) @ A2


def f1(x):
    return A1 @ f(inv(A1) @ x)


def f2(x):
    return A2 @ f(inv(A2) @ x)


def f3(x):
    return A3 @ f(inv(A3) @ x)


def draw_field(f):
    X, Y, U, V = [], [], [], []
    for i in linspace(xmin, xmax, 20):
        for j in linspace(ymin, ymax, 20):
            x = array([[i], [j]])
            X.append(i)
            Y.append(j)
            U.append(f(x)[0, 0] / norm(f(x)))
            V.append(f(x)[1, 0] / norm(f(x)))
    quiver(X, Y, U, V)


def follow_field(f):
    x = array([[2.1], [2]])
    dt = 0.02
    for t in arange(0, 5, dt):
        ax.scatter(x[0, 0], x[1, 0], s=0.3, color='r')
        x = x + dt * f(x)


xmin, xmax, ymin, ymax = -2.5, 2.5, -2.5, 2.5

ax = init_figure(xmin, xmax, ymin, ymax)

draw_field(f)
follow_field(f)
pause(3)
clear(ax)
draw_field(f1)
follow_field(f1)
pause(3)
clear(ax)
draw_field(f2)
follow_field(f2)
pause(3)
clear(ax)
draw_field(f3)
follow_field(f3)
pause(3)

dt = 0.1
tmax = 3
x_tank = array([[1], [0], [1]])


def f_tank(x):
    vector = ft(x[0:2])
    direction = angle(vector)
    u = 5 * sawtooth(direction - x[2, 0])
    return array([[cos(x[2, 0])], [sin(x[2, 0])], [u]])


for t in arange(0, tmax, dt):
    clear(ax)
    A = diag((1 + (t / tmax), 1))


    def ft(x):
        return A @ f(inv(A) @ x)


    draw_field(ft)
    x_tank = x_tank + dt * f_tank(x_tank)
    draw_tank(x_tank, r=0.1)

for t in arange(0, tmax, dt):
    clear(ax)
    A = array([[cos(t), -sin(t)],
               [sin(t), cos(t)]]) @ diag((2, 1))


    def ft(x):
        return A @ f(inv(A) @ x)


    draw_field(ft)
    x_tank = x_tank + dt * f_tank(x_tank)
    draw_tank(x_tank, r=0.1)
