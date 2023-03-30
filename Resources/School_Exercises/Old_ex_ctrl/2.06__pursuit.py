from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[u[0]*cos(x[2])], [u[0]*sin(x[2])],[u[1]]]))

def control_u(x,w,v):
    
    p = x[0:2]
    px, py, theta = x.flatten()
    Ax = array([[-1, py],
                [0, -px]])
    bx = v[0,0]*array([[cos(theta)],
                      [sin(theta)]])
    u = inv(Ax)@(w-p + dw - bx)
    return u    

ax=init_figure(-30,30,-30,30)
dt = 0.1

xa = array([[-10], [-10],[0]])
xb = array([[-5],[-5],[0]])


for t in arange(0,40,dt) :
    clear(ax)
    x = eulermat(0,0,-xa[2,0])@(xb-xa)
    v = array([[3], [sin(0.2*t)]])
    w = array([[10],[0]])
    dw = array([[0],[0]])
    u=control_u(x,w,v)
    draw_tank(xa,'blue')  	
    draw_tank(xb,'red')  	
    xa = xa + dt*f(xa,u)
    xb = xb + dt*f(xb,v)



    
