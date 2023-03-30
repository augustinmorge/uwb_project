
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def Kalman(xbar,Γx,u,y,Γα,Γβ,A,C):
    
    if y.size==0 : # predictor mode
        y = eye(0,1)
        C = eye(0,len(xbar))
        Γβ = eye(0,0)
        
    ytilde = y - C@xbar
    Γy = C@Γx@C.T + Γβ
    
    K = Γx@C.T@inv(Γy)
    xup = xbar + K@ytilde
    
    Γup = Γx - K@C@Γx
    x1 = A@xup + u
    Γ1 = A@Γup@A.T + Γα
    
    return x1, Γ1, xup, Γup

def draw_ellipse_vide(c,Γ,η,ax,col): # Gaussian confidence ellipse with artist
    #draw_ellipse(array([[1],[2]]),eye(2),0.9,ax,[1,0.8-0.3*i,0.8-0.3*i])
    if (norm(Γ)==0):
        Γ=Γ+0.001*eye(len(Γ[1,:]))
    A=sqrtm(-2*log(1-η)*Γ)    
    w,v=eig(A)    
    v1=array([[v[0,0]],[v[1,0]]])
    v2=array([[v[0,1]],[v[1,1]]])        

    f1=A @ v1
    f2=A @ v2      
    φ =  (arctan2(v1 [1,0],v1[0,0]))
    α=φ*180/3.14
    e = Ellipse(xy=c, width=2*norm(f1), height=2*norm(f2), angle=α)   
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    
    e.set_alpha(0.7)
    e.set_facecolor('none')
    e.set_edgecolor(col)

#Γx = array([[0.7,0.3],[0.3,0.2]])

xhat = array([[0,1]]).T
Gx = diag([0, 0.02**2])
Galpha = diag([0,0.01**2])
u = 0

ax=init_figure(-1,12,0.8,1.25)
ax.set_aspect('auto')
title("Ellipses de confiance en fonction de k")
draw_ellipse_vide(xhat, Gx, 0.99,ax,'red')

ex1 = zeros((21,1))
deter = zeros((21,1))
ex1[0] = sqrt(Gx[0,0])
deter[0] = det(Gx)

for k in range(20):
    
    if k<10 :
        uk = 1
    else :
        uk = -1
    
    Ak = array([[1, uk],
                [0, 1]])
    
    xhat, Gx, xup, Gup = Kalman(xhat,Gx,u,array([]),Galpha,array([]),Ak,array([]))
    
    draw_ellipse_vide(xhat, Gx, 0.99,ax,'blue')
    ex1[k+1] = sqrt(Gx[0,0])
    deter[k+1] = det(Gx)
    
figure(2)
title("Incertitude sur x1 en fonction de k")
plot(ex1)
figure(3)
title("Déterminant de Gx en fonction de k")
plot(deter)
show()