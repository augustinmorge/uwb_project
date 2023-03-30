from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from math import atan, atan2

def f(x,u):
    θ=x[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])

x=array([[20],[-10],[4]])
dt= 0.1
a,b = array([[-30],[-4]]), array([[30],[6]])
ax=init_figure(-40,40,-40,40)
phi = atan2(b[1,0]-a[1,0], b[0,0]-a[0,0])
for t in arange(0,60,dt):
    clear(ax)
    draw_tank(x,'darkblue')
    plot2D(hstack((a,b)),'red')
    plot2D(a,'ro')
    plot2D(b,'ro')    
    
    m = x[0:2]
    if (b-a).T@(b-m)<0 :
        break
    e = det(hstack((b-a,m-a)))/norm(b-a)
    thetabar = phi - atan(e)
    u = atan(tan((thetabar - x[2,0])/2))
    
    x   = x+dt*f(x,u)
    
