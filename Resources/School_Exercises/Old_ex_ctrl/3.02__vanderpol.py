from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def vdp(x1,x2):  
    return x2,-(0.01*(x1**2)-1)*x2-x1
    
    
def f(x,u):
    mx, my, θ, v, δ = x.flatten()
    u1, u2 = u .flatten()
    return array([[v*cos(δ)*cos(θ)],[v*cos(δ)*sin(θ)],[v*sin(δ)/3],[u1],[u2]])


x = array([[0],[5],[pi/2],[30],[0.6]])
s=40
dt=0.01
ax=init_figure(-s,s,-s,s)
for t in arange(0,10,dt):
    clear(ax)
    
    mx, my, θ, v, δ = x.flatten()
    
    mxy = array([[vdp(mx,my)]]).T
    w = array([[10,angle(mxy)]]).T
    ubar = array([[w[0,0],3*sawtooth(w[1,0]-θ)]]).T
    u = 10*(ubar - array([[v*cos(δ)],[v*sin(δ)/3]]))

    x = x + dt*f(x,u)
    draw_field(ax,vdp,-s,s,-s,s,4)
    draw_car(x)
  



