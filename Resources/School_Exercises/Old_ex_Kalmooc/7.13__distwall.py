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

A = array([[2,1],[15,5],[3,12]])    
B = array([[15,5],[3,12],[2,1]])    
C = zeros((3,2))
dbar = zeros((3,1))

for i in range(3):
    u = (B[i]-A[i])/norm(B[i]-A[i])
    C[i] = -u[1], u[0]
    #dbar[i] = det(hstack((u.reshape((2,1)),-A[i].reshape((2,1)))))  
    dbar[i] = u[1]*A[i,0] - u[0]*A[i,1]

x0 = array([[1,2]]).T
Γx = 100*eye(2)
Γβ = eye(3,3)
Γα = zeros((2,2))
d = array([[2, 5, 4]]).T
y = d - dbar
u = 0

x1, G1, xhat, Geps = Kalman(x0,Γx,u,y,Γα,Γβ,eye(2,2),C)

ax=init_figure(-5,20,-5,20)
for i in range(3):   
    a,b = A[i],B[i]
    plot([a[0],b[0]],[a[1],b[1]],color="black")    
    draw_disk(x1,d[i],ax,"blue",0.3)
    draw_ellipse_vide(x1,G1,0.9,ax,"black")

