from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

y = array([[0.38,3.25,4.97,-0.26]]).T

sigy = 0.1
Gbeta = sigy**2*eye(4,4)

Tm = array([[1,2,3,7]]).T
C = hstack((ones((4,1)), -cos(Tm)))

pbar = array([[0,0]]).T
sig2p = 10000
Gp = sig2p*eye(2,2)

ytilde = y - C@pbar
Gy = C@Gp@C.T + Gbeta

K = Gp@C.T@inv(Gy)
phat = pbar + K@ytilde

Geps = Gp - K@C@Gp

yhat = C@phat
r = y - yhat

print("phat = ",phat)
print("yhat = ",yhat)
print("r = ",r)

ax=init_figure(-3,40,-3,8)
p=phat.flatten()
t = arange(0,20,0.1)
plot(p[0]*t - p[1]*sin(t) , p[0] - p[1]*cos(t),'green')

fig=figure()
plot(t,p[0] - p[1]*cos(t),'blue')
plot(Tm,y,'ro')

