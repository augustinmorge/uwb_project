#https://www.ensta-bretagne.fr/jaulin/robmooc.html
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

        
def h(x,y):
    return 2*exp(-((x+2)**2+(y+2)**2)/10) + 2*exp(-((x-2)**2+(y-2)**2)/10) - 10


def draw_mesh():
    Mx=arange(-L,L,1.5)
    X,Y = meshgrid(Mx,Mx)
    H = h(X,Y)
    #ax.plot_surface(X,Y,H)
    ax.contour(X,Y,H)
    
    
def gradh(x, y):
    delta = 0.1
    return array([(h(x+delta, y)-h(x, y))/delta, (h(x, y+delta)-h(x, y))/delta])

def f(x, u):
    x, u = x.flatten(), u.flatten()
    psy = x[3]
    return array([[cos(psy)], [sin(psy)], [u[0]], [u[1]]])


def g(x):
    x = x.flatten()
    psy = x[3]
    return array([[x[2]-h(x[0], x[1])], [angle(gradh(x[0], x[1]))-psy], [-x[2]]])


def control(y):
    y = y.flatten()
    y3_bar = 2
    u1 = 0.5*(y[2]-y3_bar)
    h0 = -9
    u2 = tanh(-h0-y[2]-y[0])+sawtooth(y[1]+pi/2)
    return array([[u1], [u2]])

ax = Axes3D(figure())
x    = array([[2,-1,-1,0]]).T #x,y,z,ψ
L=10 #size of the world
dt = 0.1

for t in arange(0, 15, dt):
    y = g(x)
    u = control(y)
    x = x+dt*f(x, u)
    
    clean3D(ax,-L,L,-L,L,-L,0)
    draw_mesh()
    draw_robot3D(ax, x[0:3], eulermat(0, 0, x[3, 0]), 'blue', 0.1)
    x_sf = array([x[0], x[1], h(x[0], x[1])])
    draw_robot3D(ax, x_sf, eulermat(0, 0, x[3, 0]), 'black', 0.1)
    
    pause(0.01)


