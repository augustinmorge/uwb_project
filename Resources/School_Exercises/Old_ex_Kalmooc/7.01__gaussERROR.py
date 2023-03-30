from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py



x1 = arange(-5,5,0.1)
x2 = arange(-5,5,0.1)
x=vstack((x1,x2))
Gx=eye(2,2)
xbar=array([[1],[2]])
xbars=xbar*ones(100)
xtilde=x-xbar



Q = xtilde.T@inv(Gx)@xtilde

Z = exp(-Q/2)/(2*pi*sqrt(det(Gx)))

x1, x2 = meshgrid(x1,x2)

# fig = figure()
# ax = Axes3D(fig)
# ax.plot_surface(x1,x2,Z)
# fig = figure()
# contour(x1,x2,Z)

invGx=inv(Gx)
dx1 = x1 - xbar[0]
dx2 = x2 - xbar[1]
Q2 = invGx[0,0]*dx1**2 + 2*invGx[0,1]*dx1@dx2 + invGx[1,1]*dx2**2
Z2 = exp(-Q2/2)/(2*pi*sqrt(det(Gx)))

fig = figure()
ax = Axes3D(fig)
ax.plot_surface(x1,x2,Z2)
fig = figure()
contour(x1,x2,Z2)