# -*- coding: utf-8 -*-
"""
.. module:: test_network.py
   :platform: Unix, Windows
   :synopsis: Unit testing for the network module.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>

"""

import os
import sys
sys.path.insert(0, os.path.abspath('../pyLearnstimate'))
from pyLearnstimate import network as net
import random as rn

#%% Seed that random generator!
rn.seed(123)

#%% Test genetics

test = net.Allele()
test.generateNetwork()
for i in range(4):
    print(test.evaluateNetwork([1]*4))