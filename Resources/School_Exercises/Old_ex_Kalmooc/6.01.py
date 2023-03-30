import numpy as np
import matplotlib.pyplot as plt

fig=plt.figure()

base1 = np.arange(-4,4,.5)
x, y = np.meshgrid(base1, base1)

base2 = np.arange(-4,4,.1)
x2, y2 = np.meshgrid(base2, base2)

fig.add_subplot(2, 2, 1)
grd = (y, x)
plt.quiver(x, y, grd[0], grd[1])

fig.add_subplot(2, 2, 2)
g=x2*y2
c=plt.contour(x2,y2,g)
plt.colorbar(c)

fig.add_subplot(2, 2, 3)
grd2=(4*x+y-1, x+8*y+1)
plt.quiver(x, y, grd2[0], grd2[1])

fig.add_subplot(2, 2, 4)
g=2*x2**2+x2*y2+4*y2**2+y2-x2+3
c=plt.contour(x2,y2,g)
plt.colorbar(c)
