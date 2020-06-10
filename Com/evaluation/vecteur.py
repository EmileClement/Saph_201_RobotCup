# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:36:08 2020

@author: Leopold
"""
import numpy as np

class Vecteur():
    def __init__(self, x=0, y=0, theta=0):
        self.x, self.y, self.theta = (x, y, theta)


    def __add__(self, other):
        return Vecteur(self.x + other.x, self.y + other.y, self.theta + other.theta)

    def __mul__(self, X):
        return Vecteur(self.x * X, self.y * X, self.theta * X)

    def __rmul__(self, X):
        return self * X

    def __sub__(self, other):
        return self + ((-1) * other)

    def __repr__(self):
        return "({}, {}, {})".format(self.x, self.y, self.theta)

    def __abs__(self):
        N = 0
        N += (self.x)**2
        N += (self.y)**2
        N += (self.theta)**2
        return N**(1/2)

    def unitaire(self):
        if abs(self) == 0:
            return Vecteur()
        return self*(1/abs(self))

    def to_np_array(self):
        return np.array([self.x, self.y, self.theta])

class Vecteur_position(Vecteur):
    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        self._theta = (theta + 180)%360 - 180