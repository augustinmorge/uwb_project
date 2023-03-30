from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

         
    
def f(x,u):
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1];
    w_ap = array([[awind*cos(ψ-θ) - v],[awind*sin(ψ-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = p4*v*sin(δr)
    fs = p3*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + p0*awind*cos(ψ)
    dy=v*sin(θ) + p0*awind*sin(ψ)
    dv=(fs*sin(δs)-fr*sin(δr)-p1*v**2)/p8
    dw=(fs*(p5-p6*cos(δs)) - p7*fr*cos(δr) - p2*w*v)/p9
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs    

def control(x, q):
    x = x.flatten()
    theta = x[2]
    m = array([[x[0]], [x[1]]])
    e = det(hstack(((b-a)/norm(b-a), m-a))) 
    phi = arctan2(b[1, 0]-a[1, 0], b[0, 0]-a[0, 0]) 
    
    if abs(e) > r:
        q = sign(e)
    
    theta_bar = phi - arctan2(e, r)
    
    if cos(ψ-theta_bar)+cos(zeta) < 0:  
        theta_bar = pi+ψ-zeta*q 

    deltar = sawtooth(theta - theta_bar)/pi
    deltasmax = pi/4*(cos(ψ-theta_bar)+1)
    u = array([[deltar, deltasmax]])

    return u, q
    
def wind_evolution(a,w):
    a += 0.1*(0.5-rand())
    w += 0.1*(0.5-rand())
    return a,w
    
    
p0,p1,p2,p3,p4,p5,p6,p7,p8,p9 = 0.1,1,6000,1000,2000,1,1,2,300,10000
x = array([[10,-40,-3,1,0]]).T   #x=(x,y,θ,v,w)

dt = 0.1
awind,ψ = 2,-1
a = array([[-50],[-100]])   
b = array([[50],[100]])
r = 10  
zeta = pi/4 
q = 1 
beta = pi/4  
              
ax=init_figure(-100,100,-60,60)

for t in arange(0,40,0.1):
    clear(ax)
    plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')
    #awind,ψ = wind_evolution(awind,ψ)
    u, q = control(x, q)
    xdot,δs=f(x,u)
    x = x + dt*xdot
    draw_sailboat(x,δs,u[0,0],ψ,awind)


        