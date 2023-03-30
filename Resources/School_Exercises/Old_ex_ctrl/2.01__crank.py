from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_crank(x,col): 
    θ1=x[0,0]
    θ2=x[1,0]
    z=L1*array([[cos(θ1)],[sin(θ1)]])
    y=z+L2*array([[cos(θ1+θ2)],[sin(θ1+θ2)]])
    plot( [0,z[0,0],y[0,0]],[0,z[1,0],y[1,0]],col, linewidth = 2)   
    draw_disk(c,r,ax,"cyan")


L1,L2 = 4,3
c = array([[1],[2]])
r=4
col='magenta'
dt = 0.05
x = array([[-1],[1]])

def y(x):
    θ1=x[0,0]
    θ2=x[1,0]
    z=L1*array([[cos(θ1)],[sin(θ1)]])
    y=z+L2*array([[cos(θ1+θ2)],[sin(θ1+θ2)]])
    return y
    

def f(x,u):

    return u
    
def control_u(x,v):
    x1, x2 = x.flatten()
    A = array([[-L1*sin(x1)-L2*sin(x1+x2), -L2*sin(x1+x2)], 
               [L1*cos(x1)+L2*cos(x1+x2), L2*cos(x1+x2)]])
    
    return inv(A)@v
    
ax=init_figure(-4,8,-4,8)

# for t in arange(0,10,dt) :
#     clear(ax)
#     draw_crank(x,col)
#     w = c + r*array([[cos(t)],[sin(t)]])
#     dw = r*array([[-sin(t)],[cos(t)]])
#     v = w - y(x) + dw
#     u=control_u(x,v)
#     x = x + dt*f(x,u)  
    
###### Q5

def manivelle(x,t,col):
    draw_crank(x,col)
    w = c + r*array([[cos(t)],[sin(t)]])
    dw = r*array([[-sin(t)],[cos(t)]])
    v = w - y(x) + dw
    u=control_u(x,v)
    x = x + dt*f(x,u)  
    return x

n = 8
c = array([[3],[4]])
r=1
col='magenta'
dt = 0.05
X = [array([[-1],[1]])]*n
L = [0.1,2.9] # intervalle à éviter pour L1
L1_limite=3
x = array([[-1],[1]])

for t in arange(0,10,dt) :
    clear(ax)
    
    for i in range(n):
        l = L[0]+i*(L[1]-L[0])/(n-1)
        L1,L2 = l, l
        X[i]=manivelle(X[i],t,col)
        
    L1,L2 = L1_limite, L1_limite
    x=manivelle(x,t,'red')
    
