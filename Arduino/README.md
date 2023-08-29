# Programme Arduino pour les cartes ESP32

Ce référentiel contient les programmes principaux pour gérer les codes Arduino à flasher sur les cartes ESP32. Vous trouverez ci-dessous une brève description de chaque dossier et programme inclus dans ce référentiel :

## Programme d'autocalibration par dichotomie (ESP32_anchor_autocalibrate)

Ce programme implémente une méthode d'autocalibration par dichotomie pour les ancres utilisées dans le système. L'autocalibration est un processus essentiel pour garantir une localisation précise dans les applications utilisant la technologie UWB (Ultra-Wideband).

## Ancres

Ce dossier contient les programmes pour configurer les cartes ESP32 en tant qu'ancres dans le système de localisation. Voici les sous-dossiers inclus :

### Données brutes par série (ESP32_UWB_setup_anchor)

Ce dossier contient le programme pour récupérer les données brutes des ancres via une connexion série (UART). Les données brutes peuvent être utilisées pour effectuer des analyses et des ajustements supplémentaires.

### Données par UDP (ESP32_UWB_setup_anchor_udp)

Ce dossier contient le programme pour envoyer les données des ancres via UDP (User Datagram Protocol). L'utilisation d'UDP permet une communication efficace avec d'autres périphériques ou systèmes.

## Balises

Ce dossier contient les programmes pour configurer les cartes ESP32 en tant que balises dans le système de localisation. Voici les sous-dossiers inclus :

### Données brutes par série (ESP32_UWB_setup_tag)

Ce dossier contient le programme pour récupérer les données brutes des balises via une connexion série (UART). Ces données brutes peuvent être utiles pour diverses analyses et traitements ultérieurs.

### Données par UDP (ESP32_UWB_setup_tag_udp)

Ce dossier contient le programme pour envoyer les données des balises via UDP (User Datagram Protocol). L'envoi des données via UDP facilite l'intégration avec d'autres composants du système.

### Données par série avec le protocole LBL (ESP32_UWB_setup_tag_geo)

Ce dossier contient le programme pour envoyer les données des balises par série en utilisant le protocole LBL (Localisation-Based Localization). Ce protocole est particulièrement utile pour une localisation plus précise dans certains scénarios.

### Moyennage des trois dernières valeurs (ESP32_UWB_setup_tag_udp_mean)

Ce dossier contient le programme qui effectue le moyennage des trois dernières valeurs de localisation des balises. Bien que ce programme soit le programme par défaut, il n'est actuellement pas utilisé dans le système.

N'hésitez pas à explorer chaque dossier pour en savoir plus sur les fonctionnalités spécifiques de chaque programme. Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à nous contacter.

**Note :** Assurez-vous de disposer des connaissances appropriées en programmation Arduino et en technologie UWB avant de flasher ces programmes sur les cartes ESP32. Une utilisation incorrecte peut entraîner un fonctionnement incorrect du système ou endommager le matériel.
