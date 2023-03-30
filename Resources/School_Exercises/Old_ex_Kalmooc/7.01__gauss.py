from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


x1, x2 = meshgrid(arange(-5,5,0.1),arange(-5,5,0.1))

xbar=array([[1],[2]])
Gx=eye(2,2)
invGx=inv(Gx)
dx1 = x1 - xbar[0]
dx2 = x2 - xbar[1]
Q = invGx[0,0]*dx1**2 + 2*invGx[0,1]*dx1*dx2 + invGx[1,1]*dx2**2
Z = exp(-Q/2)/(2*pi*sqrt(det(Gx)))


A=eulermat(pi/6,0,0)[1:,1:]@diag([1,2])
B=-array([[-2],[5]])

ybar=A@xbar + B
Gy=A@Gx@A.T
invGy=inv(Gy)
dy1 = x1 - ybar[0]
dy2 = x2 - ybar[1]
Qy = invGy[0,0]*dy1**2 + 2*invGy[0,1]*dy1*dy2 + invGy[1,1]*dy2**2
Zy = exp(-Qy/2)/(2*pi*sqrt(det(Gy)))


fig = figure()
ax = Axes3D(fig)
ax.plot_surface(x1,x2,Z,cmap='summer')
ax.plot_surface(x1,x2,Zy,cmap='summer')

fig = figure()
contour(x1,x2,Z)
contour(x1,x2,Zy)