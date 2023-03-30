#https://www.ensta-bretagne.fr/jaulin/robmooc.html
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from math import inf

def draw_room():
    for j in range(A.shape[1]):
        plot(array([A[0,j],B[0,j]]),array([A[1,j],B[1,j]]),color='blue')
        
def draw(p,y,col):
    draw_tank(p,'darkblue',0.1)
    p=p.flatten()
    y=y.flatten()
    for i in arange(0,8):
        plot(p[0]+array([0,y[i]*cos(p[2]+i*pi/4)]),p[1]+array([0,y[i]*sin(p[2]+i*pi/4)]),color=col)

def deter(u,v):
    return det(vstack((u,v)))

def f(p): # p = [x, y, theta]
    y = 100000*ones((8,1))   
    p = p.flatten()
    theta = p[2]
    for i in range(8):
        u = array([cos(theta+i*pi/4),sin(theta+i*pi/4)])
        m = p[:2]
        
        for j in range(len(A[0])):
            a = A[:,j]
            b = B[:,j]
            
            if deter(a-m,u)*deter(b-m,u) <= 0 and deter(a-m,b-a)*deter(u,b-a) >= 0 :
                d = deter(a-m,b-a)/deter(u,b-a)
                
                if d>0 and d<y[i]:
                    y[i]=d
            
    return y
         
        

A=array([[0, 7, 7, 9, 9, 7, 7, 4, 2, 0,   5, 6, 6, 5],
         [0, 0, 2, 2, 4, 4, 7, 7, 5, 5,   2, 2, 3, 3]])
B=array([[7, 7, 9, 9, 7, 7, 4, 2, 0, 0,   6, 6, 5, 5],
         [0, 2, 2, 4, 4, 7, 7, 5, 5, 0,   2, 3, 3, 2]])
y0=array([[6.4],[3.6],[2.3],[2.1],[1.7],[1.6],[3.0],[3.1]])                  


ax=init_figure(-2,10,-2,10)


                
p0 = array([[1],[1],[0]]) #initial guess
j0 = norm(y0-f(p0))
draw(p0,y0,'blue')
draw_room()
T = 2
pause(10)
while T > 0.01 and j0 > 0.1 :
    clear(ax)
    draw_room()

    pe=p0+T*randn(3,1)
    ye = f(pe)
    je = norm(y0-ye)
    draw(pe,ye,'red')

    if je<j0 :
        j0 = je
        p0 = pe
        y0 = ye

    draw(p0,y0,'blue')
    plt.text(0,8,"j0 = "+str(round(j0,2)))
    plt.text(0,7,"T = "+str(round(T,2)))
    T*=0.9
    pause(1)



