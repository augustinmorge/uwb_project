from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x1,x2):        
    return -(x1**3+x2**2*x1-x1+x2),-(x2**3+x1**2*x2-x1-x2)

def fA(A,x1,x2):
    B = inv(A)
    y1 = B[0,0]*x1 + B[0,1]*x2
    y2 = B[1,0]*x1 + B[1,1]*x2
    z1,z2 = f(y1,y2)
    v1 = A[0,0]*z1 + A[0,1]*z2
    v2 = A[1,0]*z1 + A[1,1]*z2
    return v1, v2

xmin,xmax,ymin,ymax=-2.5,2.5,-2.5,2.5 
ax=init_figure(xmin,xmax,ymin,ymax)
ax.set_title("Q3")
draw_field(ax,f,xmin,xmax,ymin,ymax,0.3)    
dt=0.05
x=array([[0.5],[0]])
for t in arange(0,20,dt):
    x1,x2=x[0,0],x[1,0]
    dx1,dx2=f(x1,x2)
    x=x+dt*array([[dx1],[dx2]])
    ax.scatter(x1,x2,1.6,color='red')

pause(2)    

clear(ax)
ax.set_title("Q5")

Mx = arange(xmin, xmax, 0.3)
My = arange(ymin, ymax, 0.3)
X1, X2 = meshgrid(Mx, My)

# Changement sens de rotation
S = array([[1, 0], [0, -1]])

# Déformation en ellipse
D = array([[2, 0], [0, 1]])

# Rotation
theta = pi/4  
R = array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]) 

# Transformation linéaire
A = R @ D @ S
VX, VY = fA(A, X1, X2)  
R = sqrt(VX ** 2 + VY ** 2)  
quiver(Mx, My, VX / R, VY / R) 
dt = 0.05
x = array([[0], [0.5]])
for t in arange(0, 20, dt):
    x1, x2 = x[0, 0], x[1, 0]
    dx1, dx2 = fA(A, x1, x2)
    x = x + dt * array([[dx1], [dx2]])
    ax.scatter(x1, x2, 1.6, color="red")







