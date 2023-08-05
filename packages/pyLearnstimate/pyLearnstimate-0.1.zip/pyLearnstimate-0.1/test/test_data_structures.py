# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:03:54 2017

@author: sap625
"""

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
#import pyLearnstimate as pl
#from pyLearnstimate import data_structures as ds
from pyLearnstimate import *

#%% Test for the single link list class
s = data_structures.SingleList()
s.append(31)
s.append(2)
s.append(3)
s.append(4)
 
s.show()
s.remove(31)
s.remove(3)
s.remove(2)
s.show()

#%% Test for the doubly-linked list class and its accompanying Node class

#d = pl.data_structures.DoubleList()
#d = ds.DoubleList()
d = data_structures.DoubleList() 

d.append(5)
d.append(6)
d.append(50)
d.append(30)
 
d.show()
 
d.remove(50)
d.remove(5)
 
d.show()
#t.show()

#%% Test for linked lists and genetics

