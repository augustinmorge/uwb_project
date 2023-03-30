from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


class Robot:
    def __init__(self, a):
        self.x = array([[a], [1]])

    def move(self, u):
        self.x = self.x + dt * array([[self.x[1, 0]], [u]])

    def draw(self, col):
        θ = self.x[0, 0] / r
        a = array([[r * cos(θ)], [r * sin(θ)], [θ + pi / 2]])
        draw_tank(a, col)

    def g(self, robots):
        i = robots.index(self)
        pred = robots[(i + 1) % m]
        return array([[(pred.x[0, 0] - self.x[0, 0]) % L], [pred.x[1, 0] - self.x[1, 0]]])

    def control(self, robots):
        y = self.g(robots)
        u = 5 * (v0 - self.x[1, 0]) - y[1, 0] - (L/m - y[0, 0])
        return u


L = 150
r = L / (2 * pi)

ax = init_figure(-(r + 5), (r + 5), -(r + 5), (r + 5))
dt = 0.05

m = 5
v0 = 10

robots = []
for i in range(m):
    robots.append(Robot(7 * i))

for t in arange(0, 100, dt):
    clear(ax)
    draw_disk(ax, array([[0], [0]]), r + 3, 'lightblue')
    draw_disk(ax, array([[0], [0]]), r - 3, 'white')
    for robot in robots:
        u = robot.control(robots)
        robot.move(u)
        robot.draw('black')
    pause(0.001)
pause(5)
