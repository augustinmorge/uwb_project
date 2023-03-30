from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_buoy(x,w):
    clear(ax) 
    x=x.flatten()
    plot([-10,10],[0,0],'black',linewidth=1)    
    d=x[0]
    P=array([[-ech,-1.8*ech],[ech,-1.8*ech],[ech,0],[-ech,0]])
    draw_polygon(P,ax,'blue')    
    plot([   0,   L,  L,  L/2,   L/2,   L/2,  0,  0],
         [-L-d,-L-d, -d,   -d,   2-d,    -d, -d,-L-d],'black',linewidth=3)
    b=-x[2]     
    P=array([[0,-L-d+L],[L,-L-d+L],[L,-L/2-L*b/2-d],[0,-L/2-L*b/2-d]])
    draw_polygon(P,ax,'white')       
    
    plot([-ech,ech],[-w,-w],'red',linewidth=1)
    
def f(x,u):
    d, v, b = x.flatten()
    dv = g - (g*max(0,L+min(d,0)) + v*abs(v)*cx/2)/(1+0.1*b)
    return array([[v],[dv],[u]])

def control(x,w,dw,ddw):
    d, v, b = x.flatten()
    dv = g - (g*max(0,L+min(d,0)) + v*abs(v)*cx/2)/(1+0.1*b)
    u = sign(w-d + 2*(dw-v) + (ddw - dv)) 
    return u

rho, g, cx = 1000, 9.81, 1.05
ech=5
x = array([[3],[0],[0]])
L=1 #length of the cube
ax=init_figure(-ech,ech,-1.8*ech,0.2*ech)
dt = 0.05

for t in arange(0,30,dt):
    w = 3 + sin(0.5*t)
    dw = 0.5*cos(0.5*t)
    ddw = -0.25*sin(0.5*t)
    u = control(x,w,dw,ddw)
    x = x + dt*f(x,u)
    if abs(x[2])>1 :
        x[2]=sign(x[2])
    draw_buoy(x,w)


