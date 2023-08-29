# src folder
***
## Calibration
Dans un premier temps il faut calibrer les cartes UWB.

Pour cela il faut répéter cette simple méthodologie :
    * On place un récepteur à une position fixe de 7.94m pour le channel 5 (cf doc dans biblio) et on exécute le code d'autocalibration dans le dossier Arduino (../)

## Simulation du Kalman
Pour estimer la position, un filtre de Kalman est utilisé.
Le code est un programme Python qui utilise le module roblib. Il définit plusieurs fonctions pour le contrôle et la navigation d'un robot qui suit des points de passage prédéfinis.

La fonction "f" est la fonction d'état du système, qui prend en entrée les états et les commandes actuels du robot et renvoie les dérivées des états.

La fonction "control" calcule les commandes nécessaires pour diriger le robot vers les points de passage prédéfinis. Cette fonction utilise une loi de commande en boucle fermée qui utilise la fonction "sawtooth" pour produire une sortie périodique et la fonction "inv" pour inverser une matrice.

La fonction "g" est la fonction de mesure du système, qui prend en entrée les états actuels du robot et retourne les mesures correspondantes. Elle est utilisée dans un filtre de Kalman pour estimer l'état du système à partir des mesures.

Le code définit également une liste de points de passage (Wps), qui est utilisée par les fonctions de contrôle et de mesure pour diriger le robot vers les points de passage et déterminer s'il est proche d'un point de passage donné. Enfin, le code utilise la bibliothèque matplotlib pour tracer les trajectoires du robot et les points de passage.

## Dataset
On a :
  * logs : contient différents dataset qui ont été récupréré par différents moyens : UDP/serial pour tester l'erreur en statique ou en absolu en comparant la distance réelle avec la distance mesurée.
  * logs_trolley : contient les datasets faits sur le parking par le chariot

<div style="text-align:center">
<p align="center">
  <img src="https://git.exail.com/users/augustin.morge_exail.com/repos/uwb_project/raw/imgs/setup.jpg?at=refs%2Fheads%2Fmain" width="750" title="Résultat de la calibration">
</p>
</div>