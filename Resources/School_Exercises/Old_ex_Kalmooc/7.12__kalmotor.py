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


C = [array([[4,0]]),array([[10,1]]),array([[10,5]]),array([[13,5]]),array([[15,3]])]
y = [5,10,11,14,17]
xhat = array([[1],[-1]])
Γx = 4*eye(2)
A = eye(2,2)
u = zeros((2,1))
Galpha = zeros((2,2))
Gbeta = 9
ax=init_figure(-7,7,-7,7)
draw_ellipse(xhat,Γx,0.9,ax,[1,0.8,0.8])


for k in range(5):
    
    xhat, Γx, x, Geps = Kalman(xhat,Γx,u,y[k],Galpha,Gbeta,A,C[k])
    draw_ellipse(xhat,Γx,0.9,ax,[1,0.8,0.8])
    
x1, x2 = xhat.flatten()
print("x1 = ",x1)
print("x2 = ",x2)
print("Γx = ",Γx)