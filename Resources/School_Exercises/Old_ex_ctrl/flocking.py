from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


class Robot:
    def __init__(self):
        self.x = 20 * randn(3, 1)
        self.is_leader = False

    def update(self, u):
        θ = self.x[2, 0]
        f = array([[cos(θ)], [sin(θ)], [u]])
        self.x = self.x + dt * f

    def draw(self):
        if self.is_leader:
            draw_tank(self.x, 'r')
        else:
            draw_tank(self.x, 'b')

    def vector_to_follow(self, robots):
        alignement = zeros((2, 1))
        separation = zeros((2, 1))
        cohesion = zeros((2, 1))
        for robot in robots:
            if robot is not self:
                coeff = (1, 1, 1)
                if robot.is_leader:
                    coeff = (1, 5, 3)
                alignement += coeff[0] * array([[cos(robot.x[2, 0])],
                                                [sin(robot.x[2, 0])]])
                cohesion += -coeff[1] * 2 * (self.x[0:2] - robot.x[0:2])
                if norm(self.x[0:2] - robot.x[0:2]) < 10:
                    separation += coeff[2] * (self.x[0:2] - robot.x[0:2]) / (norm(self.x[0:2] - robot.x[0:2]) ** 2)

        if separation.any() != 0:
            separation /= norm(separation)
        if cohesion.any() != 0:
            cohesion /= norm(cohesion)
        if alignement.any() != 0:
            alignement /= norm(alignement)

        vector = alignement + cohesion + separation

        if self.is_leader:
            A = diag((20, 20))
            t = inv(A) @ self.x[0:2]
            t = -(t[0, 0] ** 2 + t[1, 0] ** 2 - 1) * t + array([[-t[1, 0]], [t[0, 0]]])
            circle = A @ t
            vector += 2 * circle / norm(circle)

        return vector / norm(vector)

    def control(self, robots):
        vector_to_follow = self.vector_to_follow(robots)
        direction = angle(vector_to_follow)
        u = sawtooth(direction - self.x[2, 0])
        return u


ax = init_figure(-60, 60, -60, 60)
m = 20
robots = []
for i in range(m):
    robots.append(Robot())
robots[0].is_leader = True
dt = 0.2

for t in arange(0, 100, dt):
    clear(ax)
    for robot in robots:
        robot.draw()
        u = robot.control(robots)
        robot.update(u)
