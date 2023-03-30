from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


tmax=100
deltas=[0.1,0.01,0.001]
sub=[311,312,313]
col=['red','blue','green']

def sim(delta,sx,tmax):
    
    T=arange(0,tmax,delta)
    kmax=size(T)
    X=sx*randn(kmax)
    S=0*X
    
    for k in range(kmax-1):
        S[k+1] = S[k] + delta*X[k]
        
    return T, X, S

fig=figure()
fig.suptitle("Evolution of the standard deviation in function of delta and t")

for i in range(len(deltas)) :
    ax = fig.add_subplot(sub[i], aspect='equal')
    
    ax.xmin=0
    ax.xmax=tmax
    ax.ymin=-10
    ax.ymax=10
    clear(ax)
    plot([],color=col[i],label="delta = "+str(deltas[i]))
    legend()
    for j in range(10): 
        
        T, X, S = sim(deltas[i],1,tmax)
    
        plot(T, S, '+', color=col[i],ms=1)

fig=figure()
fig.suptitle("Brownian insensitive to delta changes")

for i in range(len(deltas)) :
    ax = fig.add_subplot(sub[i], aspect='equal')
    
    ax.xmin=0
    ax.xmax=tmax
    ax.ymin=-10
    ax.ymax=10
    clear(ax)
    plot([],color=col[i],label="delta = "+str(deltas[i]))
    legend()
    for j in range(10): 
        
       T, X, S = sim(deltas[i],1/sqrt(deltas[i]),tmax)
    
       plot(T, S, '+', color=col[i],ms=1)




