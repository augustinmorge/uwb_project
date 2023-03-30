from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]    
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])
    

def f1(x1,x2):  
    n = sqrt((x1-qhat[0])**2 + (x2-qhat[1])**2)
    f1 = vhat[0] - 2*(x1-phat[0]) + (x1-qhat[0]) / (n**3)
    f2 = vhat[1] - 2*(x2-phat[1]) + (x2-qhat[1]) / (n**3)
    return f1, f2

def control(x):
    nq = x[0:2]-qhat
    w = vhat - 2*(x[0:2]-phat) + nq/(norm(nq)**3)
    vbar = norm(w)
    thetabar = arctan2(w[1, 0], w[0, 0])
    u = array([[vbar-x[2, 0]], [10*sawtooth(thetabar-x[3, 0])]])
    return u
    
x    = array([[4,-3,1,2]]).T #x,y,v,θ
dt   = 0.02
s=5
ax=init_figure(-s,s,-s,s)
vhat, phat, qhat = array([[1], [1]]), array([[8], [6]]), array([[4], [3]])

for t in arange(0,5,dt):
    clear(ax)
    phat = array([[cos(t/10)], [2*sin(t/10)]])
    qhat = array([[2*cos(t/5)], [2*sin(t/5)]])       
    draw_disk(qhat,0.3,ax,"magenta")
    draw_disk(phat,0.2,ax,"green")
    u=control(x)
    x=x+dt*f(x,u)    
    draw_tank(x[[0,1,3]],'red',0.2) # x,y,θ
    draw_field(ax,f1,-s,s,-s,s,0.4)


