from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

P = 2*np.random.rand(500,2)

y = array([0, 1, 2.5, 4.1, 5.8, 7.5])

epsilon = 1

for p in P:
    
    a, b = p

    A = array([[1, 0],[a, 0.3]])
    B = array([[b],[1-b]])
    C = array([1, 1])
    
    x = array([[0],[0]])
    ym = array([0, 0, 0, 0, 0, 0])
    
    for i in range(6):
        ym[i]= C@x
        x = A@x + B
    
    if norm(ym - y, inf) < epsilon :
        scatter(a, b,color='red')
    else :
        scatter(a, b,color='black')


# 2. fonction de transfert = C@inv(z*I - A)@B

a1, b1 = 0.9, 0.75
A = arange(0,2,0.1)
B = []
for a in A :
    B.append(b1*(1+10*a1)/(1+10*a))
B = array(B)

plot(A,B)

