from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def Kalman(xbar,Gx,u,y,Galpha,Gbeta,A,C):
    
    ybar = C@xbar
    ytilde = y - ybar
    Gy = C@Gx@C.T + Gbeta
    
    K = Gx@C.T@inv(Gy)
    xhat = xbar + K@ytilde
    
    Geps = Gx - K@C@Gx
    x1 = A@xhat + u
    G1 = A@Geps@A.T + Galpha
    
    return x1, G1, xhat, Geps

A0 = array([[0.5, 0],
            [0, 1]])
A1 = array([[1, -1],
            [1, 1]])
A2 = A1

u0 = array([[8, 16]]).T
u1 = array([[-6, -18]]).T
u2 = array([[32, -8]]).T

C = array([[1,1]])

y0 = 7
y1 = 30
y2 = -6

Galpha = eye(2,2)
Gbeta = 1
xhat0 = array([[0, 0]]).T
Gx0 = 100*eye(2,2)

ax=init_figure(-30,30,-30,30)
draw_ellipse(xhat0,Gx0,0.9,ax,[1,1,1])

xup1, Γup1, xhat1, Geps1 = Kalman(xhat0,Gx0,u0,y0,Galpha,Gbeta,A0,C)
draw_ellipse(xup1,Γup1,0.9,ax,[1,0.8,0.8])
draw_ellipse(xhat1,Geps1,0.9,ax,[1,1,1])

xup2, Γup2, xhat2, Geps2 = Kalman(xup1, Γup1,u1,y1,Galpha,Gbeta,A1,C)
draw_ellipse(xup2,Γup2,0.9,ax,[0.8,1,0.8])
draw_ellipse(xhat2,Geps2,0.9,ax,[1,0.8,0.8])

xup3, Γup3, xhat3, Geps3 = Kalman(xup2, Γup2,u2,y2,Galpha,Gbeta,A2,C)
draw_ellipse(xup3,Γup3,0.9,ax,[0.8,0.8,1])
draw_ellipse(xhat3,Geps3,0.9,ax,[0.8,1,0.8])