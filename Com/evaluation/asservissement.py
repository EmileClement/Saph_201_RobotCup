# -*- coding: utf-8 -*-
"""
Created on Fri May 15 10:03:10 2020

@author: Leopold
"""
from vecteur import Vecteur

dt = 0.001
v_max = 0.5
acc_max = 10000
def aller_a(cible, rep, precision, arret = False, divergence = 3):
    pos, vit = rep
    pres_pos, pres_vit = precision
    while ((abs(pos[-1] - cible) >= pres_pos) or ((abs(vit[-1]) >= pres_vit)) and arret) and (abs(pos[-1]) <= divergence):
        erreur = cible - pos[-1]
        commande = asservissement(erreur, rep)
        pos.append(pos[-1] + vit[-1] * dt)
        next_acc = vit[-1] + commande * dt
        if abs(next_acc) >= acc_max:
            next_acc = next_acc.unitaire() * acc_max
        vit.append(vit[-1] + next_acc * dt)

def asservissement(erreur, rep):
    pos, vit = rep
    return 1 * erreur - 50 * vit[-1]

#cibles = [Vecteur(rd.randint(0, 200) / 100, rd.randint(0, 200) / 100) for _ in range(15)]
cibles =[Vecteur(1), Vecteur(1, 1)]
pos_initial = Vecteur()
pos = [pos_initial]
vit = [Vecteur()]

try:
    for cible in cibles:
        aller_a(cible, (pos, vit), (0.01, 1))
except KeyboardInterrupt:
    pass
aller_a(Vecteur(), (pos, vit), (0.001, 0.001), True)
print(len(pos))
from matplotlib import pyplot as plt

plt.plot([elem.x for elem in pos], [elem.y for elem in pos], '-k')
for cible in cibles:
    plt.plot(cible.x, cible.y, "xr")
plt.show()
