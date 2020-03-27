# Saph_201_RobotCup

## Partie communication
On utilise une liaison série emulé par bluetouth.
on utilise les chaines suivante pour emmetre les commandes depuis le PC `A vfr, vlat, vrot, tfr, tlat;`. ici `vfr`, `vlat` et `vrot` sont des entier qui represente les commandes de vitesse et `tfr` et `tlat` sont les commandes de tire, qui seront amener à changer.
De plus, si ont envoie la chaine `C`, le mbed renvoie une chaine de carractères representant sont états, càd les commandes qu'il a en mémoire. On pourras utiliser un autre carractère pour récupérer les données de l'integration de l'accéléromètre.