from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

    
def draw(x):
    draw_tank(x,'darkblue',0.3)
    a,b = array([[-30],[0]]), array([[30],[0]])
    draw_segment(a,b,'red',2)
    
def f(x,u):
    θ=x[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])
        
def control_u(x):
    x1, x2, x3 = x.flatten()
    return -x3 - arctan(x2) - sin(x3)/(1+x2**2)

def control_vdp(x):
    x1, x2, x3 = x.flatten()
    a, b = vdp(x1,x2)
    da = sin(x3)
    db = -0.02*x1*x2*cos(x3) - (0.01*x1**2 - 1)*sin(x3) - cos(x3)
    y = sawtooth(x3 - arctan2(b,a))
    bx = (b*da - a*db)/(a**2+b**2)
    u = -y - bx
    return u

def f1(x1,x2):        
        return cos(-arctan(x2)), sin(-arctan(x2))

def vdp(x1,x2):
    return x2, -(0.01*x1**2 - 1)*x2 - x1

x=array([[-2],[-2],[3]])
dt= 0.05
s=10
ax=init_figure(-s,s,-s,s)
draw_field(ax,f1,-s,s,-s,s,1)


for t in arange(0,8,dt):
    clear(ax)
    draw_field(ax,f1,-s,s,-s,s,1)
    draw(x)
    u = control_u(x)
    x=x+dt*f(x,u)
    
pause(2)

x=array([[-2],[-3],[1]])
p = array([[-2],[-3]])
dt= 0.1
s=30
ax=init_figure(-s,s,-s,s)
draw_field(ax,vdp,-s,s,-s,s,1)

for t in arange(0,20,dt):
    clear(ax)
    draw_field(ax,vdp,-s,s,-s,s,1)
    draw(x)
    u = control_vdp(x)
    x=x+dt*f(x,u)
    p1, p2 = p.flatten()
    dp1, dp2 = vdp(p1,p2)
    p = p + dt*array([[dp1, dp2]]).T
    ax.scatter(p1,p2)