# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:02:24 2020

@author: Leopold
"""
import time
import math as m
import numpy as np
import serial
import evaluation.vecteur

Vecteur = evaluation.vecteur.Vecteur

class Robot():
    """
# Representation d'un robot dans Python

## Communication

### Referentiel utilise

L'asservissement de vitesse est réalise dans le referentiel du robot, donc avec les vecteurs:

* front, qui pointe vers l'avant du robot
* lat, qui pointe vers le coté gauche du robot
* rot, qui pounte vers le haut

La position du robot est realise dns le referentiel du robot a l'instant de l'initialisation. La methode `Robot.set_point_reference` permet de positioner l'origine du repère de position sur la position actuelle du robot

### Commande de vitesse

Les commances au robot sont envoyer avec le format suivant:
    `v_front, v_lat, v_rot, tir_front, tir_lat;`
On utilise des unites arbitraire

### Demande de status

L'etat des varriable interne est renvoyer avec le même formalisme que dans la commande de vitesse
    `S v_front, v_lat, v_rot, tir_front, tir_lat;\n`
On utilise des unites arbitraire

### Demande de positon

![Diagramme de sequance de la comunication](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/EmileClement/Saph_201_RobotCup/master/Com/doc/diagramme_sequance.uml&fmt=svg)
    """
    char_declancheur = ['S', 'G', 'R']
    """Liste des characteres anoncant un message du robot"""

    l = 0.2
    """Rayon du corps des robots"""
    R = 0.01
    """Rayon des roues des robot"""
    matrice_ref_local_roue = np.array([[0, 1/R, -l],
                                      [3**(1/2)/(2*R), -1/(2*R), -l],
                                      [-3**(1/2)/(2*R), -1/(2*R), -l]])

    def __init__(self, nom, com):
        """
        Parameters
        ----------
        nom : str
            Nom du robot, pas forcement utile
        com : str
            Port de comunication du robot, tres utile
        """
        self.nom = nom
        self.BT = serial.Serial(com, timeout=0.1)
        self.BT.writeTimeout = 0.1
        self.BT.baudrate = 115200
        self._commande_tir = [0, 0]
        self.commande_vit = Vecteur()
        self.commande_tir = (0, 0)
        self._position_gyro = Vecteur()
        self._position_roue = Vecteur()
        self.stop()
        self._message_en_attente = ""

    def __del__(self):
        self.BT.close()
        del self.BT

    def __repr__(self):
        return "{}|{}|C:{},{}".format(
            self.nom,
            self.position,
            self.commande_vit,
            self.commande_tir
            )

    def __str__(self):
        return self.__repr__()

    def _envoi(self, chaine):
        self.BT.write(chaine.encode('ASCII'))

    @property
    def commande_vit(self):
        """Commande actuel de vitesse du robot"""
        return self._commande_vit

    @commande_vit.setter
    def commande_vit(self, commande):
        """
        Setteur des commandes de vitesse.

        Envoie aussi les commandes au robot
        Parameters
        ----------
        frontal : float
            DESCRIPTION.
        lateral : float
            DESCRIPTION.
        rotation : float
            DESCRIPTION.
        """
        frontal, lateral, rotation = commande
        self._commande_vit = Vecteur(frontal, lateral, rotation)
        self._update_commande()

    @property
    def commande_tir(self):
        """Commande de tir actuel du robot"""
        return self._commande_tir

    @commande_tir.setter
    def commande_tir(self, commande):
        """Setteur des commande de tir"""
        front, lat = commande
        self._commande_tir = [front, lat]

    def _update_commande(self):
        chaine_comande = "{0},{1},{2},{3},{4};".format(self.commande_vit.x,
                                                       self.commande_vit.y,
                                                       self.commande_vit.theta,
                                                       self.commande_tir[0],
                                                       self.commande_tir[1])
        self._envoi(chaine_comande)

    def stop(self):
        """Stop le robot instantanément"""
        self.commande_vit = (0, 0, 0)

    def _demande_status(self):
        self.BT.write(b'S')

    def _demande_gyroscope(self):
        self.BT.write(b'G')

    def _demande_roue(self):
        self.BT.write(b'R')

    def _lire(self):
        return self.BT.read_all().decode("ASCII")

    def _lecteur(self):
        """Traitement du cahce de la liaison BlueTooth"""
        chaine_a_traiter = self._lire()
        for char in chaine_a_traiter:
            if char in Robot.char_declancheur:
                self._message_en_attente = char
            elif char == "\n":
                self._parsing()
                self._message_en_attente = ""
            else:
                self._message_en_attente += char

    def _parsing(self):
        chaine = self._message_en_attente
        declancheur = chaine[0]
        try:
            valeur = chaine[1:].split(",")
            valeur = [float(elem) for elem in valeur]
            if declancheur == 'G':
                self._position_gyro = Vecteur(valeur[0],
                                              valeur[1],
                                              valeur[2])
            elif declancheur == 'R':
                self._position_des_roues = Vecteur(valeur[0],
                                                   valeur[1],
                                                   valeur[2])
        except Exception:
            print('erreur du parsing depuis le robot {}'.format(self.nom))

    def set_point_reference(self):
        """La position actuel devient la position de reference pour la position"""
        self._envoi("R")

    @property
    def position(self):
        """Position du robot

        Il y a un temps de lattence car l'objet demande au robot une mise a jour de sa positon
        """
        self._demande_gyroscope()
        self._demande_roue()
        time.sleep(0.025)
        self._lecteur()
        return self.position_gyro

    @property
    def position_des_roues(self):
        """Position des trois roues du robot"""
        self._demande_roue()
        self.lecteur()
        return self._position_des_roues




# try:
#     del R
# except :
#     pass
# R = Robot("A", "COM7")
