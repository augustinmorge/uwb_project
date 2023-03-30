import numpy as np
import matplotlib.pyplot as plt

t = np.array([[-3],[-1],[0],[2],[3],[6]])     
y = np.array([[17],[3],[1],[5],[11],[46]])

M=np.concatenate((t**2,t,np.ones((len(t),1))),axis=1) # Mp=y

Minv=np.linalg.inv(M.T@M)@M.T # M inverse généralisée

p_mc=np.dot(Minv,y) # calcul des p1,p2,p3
p=np.round(p_mc,2)
print("\np1 = ",p[0][0],"\n\np2 = ",p[1][0],"\n\np3 = ",p[2][0])

yv = p_mc[0][0]*t**2+p_mc[1][0]*t+p_mc[2][0] # valeurs filtrées

residu = yv-y
print("\nResidus = ", np.round(residu.T,2))

plt.plot(t,y,color="black") 
plt.plot(t,yv,color="red")
plt.show()