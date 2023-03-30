from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x, u):
    x = x.flatten()
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    n3 = (x1**2+x2**2)**1.5
    v3 = (-x1/n3)+u*x3
    v4 = (-x2/n3)+u*x4
    return array([[x3], [x4], [v3], [v4]])


def control(x):
    x = x.flatten()
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    e1 = x1**2+x2**2-R**2
    e2 = x1*x3+x2*x4
    e3 = x3**2+x4**2-1/R
    u = -e1-5*e2-e3
    return u

dt = 0.1
s = 3
ax=init_figure(-s,s,-s,s)

R = 2.0
draw_disk(array([[0], [0]]), R, ax, "b", 0.1, 4)

draw_disk(array([[0],[0]]),0.2,ax,"blue",1,1)
x=array([[1.22],[0],[0],[1]])
draw_disk(array([[x[0]],[x[1]]]),0.1,ax,"red",1)

for t in arange(0, 15, dt):
    u = control(x)
    x = x+dt*(0.25*f(x, u)+0.75*(f(x+dt*(2/3)*f(x, u), u)))
    ax.scatter(x[0], x[1])
    pause(0.01)





 
