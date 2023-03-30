from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,col):
    θ = x[0]/r
    a=array([[r*cos(θ)],[r*sin(θ)],[θ+pi/2]])
    draw_tank(a,col)
        
def circular_dist(xa,xb):
    dx = xb - xa
    return r*(sawtooth(dx[0]/r - pi) + pi)

def f(xa,u):
    return array([xa[1],u])

def g(xa,xb):
    dx = xb - xa
    return array([[circular_dist(xa, xb)],[dx[1]]])

def control(x,y,a):
    u = (y[0]-d0) + a*y[1] + (v0-x[1])
    return u

def sim(m,titre,a):
    X = zeros((2,m))
    for i in range(m):
        X[0,i] = -8*i
    
    for t in arange(0,10,dt):
        clear(ax)
        ax.set_title(titre)
        draw_disk(array([[0],[0]]),r+3,ax,'lightblue')
        draw_disk(array([[0],[0]]),r-3,ax,'white') 
        
        
        for i in range(m):  
            xi = X[:,i]
            xj = X[:,i-1] #devant xi
            yi = g(xi,xj)
            u = control(xi,yi,a)
            xi = xi + dt*f(xi,u)
            draw(xi,'black')
            if circular_dist(xi, xj)<5 :
                xi[1] = 0
                draw(xi,'red')
            X[:,i] = xi

L=100
r=L/(2*pi)
ax=init_figure(-20,20,-20,20)
dt = 0.05

m = 10
d0 = L/m
v0 = 10
titre = "Commande sans le terme dérivé"
sim(m,titre,0)
pause(1)
titre = "Commande complète"
sim(m,titre,1)
