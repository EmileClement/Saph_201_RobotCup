# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:02:24 2020

@author: Leopold
"""
import serial
import time

class Robot():
    def __init__(self, nom, com):
        """
        Initialise une nouvelle instance de robot

        Parameters
        ----------
        nom : str
            Nom du robot, pas forcement utile
        com : str
            Port de comunication du robot
        """
        self.nom = nom
        self.BT = serial.Serial(com, timeout=0.1)
        self.BT.writeTimeout = 0.1
        self.BT.baudrate = 115200
        self.pos = [0, 0, 0]
        self.commande_vit = [0, 0, 0]
        self.commande_tir = [0, 0]
        self.vit_mbed = [0, 0, 0]
        self.tir_mbed = [0, 0]
        self.stop()
    
    def __del__(self):
        self.BT.close()
        del self.BT
        
    def __repr__(self):
        return "{}|{}|C:{},{}|Mbed:{},{}".format(
            self.nom,
            self.pos,
            self.commande_vit,
            self.commande_tir,
            self.vit_mbed,
            self.tir_mbed
            )
    
    def __str__(self):
        return self.__repr__()
 
    def _envoi(self, L_str):
        if not isinstance(L_str, list):
            L_str = [L_str]
        for elem in L_str:
            self.BT.write(elem.encode('ASCII'))
   
    def set_commande_vit(self, frontal, lateral, rotation):
        """
        Setteur des commandes. envoie aussi les commandes au robot

        Parameters
        ----------
        frontal : int
            DESCRIPTION.
        lateral : int
            DESCRIPTION.
        rotation : int
            DESCRIPTION.
        """
        self.commande_vit = [frontal, lateral, rotation]
        self._update_commande()
    
    def _update_commande(self):
        self._envoi(self._sequance(97, self.vit_mbed[0], self.commande_vit[0]))
        self._envoi(self._sequance(99, self.vit_mbed[1], self.commande_vit[1]))
        self._envoi(self._sequance(101, self.vit_mbed[2], self.commande_vit[2]))

    def stop(self):
        """
        Stop le robot instantanément

        Returns
        -------
        None.

        """
        self.set_commande_vit(0, 0, 0)
        self._envoi(10*"Z")
    
    def _demande_status(self):
        self.BT.write(b'S')

    def _sequance(self, id_dep, val_act, val_cible):
        """
                
        ord("a") = 97 - front
        ord("c") = 99 - lat
        ord("e") = 101 - rot
        ord("g") = 103 - tir_front
        ord("i") = 105 - tir_lat
        
        Parameters
        ----------
        id_dep : int
            Id du caractere de reference
        val_act : int
            valeur actuel du registre
        val_cible : int
            valeur cible du registre

        Returns
        -------
        str
            Chaine de caractere permetant de changer la valeur du registre

        """
        delta = val_cible - val_act
        L = []
        if delta == 0:
            return L
        if delta > 0:
            L += delta//10 * [id_dep - 32]
            L += delta%10 * [id_dep]
        else:
            delta *= -1
            L += delta//10 * [id_dep + 1 - 32]
            L += delta%10 * [id_dep + 1]
        return [chr(i) for i in L]

    def _lire(self):
        return self.BT.read_all().decode("ASCII")
    
    def update_status(self, timeout = 1):
    """
        Mets à jour la representation local des varriables du robot

        Parameters
        ----------
        timeout : float, optional
            temps en seconde avant la levé d'une erreur. The default is 1.

        Returns
        -------
        None.

        """
        txt = " "
        self._demande_status()
        T = time.time()
        while (txt[-1] != "\n"):
            if (time.time() - T < timeout) :
                raise TimeoutError
            txt += self._lire()
        assert txt[1] == "S"
        D = txt[2:-1].split(",")
        E = [int(s.split(".")[0]) for s in D]
        self.vit_mbed = E[:3]
        self.tir_mbed = E[3:]
        return self.vit_mbed

# try:    
#     del R
# except :
#     pass
# R = Robot("A", "COM4")
        