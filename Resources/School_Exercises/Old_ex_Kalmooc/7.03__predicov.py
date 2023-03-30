from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from time import time
N=1000
X=randn(2,N)

xbar = array([[1],[2]])
Gx = array([[3,1],[1,3]])

x = sqrtm(Gx)@X + xbar

# ax=init_figure(-10,10,-10,10)
# eta = [0.9, 0.99, 0.999]
# for i in range(len(eta)):
#     draw_ellipse(xbar,Gx,eta[i],ax,'none') 
# plot(x[0,:],x[1,:],'+')   

print('xbar estimé = ',[mean(x[0,:]),mean(x[1,:])])

dt = 0.03
tmax = 5
A = array([[0,1],[-1,0]])
B = array([[2],[3]])
Ad = eye(2,2)+A*dt

d = 17
ax = init_figure(-d,d,-d,d)
pause(15)
for t in arange(0,tmax,dt):
    Bd = dt*B*sin(t)
    x = Ad@x + Bd
    xbar = Ad@xbar + Bd
    Gx = Ad@Gx@Ad.T
    
    clear(ax)
    draw_ellipse(xbar,Gx,0.9,ax,'none')
    draw_ellipse(xbar,Gx,0.99,ax,'none')
    draw_ellipse(xbar,Gx,0.999,ax,'none')
    plot(x[0,:],x[1,:],'+')
    pause(dt)
    
