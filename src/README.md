# src folder
***
## Calibration
Dans un premier temps il faut calibrer les cartes UWB.

Pour cela il faut répéter cette simple méthodologie :
    * On place un récepteur à une position fixe
    * On fait varier l'émetteur en distance (ici tous les 50 cm) et on mesure sa distance

Pour cela on peut utiliser le code `calibration.py`.

Cela nous donne le résulat suivant :

<div style="text-align:center">
<p align="center">
  <img src="https://github.com/augustinmorge/uwb_project/blob/main/src/logs/log_cali/Test_on_2023_03_30_09_35_46.png" width="750" title="Résultat de la calibration">
</p>
</div>

## Simulation du Kalman
Pour estimer la position, un filtre de Kalman est utilisé.
Le code est un programme Python qui utilise le module roblib. Il définit plusieurs fonctions pour le contrôle et la navigation d'un robot qui suit des points de passage prédéfinis.

La fonction "f" est la fonction d'état du système, qui prend en entrée les états et les commandes actuels du robot et renvoie les dérivées des états.

La fonction "control" calcule les commandes nécessaires pour diriger le robot vers les points de passage prédéfinis. Cette fonction utilise une loi de commande en boucle fermée qui utilise la fonction "sawtooth" pour produire une sortie périodique et la fonction "inv" pour inverser une matrice.

La fonction "g" est la fonction de mesure du système, qui prend en entrée les états actuels du robot et retourne les mesures correspondantes. Elle est utilisée dans un filtre de Kalman pour estimer l'état du système à partir des mesures.

Le code définit également une liste de points de passage (Wps), qui est utilisée par les fonctions de contrôle et de mesure pour diriger le robot vers les points de passage et déterminer s'il est proche d'un point de passage donné. Enfin, le code utilise la bibliothèque matplotlib pour tracer les trajectoires du robot et les points de passage.

## Test en réel 
TODO

## Caractérisation des erreurs
TODO
