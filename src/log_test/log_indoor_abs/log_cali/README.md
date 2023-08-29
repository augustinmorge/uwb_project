# A ajouter :
***
Pour pouvoir appliquer Anchor_autocalibrate et réinitialiser le delai d'antenne :

A la fin de la foncton `set_antenna_delay`dans DW1000.cpp :

    // added by SJR -- commit to device register (see function commitConfiguration())
	byte antennaDelayBytes[DW1000Time::LENGTH_TIMESTAMP];
	_antennaDelay.getTimestamp(antennaDelayBytes);
	writeBytes(TX_ANTD, NO_SUB, antennaDelayBytes, LEN_TX_ANTD);
	writeBytes(LDE_IF, LDE_RXANTD_SUB, antennaDelayBytes, LEN_LDE_RXANTD);
	// added by SJR

***
On peut aussi modifier et doubler le TX_POWER à 0x28 (line 885 dans DW1000.cpp)

## Notes à part :
### DW1000Class::getReceivePower
Cette fonction est une méthode de la classe DW1000, qui permet de mesurer la puissance du signal reçu par le module DW1000 lors de la réception d'un message. Elle utilise les données reçues pendant la réception du message pour calculer la puissance du signal.

Plus précisément, cette méthode récupère les valeurs du tableau cirPwrBytes et de rxFrameInfo, qui sont des informations sur la qualité du signal reçu, stockées dans le module DW1000 pendant la réception du message. Ensuite, elle utilise ces valeurs pour calculer la puissance du signal en utilisant une formule qui dépend de la fréquence d'émission du signal (16 MHz ou 64 MHz) et de coefficients de correction.

La méthode retourne un flottant représentant la puissance du signal reçu en décibels (dBm). Si cette valeur est inférieure ou égale à -88 dBm, cela signifie que le signal reçu est très faible, et donc la méthode retourne cette valeur. Sinon, elle applique une correction pour améliorer la précision de la mesure et retourne la valeur corrigée.

### DW1000Class::getFirstPathPower
Cette fonction est une méthode de la classe DW1000Class qui permet de calculer la puissance du premier chemin d'arrivée (en anglais : First Path Power ou FPP) reçue par le module de communication radio DW1000.

La fonction utilise les informations reçues dans le paquet radio pour extraire les amplitudes du premier, deuxième et troisième chemins d'arrivée (en anglais : First Path Amplitude 1, 2 et 3 ou FPA1, FPA2 et FPA3). Ensuite, elle calcule la puissance de chaque chemin en les additionnant et en les divisant par le carré de la norme de la réponse impulsionnelle (en anglais : Channel Impulse Response ou CIR) du canal de communication. Le résultat est corrigé en fonction de la fréquence d'impulsion (16 MHz ou 64 MHz) et de l'amplitude mesurée.

Si le résultat de la puissance du premier chemin est inférieur à -88 dBm, il est retourné tel quel. Sinon, il est corrigé en utilisant une approximation de la courbe de correction de la puissance dBm (Figure 22 dans le manuel d'utilisation du DW1000) pour compenser l'erreur de mesure. Finalement, la fonction retourne la puissance estimée du premier chemin en dBm.

### Différence RX/FP
Les fonctions getFirstPathPower() et getReceivePower() sont toutes les deux des méthodes de la classe DW1000Class qui permettent de mesurer la puissance du signal reçu par le module UWB (Ultra Wide Band). Cependant, elles mesurent des aspects différents de la puissance du signal reçu.

La fonction getReceivePower() mesure la puissance globale du signal reçu par le module UWB. Elle utilise les informations contenues dans les champs CIR_PWR et RX_FINFO pour calculer la puissance du signal reçu en dBm.

La fonction getFirstPathPower(), quant à elle, mesure la puissance du premier trajet (ou path) du signal reçu. Le premier trajet est le trajet direct du signal depuis l'émetteur jusqu'au récepteur, sans qu'il y ait eu de réflexions sur les obstacles ou les murs environnants. Elle utilise les informations contenues dans les champs FP_AMPL1, FP_AMPL2, FP_AMPL3 et RX_FINFO pour calculer la puissance du premier trajet du signal reçu en dBm.

En résumé, la fonction getReceivePower() mesure la puissance globale du signal reçu, tandis que la fonction getFirstPathPower() mesure la puissance du premier trajet du signal reçu.