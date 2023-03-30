from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from math import atan, atan2

def f(x,u):
    x = x.flatten()
    return array([[5*cos(x[2])],[5*sin(x[2])],[u]])

def control_u(x):
    x1, x2, x3 = x.flatten()
    alpha = atan2(x2,x1)
    phi = pi + x3 - alpha
    if cos(phi) < 1/sqrt(2) :
        u = 1
    else :
        u = -sin(phi)
    return u
    
def go(x,col):
    for t in arange(0,15,dt):
        clear(ax)
        draw_disk(array([[0],[0]]),10,ax,'cyan')
        u = control_u(x)
        draw_tank(x, col)
        x = x+dt*f(x,u)      
    
x = array([[15],[20],[1]])
dt   = 0.1
ax=init_figure(-30,30,-30,30)
go(x,'red')
color = ['black','green','yellow']

for i in range(3):
    go(randn(3,1)*10,color[i])
