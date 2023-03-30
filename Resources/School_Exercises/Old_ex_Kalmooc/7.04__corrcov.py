from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

N=1000
xbar = array([[1],[2]])
Γx = array([[3,1],[1,3]])

ax=init_figure(-10,10,-10,10)
draw_ellipse(xbar,Γx,0.9,ax,[1,0.8,0.8])

x=randn(2,N)
# ax.scatter(x[0],x[1]) 

xa = xbar + sqrtm(Γx)@x
ax.scatter(xa[0],xa[1])

# xb=np.random.multivariate_normal(xbar.flatten(), Γx, N).T
# ax.scatter(xb[0],xb[1])

x1bar, x2bar = xbar.flatten()
Γx1x2 = Γx[0,1]
Γx2 = Γx[1,1]
Γx1 = Γx[0,0]
k1 = Γx1x2/Γx2 
k2 = Γx1x2/Γx1 

x2=array([-10,10])
x1 = x1bar + k1*(x2-x2bar)
plot(x1,x2,'red')

x1=array([-10,10])
x2 = x2bar + k2*(x1-x1bar)
plot(x1,x2,'green')