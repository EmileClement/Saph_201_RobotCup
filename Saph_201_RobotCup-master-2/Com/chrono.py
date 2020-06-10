# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:08:56 2020

@author: Leopold
"""
from Robot import *
try:
    assert isinstance(R, Robot)
except :
    R = Robot("A", "COM4")

import time
print('start')
T = time.time()
R.set_commande_vit(10, 42, 32)
R.update_status()
print('end - {}s'.format(time.time() - T))