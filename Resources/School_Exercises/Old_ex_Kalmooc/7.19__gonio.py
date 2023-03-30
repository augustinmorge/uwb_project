from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from math import atan2
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


La = array([[0,15,30,15],
              [25,30,15,20]])

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[x[3]*cos(x[4])*cos(x[2])],
                    [x[3]*cos(x[4])*sin(x[2])],
                    [x[3]*sin(x[4])/3],
                    [u[0]],
                    [u[1]]]))


    
def g(x):
    x=x.flatten()
    for i in range(La.shape[1]):
        C = array([[0,0,1]])
        y=array([[x[3]]])
        Beta = [1]
        a=La[:,i].flatten()
        da = a-(x[0:2]).flatten()
        dist = norm(da)      
        if dist < 15:
            plot(array([a[0],x[0]]),array([a[1],x[1]]),"red",1)
            δ=arctan2(da[1],da[0])
            Ci = array([[-sin(δ),cos(δ), 0]])
            C = vstack((C,Ci))          
            yi=[[-sin(δ)*a[0] + cos(δ)*a[1]]]
            y = vstack((y,yi)) 
            Beta.append(1)
    Γβ = diag(Beta)
    y = y + mvnrnd1(Γβ)
    return C, y, Γβ 

def gab(xa,xb):
    dab = xb[0:2] - xa[0:2]
    xa=xa.flatten()
    xb=xb.flatten()
    phi = atan2(dab[1,0],dab[0,0]) - xa[2]
    Cab,yab,Γβab = array([]),array([]),array([])     
    if norm(dab) < 20:
        plot(array([xa[0],xb[0]]),array([xa[1],xb[1]]),"red",1)
        δ=arctan2(dab[1],dab[0])
        o = xa[2]+phi
        Cab = array([[-sin(o),cos(o), 0, sin(o), -cos(o),0]])
        Γβab = array([[1]])
        yab = 0 + mvnrnd1(Γβab)
    return Cab, yab, Γβab

def gall(xa,xb):
    Ca, ya, Γβa = g(xa) 
    Cb, yb, Γβb = g(xb) 
    Cab, yab, Γβab = gab(xa,xb)

    if yab.size==0 :
        Γβ = block_diag(Γβa,Γβb)
        C = block_diag(Ca,Cb)
        y = vstack((ya,yb))
    else :
        Γβ = block_diag(Γβa,Γβb,Γβab)
        C = vstack((block_diag(Ca,Cb),Cab))
        y = vstack((ya,yb,yab))

    return C, y, Γβ 
            
def onecar():      
    dt = 0.1
    ua = array([[0]] * 2)
    xa = array([[20,-30,pi/3,15,0.1]]).T
    Γαxa = diag([dt*0.001,dt*0.001,0,dt*0.001,0])
    
    z = zeros((3,1))
    Gz = 1000*eye(3,3)
    Galpha = dt*0.001*eye(3,3)
    
    ax=init_figure(-100,100,-100,100)
    
    for t in arange(0,10,dt) :   
        clear(ax)
        draw_car(xa)
        scatter(La[0], La[1])
        θa,δa = xa[2,0],xa[4,0]
        Ak = eye(3,3) + dt*array([[0, 0, cos(δa)*cos(θa)],
                                  [0, 0, cos(δa)*sin(θa)],
                                  [0, 0,        0       ]])
        uk = array([[0,0,dt*ua[0,0]]]).T
        Ca,ya,Γβa = g(xa)
        
        z, Gz = kalman(z,Gz,uk,ya,Galpha,Γβa,Ak,Ca)
        draw_ellipse_vide(z[0:2], Gz[0:2,0:2], 0.9,ax,'green')
        xa = xa + dt*f(xa,ua) + mvnrnd1(Γαxa)        
   
### Q5

def twocars():
    dt = 0.1
    
    ua = array([[0]] * 2)
    xa = array([[-13,-22,pi/3,15,0.1]]).T
    Γαxa = diag([dt*0.001,dt*0.001,0,dt*0.001,0])
    
    ub = array([[0]] * 2)
    xb = array([[20,-10,pi/3,18,0.2]]).T
    Γαxb = diag([dt*0.001,dt*0.001,0,dt*0.001,0])
    
    z = zeros((6,1))
    Gz = 1000*eye(6,6)
    Galpha = dt*diag([0.1,0.1,0.5,0.1,0.1,0.5])
    
    ax=init_figure(-100,100,-100,100)
    
    for t in arange(0,15,dt) :   
        clear(ax)
        draw_car(xa)
        draw_car(xb)
        scatter(La[0], La[1])
        θa,δa = xa[2,0],xa[4,0]
        θb,δb = xb[2,0],xb[4,0]
        Aka = eye(3,3) + dt*array([[0, 0, cos(δa)*cos(θa)],
                                  [0, 0, cos(δa)*sin(θa)],
                                  [0, 0,        0       ]])
        Akb = eye(3,3) + dt*array([[0, 0, cos(δb)*cos(θb)],
                                  [0, 0, cos(δb)*sin(θb)],
                                  [0, 0,        0       ]])
        Ak = block_diag(Aka,Akb)
        uk = array([[0,0,dt*ua[0,0],0,0,dt*ub[0,0]]]).T
        Ck, y, Γβ = gall(xa,xb)
    
        z, Gz = kalman(z,Gz,uk,y,Galpha,Γβ,Ak,Ck)
        
        draw_ellipse_vide(z[0:2], Gz[0:2,0:2], 0.9,ax,'green')
        draw_ellipse_vide(z[3:5], Gz[3:5,3:5], 0.9,ax,'green')
        xa = xa + dt*f(xa,ua) + mvnrnd1(Γαxa)        
        xb = xb + dt*f(xb,ub) + mvnrnd1(Γαxb) 
    
if __name__ == '__main__' :
    onecar()
    pause(2)
    twocars()
    
       
