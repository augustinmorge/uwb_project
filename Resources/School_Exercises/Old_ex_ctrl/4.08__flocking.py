from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    θ = x[2]
    return array([[cos(θ)], [sin(θ)], [u]])

def sim(alignement,cohesion,repulsion,m,txt):
    
    
    X   = 20*randn(3,m)
    dt  = 0.2
    for t in arange(0,20,dt):
        clear(ax)
        ax.set_title(txt)
        for i in range(m):
            
            H = zeros((2,2*(m-1)))
            k = 0
            for j in range(m):
                if j!=i :
                    θj = X[2,j]
                    H[0,k] = alignement*cos(θj)
                    H[1,k] = alignement*sin(θj)
                    k+=1
                    dp = array([X[0,i]-X[0,j],X[1,i]-X[1,j]])
                    v = cohesion*dp + repulsion*dp/(norm(dp)**3)
                    v = v/norm(v)
                    H[:,k] = v
                    k+=1
            Hbar = mean(H,1)
            u=sawtooth(angle(Hbar)-X[2,i])
            
            xi=X[:,i].flatten()
            xi=xi.reshape(3,1)
            draw_tank(xi,'b')
            xi=xi+f(xi,u)*dt        
            X[:,i]  = xi.flatten()        

m   = 20

ax=init_figure(-60,60,-60,60)

texte = "Avec les 3 lois de Reynolds"
alignement,cohesion,repulsion = 1, -0.01, 30
sim(alignement,cohesion,repulsion,m,texte)
pause(1)
texte = "Sans alignement"
alignement,cohesion,repulsion = 0, -0.01, 30
sim(alignement,cohesion,repulsion,m,texte)
pause(1)
texte = "Sans cohesion"
alignement,cohesion,repulsion = 1, 0, 30
sim(alignement,cohesion,repulsion,m,texte)
pause(1)
texte = "Sans repulsion"
alignement,cohesion,repulsion = 1, -0.01, 0
sim(alignement,cohesion,repulsion,m,texte)