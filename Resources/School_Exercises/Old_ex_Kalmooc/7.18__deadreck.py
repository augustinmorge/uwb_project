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

def f(x,u):
    return (array([x[3]*cos(x[4])*cos(x[2]),
                       x[3]*cos(x[4])*sin(x[2]),
                       x[3]*sin(x[4])/3,
                       u[0],
                       u[1]]))


dt = 0.1
ux = array([[0,0]]).T
x = array([[0,0,pi/3,4,0.2]]).T

Gαx = array([[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0.01*dt,0,0],
            [0,0,0,0.01*dt,0],
            [0,0,0,0,0.01*dt]])

z = array([x[0],x[1],x[3]])
Gz = zeros((3,3))
Gαz = 0.01*dt*eye(3,3)

z2 = z
Gz2 = Gz

ax=init_figure(-50,50,-50,50)

for t in arange(0,30,dt) :
    clear(ax)
     	
    uz = array([[0,0,dt*ux[0,0]]]).T   
    x = x + dt*f(x,ux) + mvnrnd1(Gαx)
    Ak = array([[1, 0, dt*cos(x[4,0])*cos(x[2,0])],
                [0, 1, dt*cos(x[4,0])*sin(x[2,0])],
                [0, 0,          1             ]])
    
    z, Gz, zup, Gup = Kalman(z,Gz,uz,array([]),Gαz,array([]),Ak,array([]))
    draw_ellipse_vide(z[0:2], Gz[0:2,0:2], 0.9,ax,'black')
    draw_car(x) 
    
    # avec lock
    Gbz = 0.1
    y = array([ x[3] + mvnrnd1(Gbz)])
    C = array([[0,0,1]])
    z2, Gz2, zup2, Gup2 = Kalman(z2,Gz2,uz,y,Gαz,Gbz,Ak,C)
    draw_ellipse(z2[0,0:2], Gz2[0:2,0:2], 0.9,ax,'red')
    