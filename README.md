# Saph_201_RobotCup

## Partie communication
On utilise une liaison série emulé par bluetouth.
Chaque commande est representé par un carractère:

| Character    | action |
| ---  | --- |
| S | `envoie du status` |
| Z | `tout a zéro` |
| G | `demande de la position par le gyroscope` |
| R | `demande de la position par les roues` |
![Diagramme de sequance de la comunication](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/EmileClement/Saph_201_RobotCup/master/Com/doc/diagramme_sequance.uml&fmt=svg)
