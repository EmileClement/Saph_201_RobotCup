# Saph_201_RobotCup

## Partie communication
On utilise une liaison série emulé par bluetouth.
Chaque commande est representé par un carractère:

| Character    | action |
| ---  | --- |
| a | `front + 1` |
| b | `front - 1` |
| A | `front + 10` |
| B | `front - 10` |
| c | `lat + 1` |
| etc | etc |
| S | `envoie du status` |
| Z | `tout a zéro` |
