from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

# calcul de l'inverse de A, avec tmax=10 le programme met 31s contre 36s donc pas très utile ici
import sympy as sp 

va, θa = sp.symbols("va θa")
A = sp.Matrix([[-va*sp.sin(θa), sp.cos(θa)],
                [va*sp.cos(θa), sp.sin(θa)]])
Ainv = sp.simplify(A.inv())
Ainv = sp.lambdify((va, θa), Ainv)

def f(x,u):
    xr,yr,θr,vr=x.flatten()
    u1,u2=u.flatten()
    return array([[vr*cos(θr)],[vr*sin(θr)],[u1],[u2]])

def control_u(x,w,dw):
    xa, ya, θa, va = x.flatten()
    dxa = va*cos(θa)
    dya = va*sin(θa)
    # A = array([[-dya, cos(θa)],
    #             [dxa, sin(θa)]])
    y = array([[xa,ya]]).T
    dy = array([[dxa,dya]]).T
    v = w - y + 2*(dw - dy) # pas de ddy
    u = Ainv(va, θa)@v
    return u

def control_w(x,u):
    θ = x[2,0]
    v = x[3,0]
    dx = v*cos(θ)
    dy = v*sin(θ)
    w = x[:2,:] - l*array([[cos(θ)], [sin(θ)]])
    dw = array([[dx,dy]]).T + l*u[0,:]*array([[sin(θ)], [-cos(θ)]])
    return w, dw

ax=init_figure(-30,30,-30,30)
dt = 0.05

xa = array([[0],[1],[pi/3],[1]])
wa = zeros((2,1))
ua = zeros((2,1))

xb = array([[10],[0],[1],[2]])
wb = zeros((2,1))
ub = zeros((2,1))

xc = array([[-10],[0],[1],[2]])
wc = zeros((2,1))
uc = zeros((2,1))

Lx, Ly = 15, 7
omega = 0.1
l = 6
T = array([i for i in arange(0,2*pi,0.01)])
E = [Lx*sin(T),Ly*cos(T)]

for t in arange(0,10,dt) :
    clear(ax)
    plot(E[0],E[1])

    draw_tank(xa,'r')
    plot(wa[0,:], wa[1,:], 'ro')
    draw_tank(xb,'b')
    plot(wb[0,:], wb[1,:], 'bo')
    draw_tank(xc,'g')
    plot(wc[0,:], wc[1,:], 'go')
    
    wa = array([[Lx*sin(omega*t), Ly*cos(omega*t)]]).T
    dwa = array([[Lx*omega*cos(omega*t), -Ly*omega*sin(omega*t)]]).T
    ua = control_u(xa,wa,dwa)   
    
    # wb, dwb = control_w(xa,ua)
    # ub = control_u(xb,wb,dwb)  
    
    # wc, dwc = control_w(xb,ub)
    # uc = control_u(xc,wc,dwc)  
    
    #######Q6
    
    t -= 5
    wb = array([[Lx*sin(omega*t), Ly*cos(omega*t)]]).T
    dwb = array([[Lx*omega*cos(omega*t), -Ly*omega*sin(omega*t)]]).T
    ub = control_u(xb,wb,dwb)  
    
    t -= 5
    wc = array([[Lx*sin(omega*t), Ly*cos(omega*t)]]).T
    dwc = array([[Lx*omega*cos(omega*t), -Ly*omega*sin(omega*t)]]).T
    uc = control_u(xc,wc,dwc)  
    
    
    xa = xa+dt*f(xa,ua)
    xb = xb+dt*f(xb,ub)
    xc = xc+dt*f(xc,uc)

