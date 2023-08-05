# -*- coding: utf-8 -*-
"""
.. module:: test_genetics.py
   :platform: Unix, Windows
   :synopsis: Unit testing for the genetics module.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>

"""

#%% Import all necessary files for genetics unit testing

print("\nImporting all necessary files")
import os
import sys
sys.path.insert(0,os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../pyLearnstimate'))
from pyLearnstimate import genetics as gen
import random as rn

#%% Seed that random generator!

# Define a constant seed value for random
seed_val = 123
print("\nSeeding random generator with value: ",seed_val)
rn.seed(seed_val)

#%% Network testing

print("\nTesting network functionality:")
testn = gen.Network()

print("Generating test network")
testn.generateTestNetwork(10)

print("Test network once:")
print(testn.evaluateNetwork([1,2,3,4]))

print("Test network twice:")
print(testn.evaluateNetwork([4,3,2,1]))

print("Test network thrice:")
print(testn.evaluateNetwork([1,2,3,4]))


#%% Genetics testing

print("\nTesting genetics functionality")

print("\nGENOME 1")
print("Generating genome")
testg1 = gen.Genome()

print("Generating test genome")
testg1.generateTestGenome(10)

print("Generating network from the test genome")
testg1.generateNetwork()

# Test getRandomNeuron
print("Getting a random neuron:")
random_neuron = testg1.network.getRandomNeuron(True)

print('A random neuron is: ',random_neuron,' at ',random_neuron)

# Test mutations
print("\nGENOME 2")
print("Test none output on genome:")
testg2 = gen.Genome()
testg2.generateNetwork()
for i in range(10):
    testg2.network.evaluateNetwork([None]*4)
print(testg2.network.evaluateNetwork([None]*4))

print("\nGENOME 3")
print("Generate a third genome")
testg3 = gen.Genome()
print("Display the genome")
#testg3.displayGenome()

print("Mutate the genome 10 times")
for i in range(100):
    testg3.mutate()
    
print("Generate the network")
testg3.generateNetwork()

print("The number of neurons are: ",len(testg3.network.neurons))

print("Evaluate the network 10 times")
for i in range(10):
    testg3.network.evaluateNetwork([4,3,2,1])
print(testg3.network.evaluateNetwork([4,3,2,1]))

print("Display the genome")
testg3.displayGenome()
#%% Species testing
    
#%% Pool testing