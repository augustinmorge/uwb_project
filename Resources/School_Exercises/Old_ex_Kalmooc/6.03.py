import numpy as np
import matplotlib.pyplot as plt


U = np.array([[4],[10],[10],[13],[15]])     
T = np.array([[0],[1],[5],[5],[3]])
O = np.array([[5],[10],[8],[14],[17]])

M=np.concatenate((U,T),axis=1) # Mp=O

Minv=np.linalg.inv(M.T@M)@M.T # M inverse généralisée

p_mc=np.dot(Minv,O) # calcul des p1,p2,p3
p=np.round(p_mc,2)
print("\np1 = ",p[0][0],"\n\np2 = ",p[1][0])

Ov = p_mc[0][0]*U+p_mc[1][0]*T # valeurs filtrées

residu = Ov-O
print("\nResidus = ", np.round(residu.T,2))


O_U20_T10 = 20*p_mc[0][0] + 10*p_mc[1][0]
print("O_U20_T10 = ", O_U20_T10)


plt.plot(O,color="black") 
plt.plot(Ov,color="red")
plt.show()

