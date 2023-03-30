from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_rob(x,col):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    R = Rlatlong(lx,ly) @ eulermat(0,0,ψ)
    draw_robot3D(ax,latlong2cart(ρ,lx,ly),R,col,1) 
    
def f(x,u):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    return array([[cos(ψ)/(ρ*cos(ly))], [sin(ψ)/ρ], [u]])

def control(x, xa):
    dx = xa - x
    dx = dx.flatten()
    xa = xa.flatten()
    x = x.flatten()
    M = array([[cos(x[2]), dx[0]*cos(x[1])],[sin(x[2]), dx[1]]])
    u = det(M)
    return u

ρ = 30 
ax = Axes3D(figure())  
xa = array([[0], [0], [0]])
x = array([[1], [1], [1]])
dt = 0.3

for t in arange(0,60,dt):
    clean3D(ax,-ρ,ρ,-ρ,ρ,-ρ,ρ)
    draw_earth3D(ax,ρ,eye(3),'gray')    
    u = control(x, xa)   
    ua = 0.1 * randn(1)
    x = x + dt*f(x,u) 
    xa = xa + dt*f(xa, ua)
    draw_rob(x,"blue")
    draw_rob(xa, "red")
    #draw_earth3D(ax,ρ,eye(3),'gray')
    pause(0.001)
