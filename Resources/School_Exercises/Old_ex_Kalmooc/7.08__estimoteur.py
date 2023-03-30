from roblib import *


xbar = array([[1,-1]]).T
sig2x = 4
Gx = sig2x*eye(2,2)

U = array([[4, 10, 10, 13, 15]]).T
Tr = array([[0, 1, 5, 5, 3]]).T
y = array([[5, 10, 8, 14, 17]]).T
C = hstack((U,Tr))

sig2y = 9
Gbeta = sig2y*eye(5,5)

ytilde = y - C@xbar
Gy = C@Gx@C.T + Gbeta

K = Gx@C.T@inv(Gy)
xhat = xbar + K@ytilde

Geps = Gx - K@C@Gx

yhat = C@xhat
r = y - yhat

print("xhat = ",xhat)
print("yhat = ",yhat)
print("r = ",r)