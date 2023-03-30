from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(ap,aw): 
    aw=-aw-ap;
    c=2*array([-sin(ap),cos(ap)])
    plot( [0,c[0]],[0,c[1]],'magenta', linewidth = 2)
    for i in arange(0,8):
        plot(c[0]+array([0,cos(aw+i*pi/4)]),c[1]+array([0,sin(aw+i*pi/4)]),'blue')
    pause(0.01)
    

def f(x,u): 
    x=x.flatten()
    return array([[x[1]],[a1*sin(x[0])-b1*u],[-a1*sin(x[0])+c1*u]])

def control_u1(x,v):
    x1, x2, x3 = x.flatten()
    u = (a1*sin(x1) - v)/b1
    return u

def control_v1(x,w,dw,ddw):
    x1, x2, x3 = x.flatten()
    y = x1
    dy = x2
    v = w-y + 2*(dw-dy) + ddw
    return v
    
def calcul_w1(x):
    return 0, 0, 0

def control_u2(x,v):
    x1, x2, x3 = x.flatten()
    bx = eta*sin(x1)*(a1*cos(x1)-x2**2)
    ax = -b1*eta*cos(x1)
    u = (v-bx)/ax
    return u

def control_v2(x,w,dw,ddw):
    x1, x2, x3 = x.flatten()
    y = c1*x2 + b1*x3
    dy = eta*sin(x1)
    ddy = eta*x2*cos(x1)
    v = w-y + 3*(dw-dy) + 3*(ddw-ddy) + 0
    return v

a1,b1,c1=10,1,2
eta = a1*(c1-b1)
dt = 0.02
x = array([[1],[0],[1]])
aw=0  # wheel angle
ax=init_figure(-3,3,-3,3)

### Q2

for t in arange(0,5,dt) :
    
    w, dw, ddw = calcul_w1(x)
    v = control_v1(x,w,dw,ddw)
    u = control_u1(x,v)
    x=x+f(x,u)*dt
    aw=aw+dt*x[2]
    clear(ax)
    draw(x[0],aw)


### Q3

x = array([[1],[0],[1]])

for t in arange(0,10,dt) :
    
    w, dw, ddw = calcul_w1(x)
    v = control_v2(x,w,dw,ddw)
    u = control_u2(x,v)
    x=x+f(x,u)*dt
    aw=aw+dt*x[2]
    clear(ax)
    draw(x[0],aw)

 


