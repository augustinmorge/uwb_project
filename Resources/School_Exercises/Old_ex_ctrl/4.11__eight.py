from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def φ0(p1,p2):        
    return -(p1**3+p2**2*p1-p1+p2),-(p2**3+p1**2*p2-p1-p2)

def phi(p1, p2): 
    D_ = inv(D)
    z1 = D_[0, 0] * (p1 - c1) + D_[0, 1] * (p2 - c2)
    z2 = D_[1, 0] * (p1 - c1) + D_[1, 1] * (p2 - c2)
    w1, w2 = φ0(z1, z2)
    v1 = D[0, 0] * w1 + D[0, 1] * w2
    v2 = D[1, 0] * w1 + D[1, 1] * w2
    return v1, v2

def Jphitheta(p):
    p1, p2 = p.flatten()
    return array( [[-3*p1**2 - p2**2 + 1, -2*p1*p2 - 1],
                   [-2*p1*p2 + 1, -3*p2**2 - p2**2 + 1]])

def dphi(x):
    p1, p2, theta = x.flatten()
    z = inv(D) @ array([[p1 - c1], [p2 - c2]])
    dv = D @ Jphitheta(z) @ inv(D) @ array([[cos(theta)], [sin(theta)]])
    return dv.flatten()

def f(x, u):
    theta = x[2, 0]
    return array([[cos(theta)], [sin(theta)], [u]])

def control(x):
    da, db = dphi(x)
    x1, x2, x3 = x.flatten()
    a, b = phi(x1, x2)
    u = -sawtooth(x3 - arctan2(b, a)) - (b * da - a * db) / (a ** 2 + b ** 2)
    return u


x = array([[-2], [-3], [1]])
dt, s = 0.1, 5
ax = init_figure(-s, s, -s, s)
draw_field(ax, φ0, -s, s, -s, s, 0.5)
ax.set_title("Champs de vecteur cercle")
pause(2)
q = 0
for t in arange(0, 40, dt):
    clear(ax)
    ax.set_title("Circuit en huit")
    if q == 0:
        c1, c2, r, eps = 2, 0, 2, 1
        draw_tank(x, "darkblue", 0.1, 2)
    if q == 1:
        c1, c2, r, eps = 2, 0, 2, 1
        draw_tank(x, "red", 0.1, 2)
    if q == 2:
        c1, c2, r, eps = -2, 0, 2, -1
        draw_tank(x, "green", 0.1, 2)
    if q == 3:
        c1, c2, r, eps = -2, 0, 2, -1
        draw_tank(x, "magenta", 0.1, 2)

    D = array([[r, 0], [0, r * eps]])
    x1, x2 = x[0:2].flatten()
    if ((q % 2 == 0) & (x2 > 0.5)) | ((q % 2 == 1) & (x2 < 0)):
        q = (q + 1) % 4 
    u = control(x)  
    x = x + dt * f(x, u)
    draw_field(ax, phi, -s, s, -s, s, 0.5)

    
    



