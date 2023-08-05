# -*- coding: utf-8 -*-
"""
.. module:: network.py
   :platform: Unix, Windows
   :synopsis: Network classes and functions and definitions.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>

"""
import os
import sys
import numpy as np
#import scipy as sp
import constants as cs
import random as rn

""" FUNCTION DEFINITIONS """

def sigmoid(x):
    """This function defines the sigmoid for all neurons"""
    return 2/(1+np.exp(-4.9*x))-1

def localrand():
    """Returns a random value with the locally selected random function
    """
    return rn.uniform(-1,1)

""" CLASS DEFINITIONS """

class Neuron:
    """Base class for neurons"""

    neuron_count = 0

    def __init__(self):
        self.incoming = []
        self.into = []
        self.in_dict = {}               # neuron key: incoming weight
        self.out_dict = {}              # neuron key: ?
        self.output_value = 0
        self.output_hold = 0
        self.bias = localrand()
        Neuron.neuron_count += 1

class SensorNeuron(Neuron):
    """Class for a neuron that connects to inputs
    """
    def __init__(self):
        super().__init__()
       

class MotorNeuron(Neuron):
    """Class for a neuron that produces output to outside the allele
    """
    def __init__(self):
        super().__init__()

class Allele:
    """Base class for network"""

    def __init__(self):
        """Base class for allele generation.

        """
        
        # Initialize the input and output neurons
        self.neurons = []
        self.input_neurons = []
        self.output_neurons = []
    
    def generateNetwork(self):
        """This function generates the object's initial network
        
        :raises: AttributeError, KeyError
        """
        # Append input neurons
        for i in range(cs.NUM_INPUTS):
            self.input_neurons.append(SensorNeuron())
        # Append output neurons
        for i in range(cs.NUM_OUTPUTS):
            self.output_neurons.append(MotorNeuron())
        # Append a test layer
        for i in range(cs.NUM_TEST):
            self.neurons.append(Neuron())
            
        # Make a connection between the inputs, test layer, and outputs
        for i in range(cs.NUM_INPUTS):
            for j in range(cs.NUM_TEST):
                self.neurons[j].in_dict[self.input_neurons[i]] = localrand()
        for i in range(cs.NUM_OUTPUTS):
            for j in range(cs.NUM_TEST):
                self.output_neurons[i].in_dict[self.neurons[j]] = localrand()
                

    def __computeNeuron(self,neuron):
        """Computes one neuron's local output to output_hold
        
        :neuron: Local neuron object
        :type name: list
        :returns:  list
        :raises: AttributeError, KeyError
        """
        local_sum = 0
        for in_neuron, in_weight in neuron.in_dict.items():
            if in_neuron.output_value:
                local_sum += in_neuron.output_value*in_weight
        if local_sum:
            neuron.output_hold = sigmoid(local_sum + neuron.bias)
        
        
    def evaluateNetwork(self, inputs):
        """Evaluates the network at each simulation time step
        
        :param list inputs: List of inputs to the network
        :returns: List of outputs from the network
        :rtype: list
        :raises: AttributeError, KeyError
        """
        
        """ COMPUTE NEURAL OUTPUTS """
        # Attach inputs to sensor neurons            
        for i in range(cs.NUM_INPUTS):
            self.input_neurons[i].output_value = inputs[i]
            
        # Compute outputs for each neuron
        for neuron in self.neurons:
            self.__computeNeuron(neuron)
        for neuron in self.output_neurons:
            self.__computeNeuron(neuron)

        """ REASSIGN INPUTS FOR NEXT STEP """
        for neuron in self.neurons:
            neuron.output_value = neuron.output_hold
        for neuron in self.output_neurons:
            neuron.output_value = neuron.output_hold
            
        """ GET END-OF-NETWORK OUTPUTS """
        return [self.output_neurons[i].output_value for i in range(cs.NUM_OUTPUTS)]


    def mutateAddConnection(self):
        """Add a connection between existing nodes
        """
        
        pass
    
    def mutateAddNode(self):
        """Add a new node and connections
        """
        
        rn.choice(self.neurons.keys())
        pass
    
    def mutateInsertNode(self):
        """Insert a node between an existing connection
        """
        pass
            
    def mutateDeleteConnection(self):
        """Delete an existing connection between nodes
        """
        pass
    
    def mutateDeleteNode(self):
        """Delete an existing node and its accompanying connections
        """
        rn.choice(self.neurons.keys())
        
        pass
    
    def mutateNodeWeight(self):
        """Change the existing initial weight for a connection
        """
        pass
    
class Genotype(Allele):
    
    def __init__(self):
        super().__init__(self)
        
class Tableau():
    pass



#print(test.evaluateNetwork([-1]*4))