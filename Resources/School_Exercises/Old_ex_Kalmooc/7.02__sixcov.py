from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def draw_ellipse2(c,Γ,η,ax,col): # Gaussian confidence ellipse with artist
    #draw_ellipse(array([[1],[2]]),eye(2),0.9,ax,[1,0.8-0.3*i,0.8-0.3*i])
    if (norm(Γ)==0):
        Γ=Γ+0.001*eye(len(Γ[1,:]))
    A=sqrtm(-2*log(1-η)*Γ)    
    w,v=eig(A)    
    v1=array([[v[0,0]],[v[1,0]]])
    v2=array([[v[0,1]],[v[1,1]]])        

    f1=A @ v1
    f2=A @ v2      
    φ =  (arctan2(v1 [1,0],v1[0,0]))
    α=φ*180/3.14
    e = Ellipse(xy=c, width=2*norm(f1), height=2*norm(f2), angle=α)   
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    
    e.set_alpha(0.7)
    e.set_facecolor('none')
    e.set_edgecolor(col)

A1 = diag([1,3])
A2 = eulermat(pi/4,0,0)[1:,1:]

G1 = eye(2,2) #matrice identité donc cercle
G2 = 3*G1 # x3 donc le cercle plus grand
G3 = A1 @ G2 @ A1.T + G1
G4 = A2 @ G3 @ A2.T
G5 = G4 + G3
G6 = A2 @ G5 @ A2.T
c= [0,0]
η = 0.9
G = [G1,G2,G3,G4,G5,G6]
col = ['r','g','b','y','m','black']
d = 15
ax = init_figure(-d,d,-d,d)

for i in range(len(G)):
    draw_ellipse2(c,G[i],η,ax,col[i])
    plot([],color=col[i],label="G"+str(i+1))
legend()