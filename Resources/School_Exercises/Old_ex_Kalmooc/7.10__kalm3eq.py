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
    
    
xhat0 = zeros((2,1))
Gx0 = 1000*eye(2,2)
u = 0
y0 = 8
Galpha = zeros((2,2))
Gbeta = 1
A = eye(2,2)
C0 = array([[2,3]])
x1, G1, xhat, Geps = Kalman(xhat0,Gx0,u,y0,Galpha,Gbeta,A,C0)


ax=init_figure(-100,100,-100,100)
draw_ellipse(xhat0,Gx0,0.9,ax,[1,1,1]) #blanc

draw_ellipse(x1,G1,0.9,ax,[1,0.9,0.9]) # rouge

y1 = 7
Gbeta = 4
C1 = array([[3,2]])
x2, G2, xhat, Geps = Kalman(x1,G1,u,y1,Galpha,Gbeta,A,C1)
draw_ellipse(x2,G2,0.9,ax,[0.8,1,0.8]) #vert

y2 = 0
Gbeta = 4
C2 = array([[1,-1]])
x3, G3, xhat, Geps = Kalman(x2,G2,u,y2,Galpha,Gbeta,A,C2)
draw_ellipse(x3,G3,0.9,ax,[0.7,0.7,1]) #bleu


xhat0 = zeros((2,1))
Gx0 = 1000*eye(2,2)
u = 0
Galpha = zeros((2,2))
y = array([[8,7,0]]).T
Gbeta = diag([1,4,4])
A = eye(2,2)
C = vstack((C0,C1,C2))
x, Gx, xhat, Geps = Kalman(xhat0,Gx0,u,y,Galpha,Gbeta,A,C)
draw_ellipse(x,Gx,0.9,ax,[1,1,0.7]) # jaune

