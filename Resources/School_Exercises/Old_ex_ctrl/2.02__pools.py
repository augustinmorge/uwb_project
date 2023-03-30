from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_pools(x,w):
    x=x.flatten()
    plot([0,0],[10,1],'black',linewidth=2)    
    plot([-7,23],[0,0],'black',linewidth=5)    
    plot([16,16],[1,10],'black',linewidth=2)    
    plot([4,4,6,6],[10,1,1,10],'black',linewidth=2)    
    plot([10,10,12,12],[10,1,1,10],'black',linewidth=2)    
    P=array([[0,x[0]],[0,1],[-6,0],[22,0],[16,1],[16,x[2]],[12,x[2]],[12,1]
            ,[10,1],[10,x[1]],[6,x[1]],[6,1],[4,1],[4,x[0]]])
    draw_polygon(P,ax,'blue')       
    P=array([[1,10],[1,x[0]],[1+0.1*u[0],x[0]],[1+0.1*u[0],10]])            
    draw_polygon(P,ax,'blue')
    P=array([[13,10],[13,x[2]],[13+0.1*u[1],x[2]],[13+0.1*u[1],10]])            
    draw_polygon(P,ax,'blue')
    w1, w2 = w.flatten()
    plot([0,4],[w1, w1],'red',linewidth=2)
    plot([12,16],[w2, w2],'red',linewidth=2)

def alpha(h):
    return a*sign(h)*sqrt(2*g*abs(h))

def B(x):
    h1, h2, h3 = x.flatten()
    B1 = -alpha(h1) - alpha(h1-h2)
    B2 = -alpha(h3) + alpha(h2-h3)
    return array([[B1,B2]]).T

def f(x,u):
    h1, h2, h3 = x.flatten()
    u1, u2 = u.flatten()
    dh1 = -alpha(h1) - alpha(h1-h2) + u1
    dh2 = alpha(h1-h2) - alpha(h2-h3)
    dh3 = -alpha(h3) + alpha(h2-h3) + u2 -perturbation
    return array([[dh1],[dh2],[dh3]])

    
dt = 0.05
x = array([[4],[5],[2]])
w = array([[7],[3]])
dw = zeros((2,1))
z = zeros((2,1))
u = zeros((2,1))
ax=init_figure(-10,25,-2,12)
a=0.4
g=9.81
perturbation=6

for t in arange(0,8,dt) :
    clear(ax)
    draw_pools(x,w)
    
    y = x[[0,2]]
    e = w - y
    v = z + 2*e + dw
    u = v - B(x)
    
    x = x + dt*f(x,u) 
    z = z + dt*e
    
print("h1 = ",round(y[0,0],3))
print("h3 = ",round(y[1,0],3))
