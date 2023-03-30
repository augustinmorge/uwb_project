
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],
                  [u[0]],[u[1]],[x[3]]])
    return(xdot)

def control(x,w,dw):
    x1, x2, x3, x4, x5 = x.flatten()
    
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])
    y = array([[x1],
               [x2]])
    dy = array([[x4*cos(x3)],
                [x4*sin(x3)]])
    ddy = w-y + (dw-dy)
    u = inv(Ax)@ddy
    return u    


    
ax=init_figure(-30,30,-30,30)
xa  = array([[0],[10],[1],[5],[0]])
m = 6
d = 5
X=array([4*arange(0,m),zeros(m),ones(m),3*ones(m),zeros(m)])
Lx,Ly = 20,5
e   = np.linspace(0.,2*pi,30)
p   = array([[Lx*cos(e)],[Ly*sin(e)]])
S   = xa
ds = 0.1
dt  = 0.05
for t in arange(0,50,dt):
    clear(ax)
    wa  = array([[Lx*sin(0.1*t)],[Ly*cos(0.1*t)]]) 
    dwa = array([[Lx*0.1*cos(0.1*t)],[-Ly*0.1*sin(0.1*t)]]) 
    ua  = control(xa,wa,dwa)    
    plot(wa[0][0],wa[1][0],'ro')
    plot(p[0][0],p[1][0])
    draw_tank(xa,'blue')
    
    if xa[4] > ds :
        S = hstack((S,xa))
        xa[4] = 0
    
    xa  = xa + dt*f(xa,ua)
    for i in range(m):
        xi=X[:,i].reshape(5,1)
        j = int(S.shape[1] - d*(i+1)/ds)
        if j > 0 :
            xaj = S[:,j].reshape(5,1)
            wi = xaj[0:2]
            dwi = xa[3]*array([[cos(xaj[2])],[sin(xaj[2])]])
            ui = control(xi,wi,dwi)
            plot(wi[0][0],wi[1][0],'bo')
        else :
            ui = array([[0.2,0]]).T

        draw_tank(xi,'black')
        xi=xi+f(xi,ui)*dt        
        X[:,i]  = xi.flatten()            



