# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:04:14 2020

@author: Leopold
"""
import time
import evaluation.vecteur
from RobotV1 import Robot

Vecteur = evaluation.vecteur.Vecteur
Vecteur_position = evaluation.vecteur.Vecteur_position

cible = Vecteur_position(1)

R = Robot('Testeur', 'COM4')

pos = [R.position]

pressision_pos = 0.05

while abs(pos[-1] - cible) > pressision_pos:
    erreur = cible - pos[-1]
    R.commande_vit(100 * erreur)
    pos.append(R.position)
    time.sleep(0.05)

R.stop()