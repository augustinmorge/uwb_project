
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return array([[x[3]*cos(x[2])],
                   [x[3]*sin(x[2])],
                   [u[0]],[u[1]]])
    
    
    
def control(x,w,dw,ddw):
    x1, x2, x3, x4 = x.flatten()
    
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])
    y = array([[x1],
               [x2]])
    dy = array([[x4*cos(x3)],
                [x4*sin(x3)]])
    ddy = w-y + 2*(dw-dy) + ddw
    
    u = inv(Ax)@ddy
    return u  

def control2(x,w,dw):
    x1, x2, x3, x4 = x.flatten()
    
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])
    y = array([[x1],
               [x2]])
    dy = array([[x4*cos(x3)],
                [x4*sin(x3)]])
    K = 100
    ddy = K*sign((w-y + dw-dy))
    
    u = inv(Ax)@ddy
    return u   


ax=init_figure(-30,30,-30,30)
dt = 0.02
x = array([[10],[0],[1],[1]])
xg = array([[10],[0],[1],[1]])
E = []
Eg = []
T = []
L=10
s = arange(0,2*pi,0.01)
for t in arange(0,10,dt) :
    clear(ax)
    plot(L*cos(s), L*sin(3*s),color='magenta')
    
    draw_tank(x,'red') 
    draw_tank(xg,'blue') 
    
    w=L*array([[cos(t)],[sin(3*t)]])  
    dw=L*array([[-sin(t)],[3*cos(3*t)]])  
    ddw=L*array([[-cos(t)],[-9*sin(3*t)]]) 
    draw_disk(w,0.5,ax,"red") 
    
    u=control(x,w,dw,ddw)
    ug=control2(xg,w,dw)
    
    E.append(abs(x[0,0]-w[0,0])+abs(x[1,0]-w[1,0]))
    Eg.append(abs(xg[0,0]-w[0,0])+abs(xg[1,0]-w[1,0]))
    T.append(t)
    
    x = x + dt*f(x,u)
    xg = xg + dt*f(xg,ug)
    
fig=figure()
plot(T,E,'red')
plot(T,Eg,'blue')




    

    



    
    
    

