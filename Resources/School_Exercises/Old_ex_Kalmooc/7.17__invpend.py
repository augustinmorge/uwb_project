from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

# Q1 :
# Linéarisation en x=0 :
# dx1 = x3 ; dx2 = x4 ; 
# dx3 = (m*x2*g + u)/M
# dx4 = (x2*(M+m)*g + u)/(l*M)
#
#Q2 :
# dx = (A-BK)x + Bhw
# det(sI-A+BK)= (s+2)²

def f(x,u):
    s,θ,ds,dθ=x[0,0],x[1,0],x[2,0],x[3,0]
    dds=(mr*sin(θ)*(g*cos(θ)- l*dθ**2) + u)/(mc+mr*sin(θ)**2)
    ddθ= (sin(θ)*((mr+mc)*g - mr*l*dθ**2*cos(θ)) + cos(θ)*u)/ (l*(mc+mr*sin(θ)**2))
    return array([[ds],[dθ],[dds],[ddθ]])


def kalman_extended(x0,Γ0,u,y,Γα,Γβ,A,C):
    xup, Gup = kalman_correc(x0,Γ0,y,Γβ,C)
    Γ1 = A @ Gup @ A.T + Γα
    x1 = xup + f(xup,u)*dt  
    return x1, Γ1   

def draw_invpend2(ax,x,y): #inverted pendulum
    s,θ=x[0,0],x[1,0]
    draw_box(ax,s-0.7,s+0.7,y-0.25,y,'blue')
    plot( [s,s-sin(θ)],[y,y+cos(θ)],'magenta', linewidth = 2)

ax=init_figure(-3,3,-3,3)

mc,l,g,mr = 5,1,9.81,1
dt = 0.02


Γα = (sqrt(dt)*(10**-3))**2*eye(4)
A = array([[0,       0      , 1, 0],
           [0,       0      , 0, 1],
           [0,     mr*g/mc   , 0, 0],
           [0, (mr+mc)*g/(l*mc), 0, 0]])
B = array([[0],[0],[1/mc],[1/(l*mc)]])
K = place(A,B,(-2,-2.1,-2.2,-2.3))
E = array([[1,0,0,0]])
h = -inv(E@inv(A-B@K)@B)
w = 2
C = array([[1,0,0,0],
           [0,1,0,0]])
L = place(A.T,C.T,(-2,-2.1,-2.2,-2.3)).T
Galpha = dt*0.0001*eye(4,4)
Gbeta = 0.01**2*eye(2,2)


x = array([[0,0.2,0,0]]).T
xhat = zeros((4,1))

x1 = array([[0,0.2,0,0]]).T
xhat1 = zeros((4,1))
Gx1 = eye(4,4)

x2 = array([[0,0.2,0,0]]).T
xhat2 = zeros((4,1))
Gx2 = eye(4,4)


for t in arange(0,8,dt) :
    clear(ax)
    draw_invpend2(ax,x,0)
    draw_invpend2(ax,x1,2)
    draw_invpend2(ax,x2,-2)
    plot(w,0,"ro")
    plot(w,2,"bo")
    plot(w,-2,"go")
    ax.scatter(xhat[0,0],0)
    ax.scatter(xhat1[0,0],2)
    ax.scatter(xhat2[0,0],-2)

    α=mvnrnd1(Γα)
    beta=mvnrnd1(Gbeta)
    
    ## Luen Berger
    u = (-K@xhat + h*w)[0,0]
    y = C@x + beta
    xhat = xhat + (A@xhat + B*u - L@(C@xhat-y))*dt
    
    ## Kalman
    u1 = (-K@xhat1 + h*w)[0,0]
    y1 = C@x1 + beta
    xhat1, Gx1 = kalman(xhat1,Gx1,dt*B*u1,y1,Galpha,Gbeta,eye(4,4)+dt*A,C)
    
    ## Kalman extended
    u2 = (-K@xhat2 + h*w)[0,0]
    y2 = C@x2 + beta
    xhat2, Gx2 = kalman_extended(xhat2,Gx2,u2,y2,Galpha,Gbeta,eye(4,4)+dt*A,C)
    
    
    x = x + dt*f(x,u) + α  
    x1 = x1 + dt*f(x1,u1) + α  
    x2 = x2 + dt*f(x2,u2) + α  
   
