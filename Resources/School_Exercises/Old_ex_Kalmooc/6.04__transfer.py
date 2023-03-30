from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py



U = array([1,-1,1,-1,1,-1,1,-1])
Y = array([0,-1,-2,3,7,11,16,36])

M = zeros((6,4))

for i in range(6):
    M[i,0]= -Y[i+1]
    M[i,1]= -Y[i]
    M[i,2]= U[i+1]
    M[i,3]= U[i]
    
#Minv=inv(M.T@M)@M.T impossible car le déterminant de M est nul
#p=Minv@Y[2:]
print(M)
