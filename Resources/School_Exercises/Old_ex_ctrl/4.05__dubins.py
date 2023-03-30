from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x = x.flatten()
    θ = x[2]
    return array([[cos(θ)],[sin(θ)],[u]])

def control(x):
    x = x.flatten()
    e = theta_bar - x[2]
    u = e % (2*pi) - 2*pi  # pour tourner par la droite
    return u/2*pi
    
x   = array([[0],[0],[0.1]])
dt  = 0.1
ax=init_figure(-10,10,-10,10)
theta_bar = -2

for t in arange(0,6,dt):
    clear(ax)
    u = control(x)
    x = x + dt*f(x,u)    
    draw_tank(x,'red',0.3) 
    
