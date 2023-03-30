from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],[u[0]],[u[1]]])
        
def control (x,w,dw):
    x=x.flatten()
    A = array([[-x[3]*sin(x[2]), cos(x[2])],
                  [x[3]*cos(x[2]), sin(x[2])]])
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])]])
    return inv(A) @ ((w - y) + 2*(dw - dy))

def b(i, n, t):
    return factorial(n)/(factorial(i)*factorial(n-i))*pow(1-t, n-i)*pow(t, i)

def db(i, n, t):
    if n == i:
        return n*t**(n-1)
    elif i == 0:
        return -n*(1-t)**(n-1)
    else:
        return factorial(n)/(factorial(i)*factorial(n-i))*(i*(1-t)**(n-i)*t**(i-1) - (n-i)*(1-t)**(n-i-1)*t**i)

def setpoint(t):
    w = zeros((2, 1))
    for i in range(0, n+1):
        w = w + b(i, n, t)*(P[:, i].reshape(2, 1))
    return w

def dsetpoint(t):
    dw = zeros((2, 1))
    for i in range(0, n+1):
        dw = dw + db(i, n, t)*(P[:, i].reshape(2, 1))
    return dw

def draw():
    clear(ax)
    plot(P[0], P[1], 'or')
    A1=array([[2,0],[4,2],[2,7]])
    A2=array([[7,2],[8,3],[3,10]])
    draw_polygon(A1,ax,'green')
    draw_polygon(A2,ax,'green')

P = array([[1,1,1,1,2, 3,4,5,4,8,10,8],
           [1,4,7,9,10,8,6,4,0,0,0,8]])
n = len(P[0])-1

ax=init_figure(-1,11,-1,11)

dt = 0.1
x = array([[0,0,0,1]]).T
tmax = 25
for t in arange(0,tmax,dt):
    w = setpoint(t/tmax)
    dw = dsetpoint(t/tmax)/tmax
    u = control(x,w,dw)
    plot(w[0],w[1], 'm.')
    x = x+f(x,u)*dt
    draw()
    draw_tank(x,'darkblue',0.2)
    pause(0.01)

