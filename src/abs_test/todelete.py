import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

# Définir les points de la ligne id
id = np.arange(-10000, 10000, 1)

# Définir la formule de y1
y1 = 7/22.8*id -60.984

# Calculer les valeurs de y2
y2 = y1 + 2.334*(y1+88)

# Tracer la ligne id en bleu
ax.plot(id, id, label='Actual RX LEVEL', color='blue')

# Tracer la ligne y1 en rouge
ax.plot(id, y1, label='Estimated RX LEVEL', color='red')

# Tracer la ligne y2 en vert
ax.plot(id, y2, label='Correction', color='green')

# Ajouter une légende
ax.legend()
ax.set_xlim([-105,-65])
ax.set_ylim([-105,-65])
ax.set_ylabel("Estimated RX LEVEL (dBm)")
ax.set_xlabel("Actual RX LEVEL (dBm)")
ax.grid()

# Afficher le graphe
plt.show()
