from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
    
def draw_ellipse2(c,Γ,η,ax,col): # Gaussian confidence ellipse with artist
    #draw_ellipse(array([[1],[2]]),eye(2),0.9,ax,[1,0.8-0.3*i,0.8-0.3*i])
    if (norm(Γ)==0):
        Γ=Γ+0.001*eye(len(Γ[1,:]))
    A=sqrtm(-2*log(1-η)*Γ)    
    w,v=eig(A)    
    v1=array([[v[0,0]],[v[1,0]]])
    v2=array([[v[0,1]],[v[1,1]]])        

    f1=A @ v1
    f2=A @ v2      
    φ =  (arctan2(v1 [1,0],v1[0,0]))
    α=φ*180/3.14
    e = Ellipse(xy=c, width=2*norm(f1), height=2*norm(f2), angle=α)   
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    
    e.set_alpha(0.7)
    e.set_facecolor('none')
    e.set_edgecolor(col)

#Q3
# dg(x0)/dx = [[2(px0 - xa), 0, 2(py0 - ya), 0], = C
#              [2(px0 - xb), 0, 2(py0 - yb), 0]]   
# y - g(x0) + Cx0 = Cx
           
def g(x):
    g1 = norm(x[::2,:]-a)**2
    g2 = norm(x[::2,:]-b)**2
    return(array([[g1],[g2]]))

def kalman_ext(xhat,Gx,uk,y,Γα,Γβ,Ak):
    C = array([[2*(xhat[0,0] - a[0,0]), 0, 2*(xhat[2,0] - a[1,0]), 0],
                [2*(xhat[0,0] - b[0,0]), 0, 2*(xhat[2,0] - b[1,0]), 0]])
    z = y - g(xhat) + C@xhat
    return kalman(xhat,Gx,uk,z,Γα,Γβ,Ak,C)
dt = 0.02
Γα = diag([0,dt,0,dt])
Γβ = eye(2)
x  = array([[-4],[1],[4],[-1]])
a = array([[0,0]]).T
b = array([[1,0]]).T
Ak=array([[1,dt,0,0],[0,1-0.01*dt,0,0],[0,0,1,dt],[0,0,0,1-0.01*dt]])
xbadhat = array([[0],[0],[15],[0]])
Gxbad = 10000*eye(4,4)
xgoodhat = array([[-3],[0],[3],[0]])
Gxgood = 10000*eye(4,4)
ax=init_figure(-5,5,-5,5)
for t in arange(0,5,dt) :
    clear(ax)
    y = g(x) +  mvnrnd1(Γβ)
    uk=array([[0]]*4)
    
    plot(a[0],a[1],'ro')
    plot(b[0],b[1],'go')
    plot(x[0,0],x[2,0],'bo')    
    draw_disk(a,sqrt(y[0,0]),ax,[0.8,0.8,0.8])
    draw_disk(b,sqrt(y[1,0]),ax,[0.8,0.8,0.8])   
    
    xbadhat, Gxbad = kalman_ext(xbadhat,Gxbad,uk,y,Γα,Γβ,Ak)
    draw_ellipse2(xbadhat[0::2],Gxbad[0::2,0::2],0.9,ax,'red')
    xgoodhat, Gxgood = kalman_ext(xgoodhat,Gxgood,uk,y,Γα,Γβ,Ak)
    draw_ellipse2(xgoodhat[0::2],Gxgood[0::2,0::2],0.9,ax,'blue')
    
    x = Ak @ x + mvnrnd1(Γα)
