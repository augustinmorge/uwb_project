from roblib import *

y = array([[8,7,0]]).T
C = array([[2,3],[3,2],[1,-1]])
Gbeta = diag([1,4,4])

xbar = array([[0,0]]).T
Gx = 10000*eye(2,2)

ybar = C@xbar
ytilde = y - ybar
Gy = C@Gx@C.T + Gbeta

K = Gx@C.T@inv(Gy)
xhat = xbar + K@ytilde

Geps = Gx - K@C@Gx

yhat = C@xhat
r = y - yhat

print("xhat = ",xhat)
print("yhat = ",yhat)
print("r = ",r)