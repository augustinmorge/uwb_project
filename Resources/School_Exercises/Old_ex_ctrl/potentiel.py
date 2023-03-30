from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


# XY = array([[176, 272], [192, 272], [208, 272], [224, 272], [240, 256], [256, 240], [272, 224], [288, 208], [304, 208], [320, 208], [336, 224], [352, 240], [368, 256], [384, 272], [400, 288], [416, 304], [432, 320]])
# X = XY[:,0]
# Y = XY[:,1]
# print(X)

# plot(X,Y)
# show()

def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]    
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])
    

def field(x1,x2):  
    xy = array([x1, x2]).T
    n = sqrt((x1-qhat[0])**2 + (x2-qhat[1])**2)
    f1 = vhat[0] - 2*(x1-phat[0])
    f2 = vhat[1] - 2*(x2-phat[1]) 
    print(f1 , " f2 ", f2)
    f1, f2 = vhat - 2*(xy-phat) 
    print(f1 , " f2 le 2 : ", f2)
    return f1, f2

def control(x):

    f1, f2 = field(x[0,0], x[1,0])
    w = array([[f1[0]], [f2[0]]])
    vbar = norm(w)
    thetabar = arctan2(w[1, 0], w[0, 0])
    u = array([[vbar-x[2, 0]], [10*sawtooth(thetabar-x[3, 0])]])
    return u
    
x    = array([[4,-3,1,2]]).T #x,y,v,θ
dt   = 0.02
s=5
ax=init_figure(-s,s,-s,s)
vhat, phat, qhat = array([[1], [1]]), array([[8], [6]]), array([[4], [3]])

for t in arange(0,2*dt,dt):
    clear(ax)
    phat = array([[cos(t/10)], [2*sin(t/10)]])
    qhat = array([[2*cos(t/5)], [2*sin(t/5)]])       
    draw_disk(qhat,0.3,ax,"magenta")
    draw_disk(phat,0.2,ax,"green")
    u=control(x)
    x=x+dt*f(x,u)    
    draw_tank(x[[0,1,3]],'red',0.2) # x,y,θ
    draw_field(ax,field,-s,s,-s,s,0.4)