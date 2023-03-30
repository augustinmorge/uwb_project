from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from numpy.linalg import pinv

ax=init_figure(-5,15,-5,15)
m=30
P=10*rand(2,m)
plot(P[0,:],P[1,:],'ob')

C = array([[0], [0], [0]])
K = [] 

for i in range(0, m-2):
    for j in range(i+1, m-1): 
        for k in range(j+1, m): 
            p = P[:, [i, j, k]] 
            M = hstack((2*p.T, - ones((3, 1))))
            A = sum(p**2, 0).reshape(3, 1)
            c = pinv(M)@A  
            r = sqrt(norm(c[0:2, 0])**2-c[2, 0]) 
            # draw_disk(c[0:2, 0], r, ax, 'green', 1)

            # Sélection des triangles
            
            valid = True
            for q in range(0, m):
                valid = valid and (q == i or q == j or q == k or norm(P[:, q]-c[0:2, 0]) > r)
            if valid:
                #draw_disk(c[0:2, 0], r, ax, 'red', 0.2)
                plot(p[0, [0, 1, 2, 0]], p[1, [0, 1, 2, 0]], 'g:')
                C = hstack((C, c))
                K.append(array([i, j, k]).T)


def ismember(A, B):
    return [sum(a == B) for a in A]

def isvoisin(x,y):
    return sum(ismember(x, y)) == 2

ax.set_title("Diagramme de Voronoi")

for i in range(len(K)):
    for j in range(len(K)):
        if isvoisin(K[i],K[j]):
            plot(C[0, [i+1, j+1]], C[1, [i+1, j+1]], 'red', 3)


