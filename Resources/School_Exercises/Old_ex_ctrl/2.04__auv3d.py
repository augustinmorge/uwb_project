from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,w):
    clean3D(ax,-50,50,-50,50,0,20)
    draw_axis3D(ax,0,0,0,eye(3,3),10)
    draw_robot3D(ax,x[0:3],eulermat(*x[4:7,0]),'blue')
    ax.scatter(w[0,0],w[1,0],w[2,0],color='red')
    
    ax.plot(X,Y,Z,'black')

def f(x,u):
    x,u=x.flatten(),u.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6];
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    return array([ [v*cθ*cψ],[v*cθ*sψ],[-v*sθ],[u[0]] ,
                    [-0.1*sφ*cθ + tan(θ)*v*(sφ*u[1]+cφ*u[2])] ,
                     [cφ*v*u[1] - sφ*v*u[2]] ,
                     [(sφ/cθ)*v*u[1] + (cφ/cθ)*v*u[2]]])

def control_u(x,c):
    x = x.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6];
    A1 = array([[cos(θ)*cos(ψ), -v*cos(θ)*sin(ψ), -v*sin(θ)*cos(ψ)],
                [cos(θ)*sin(ψ), v*cos(θ)*cos(ψ), -v*sin(θ)*sin(ψ)],
                [-sin(θ), 0, -v*cos(θ)]])
    A2 = array([[1, 0, 0],
                [0, -sin(φ)/cos(θ), cos(φ)/cos(θ)],
                [0, cos(φ), -sin(φ)]])
    A = A1@A2
    u = inv(A)@c
    return u

def control_c(x,w,dw,ddw):
    p = x[0:3]
    x = x.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6];
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    dp = array([[v*cθ*cψ],[v*cθ*sψ],[-v*sθ]])
    c = 0.04*(w-p) + 0.4*(dw-dp) + ddw
    return c

def calcul_w(t):
    c1, c2, c3 = cos(f1*t), cos(f2*t), cos(f3*t)
    s1, s2, s3 = sin(f1*t), sin(f2*t), sin(f3*t)
    w = R*array([[s1+s2],
                 [c1+c2],
                 [s3]])
    dw = R*array([[f1*c1+f2*c2],
                  [-f1*s1-f2*s2],
                  [f3*c3]])
    ddw = R*array([[-f1**2*s1-f2**2*s2],
                  [-f1**2*c1-f2**2*c2],
                  [-f3**2*s3]])
    return w, dw, ddw

tmax = 40
dt = 0.1

f1 = 0.01
f2 = 6*f1
f3 = 3*f1
R = 20
T = arange(0,tmax,dt)
X = R*(sin(f1*T) + sin(f2*T))
Y = R*(cos(f1*T) + cos(f2*T))
Z = R*(sin(f3*T))

#x = array([[0,0,10,15,0,1,0]]).T
x = array([[0,0,1,0.1,0,0,0]]).T 
ax = Axes3D(figure())   

for t in arange(0,tmax,dt):
    
    w, dw, ddw = calcul_w(t)
    c = control_c(x,w,dw,ddw)
    u = control_u(x,c)
    xdot=f(x,u)
    x = x + dt * xdot
    draw(x,w)
    pause(0.001)
  