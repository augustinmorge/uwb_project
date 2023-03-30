from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_quadrotor3D2(ax,x,R,α,l):
    Ca=hstack((circle3H(0.3*l),[[0.3*l,-0.3*l],[0,0],[0,0],[1,1]])) # the disc + the blades
    T = tran3H(*x[0:3]) @ ToH(R)
    C0= T @ tran3H(0,l,0)@eulerH(0,0,α[0])@Ca  # we rotate the blades
    C1= T @ tran3H(-l,0,0) @eulerH(0,0,-α[1])@Ca
    C2= T @ tran3H(0,-l,0) @eulerH(0,0,α[2])@Ca
    C3= T @ tran3H(l,0,0) @eulerH(0,0,-α[3])@Ca
    M = T @ add1(array([[l,-l,0,0, 0],[0,0,0,l,-l],[0,0,0,0,0]]))
    draw3H(ax,M,'grey',True,-1)  #body
    draw3H(ax,C0,'green',True,-1)
    draw3H(ax, C1, 'black', True,-1)
    draw3H(ax, C2, 'red', True,-1)
    draw3H(ax, C3, 'blue', True, -1)



def draw_quadri(x,R): # vecteur d'état x,y,z, angles d'Euler
    ax.clear()
    clean3D(ax,-30,30,-30,30,0,30)
    draw_quadrotor3D2(ax,x,R,α,5*l)    # we infate the robot, just to see something
    
        
def f_vdp(x):
    x1, x2 = x.flatten()[0:2]
    dx1 = x2
    dx2 = -(0.001*x1**2 - 1)*x2 - x1
    return array([[dx1, dx2]]).T

def traj_vdp(x0,y0,z):
    X = [x0]
    Y = [y0]
    for t in arange(0,60,dt):
        x1, x2 = X[-1], Y[-1]
        dx1 = x2
        dx2 = -(0.001*x1**2 - 1)*x2 - x1
        X.append(x1+dt*dx1)
        Y.append(x2+dt*dx2)
        if t%.5==0 :
            ax.scatter(x1,x2,10,color='red')

    
def f(x,R,w):

    vr=(x[3:6])
    wr=(x[6:9])
    w2=w*abs(w)
    τ=B@w2.flatten()
    
    dwr= inv(I)@(-adjoint(wr)@I@wr+τ[1:4].reshape(3,1))  
    R = R@expm(dt*adjoint(wr))
    dvr=-adjoint(wr)@vr+R.T@array([[0],[0],[g]])+array([[0],[0],[-τ[0]/m]])  
    dp=R@vr

    dx = vstack((dp,dvr,dwr))          
    return  dx, R

    
def control(x,R):   
    vr=(x[3:6])
    wr = x[6:9]
    px, py, pz = x.flatten()[0:3]
    dp=R@vr

    zd = -10
    vd = 10
    fd = f_vdp(x[0:2])
    
    td0 = 300*tanh(pz-zd) + 60*vr[2]
    φd = 0.5*tanh(10*sawtooth(angle(fd) - angle(dp))) 
    θd = -0.3*tanh(vd - vr[0])
    ψd = angle(dp)
    Rd = eulermat(φd,θd,ψd)
    
    # inverse block 3
    wrd = R.T@adjoint_inv(logm(Rd@R.T))
    
    # inverse block 2
    td13 = I@((200*(wrd-wr)) + adjoint(wr)@I@wr)
    
    # inverse block 1
    W2 = inv(B)@vstack(([td0], td13))
    w = sqrt(abs(W2))*sign(W2)
    
    return w

fig = figure()
ax = Axes3D(fig)
clean3D(ax,-30,30,-30,30,0,30)

m,g,b,d,l=10,9.81,2,1,1
I=array([[10,0,0],[0,10,0],[0,0,20]])
dt = 0.01  
B=array([[b,b,b,b],[-b*l,0,b*l,0],[0,-b*l,0,b*l],[-d,d,-d,d]])

x = array([[0,0,0, 10,0,0, 0,0,0]]).T  #x,y,z,  vr  wr (front,right,down)
R = eulermat(0,0,0)
α=array([[0,0,0,0]]).T #angles for the blades


for t in arange(0,1,dt):
    w=control(x,R)
    xdot, R = f(x,R,w)
    x  = x + dt*xdot
    draw_quadri(x,R)
    α=α+dt*10*w  
    pause(0.001)


# dessin du cycle

fig = figure()
ax = Axes3D(fig)
clean3D(ax,-30,30,-30,30,0,30)

x = array([[1,0,0, 10,0,0, 0,0,0]]).T  #x,y,z,  vr  wr (front,right,down)
R = eulermat(0,0,0)
α=array([[0,0,0,0]]).T #angles for the blades
            
for t in arange(0,60,dt):
    w=control(x,R)
    xdot, R = f(x,R,w)
    x  = x + dt*xdot
    if t%1==0 :
        draw_quadrotor3D2(ax,x,R,α,5*l)
    # draw_quadri(x,R)
    α=α+dt*10*w    
    
  
    
   
