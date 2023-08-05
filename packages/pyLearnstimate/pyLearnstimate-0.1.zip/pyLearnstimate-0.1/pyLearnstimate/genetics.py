# -*- coding: utf-8 -*-
"""
.. module:: genetics.py
   :platform: Unix, Windows
   :synopsis: Genetics for the pyLearnstimate module.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>

"""

import os
import sys
import numpy as np
#import scipy as sp
import constants as cs
import random as rn
from copy import deepcopy    
from matplotlib import pyplot as plt
import networkx as nx

def sigmoid(x):
    """This function defines the sigmoid for all neurons
    
    :param float x: Input value to the sigmoid
    :returns: Output value of the sigmoid
    :rtype: float
    """
    return 2/(1+np.exp(-4.9*x))-1


def localrand():
    """Returns a random value with the locally selected random function
    
    :returns: Random value from selected random function
    :rtype: float
    """
    return rn.uniform(-1,1)


class Neuron():
    """Neuron class for implementation with the NEAT algorithm
    """
    # Set the global max_neuron variable
    max_neuron = cs.NUM_INPUTS+cs.NUM_OUTPUTS-1  # Global maximum neuron count
    
    def __init__(self):
        self.outof = []
        self.into = []
        self.weights = []
        self.location = 0
        self.bias = 0
        self.output = None
        self.output_hold = None
        

class Network():
    """Network class for implementation with the NEAT algorithm
    """

    def __init__(self):
        self.neurons = []           # Local list of neurons
        self.num_hidden = 0         # Local hidden neuron counter
        
        # Append input and output neurons
        for i in range(cs.NUM_INPUTS): self.newNeuron()
        for i in range(cs.NUM_OUTPUTS): self.newNeuron()
        
    def getSlices(self,num_hidden):
        """Gets range slices of the input, output, and hidden neurons
        """
        # Define slice lists for input, output, and hidden for convenience
        input_slice = range(cs.START_INPUT, cs.START_INPUT + cs.NUM_INPUTS)
        output_slice = range(cs.START_OUTPUT, cs.START_OUTPUT + cs.NUM_OUTPUTS)
        hidden_slice = range(cs.START_HIDDEN, cs.START_HIDDEN + num_hidden)

        return input_slice, output_slice, hidden_slice
    
    def newNeuron(self):
        """Creates a new neuron for the local network instance
        """
        # Append a new neuron to the network
        self.neurons.append(Neuron())
        
        # Increment the local hidden neuron counter
        self.num_hidden += 1
        
    def connectNeurons(self,local_outof,local_into,weight):
        """Connects two neurons within the network
        
        :param int local_outof: Out of this neuron
        :param int local_into: Into this neuron
        :param int weight: Weight of the connection
        """
        if cs.VERBOSE: print('Connect ',local_outof,' to ',local_into)
        self.neurons[local_into].outof.append(local_outof)
        self.neurons[local_outof].into.append(local_into)
        self.neurons[local_into].weights.append(weight)
        if cs.VERBOSE:
            print('Into\'s outof: ',self.neurons[local_into].outof[-1],
                  'Outof\'s into: ',self.neurons[local_outof].into[-1])
    
    #TODO: This is bad (needs to have a network generated to get neurons)
    def getRandomNeuron(self,do_input):
        """Gets a random neuron from the list of neurons in the network
        
        :param bool do_input: To include input neurons or not
        :returns: Random neuron
        :rtype: genetics.Neuron
        :returns: Index of random neuron
        :rtype: int
        """

        if do_input:
            random_neuron = rn.choice(self.neurons[cs.START_INPUT:cs.END_INPUT] \
                                      +self.neurons[cs.START_HIDDEN:])
        else:
            random_neuron = rn.choice(self.neurons[cs.START_OUTPUT:])
        
        index = self.neurons.index(random_neuron)
        
        return random_neuron, index
    
    def generateTestNetwork(self,num_hidden=4):
        """Generates a test network for network-level tests
        
        :param int num_hidden: Number of hidden neurons in one hidden layer
        """
        # Generate the new test hidden layer
        for i in range(num_hidden):
            self.newNeuron()
            
        # Get slices of the neurons list
        input_slice, output_slice, hidden_slice = self.getSlices(num_hidden)
        
        # Attach the input neurons to the hidden layer in every way
        for i in input_slice:
            for j in hidden_slice:
                if cs.VERBOSE: print('Connecting ', i, ' to ', j)
                self.connectNeurons(i,j,localrand())
        # Attach the hidden layer to the output layer in every way
        for i in hidden_slice:
            for j in output_slice:
                if cs.VERBOSE: print('Connecting ', i, ' to ', j)
                self.connectNeurons(i,j,localrand())

                
    def evaluateNetwork(self,inputs):
        """Evaluates the output values of each neuron in the network instance
        
        :param list inputs: List of inputs to the network's input neurons
        :returns: List of output values
        :rtype: list
        """
        # Get slices of the neurons list
        input_slice, output_slice, hidden_slice = self.getSlices(self.num_hidden)
        
        # Attach the inputs to the input neurons
        for i in range(cs.NUM_INPUTS):
            self.neurons[i].output = inputs[i]

        # Conduct evaluation for each neuron after input neurons
        for neuron in self.neurons[cs.NUM_INPUTS:]:
            if neuron.outof:
                local_sum = sum([self.neurons[neuron.outof[i]].output*neuron.weights[i] \
                                 for i in range(len(neuron.outof))\
                                 if self.neurons[neuron.outof[i]].output != None ])
                neuron.output_hold = sigmoid(local_sum+neuron.bias)
                
        # Swap holding variable for next iteration's output value
        for neuron in self.neurons[cs.START_OUTPUT:]:
            neuron.output = neuron.output_hold

        # Get outputs
        local_outputs = [self.neurons[i].output for i in output_slice]
        return local_outputs
    

class Gene():
    """Class for a single gene, which fits within a larger genome
    """
    
    # Global innovation number
    global_innovation = 0
    
    def __init__(self, outof, into, weight):
        self.into = into
        self.outof = outof
        self.weight = weight
        self.bias = 0
        self.enabled = True
        self.output = None
        self.output_hold = None

        # Increment class variable, assign innovation number to the instance
        Gene.global_innovation +=1
        self.innovation = Gene.global_innovation
        

class Genome():
    """Class for a genome of many genes, also containing its associated network
    """
    
    def __init__(self):
        self.network = Network()        # Local instance of network from genome
        self.neurons = set()            # Awareness of neurons in genome
        self.genes = []                 # List of genes

        # Old components:
        self.fitness = 0
        self.adjustedFitness = 0
        self.max_innovation = 0     # Local maximum innovation
        self.globalRank = 0
        self.mutationRates = {'connections':cs.MUTATE_CONNECTIONS_CHANCE,
                            'link':cs.LINK_MUTATION_CHANCE,
                            'bias':cs.BIAS_MUTATION_CHANCE,
                            'node':cs.NODE_MUTATION_CHANCE,
                            'enable':cs.ENABLE_MUTATION_CHANCE,
                            'disable':cs.DISABLE_MUTATION_CHANCE,
                            'step':cs.STEP_SIZE}
        
        # Mutate the genome initially, and generate a network from it
        self.mutate()
         
    def newGene(self,outof,into,weight):
        """Appends a new gene to the end of the genome
        
        :param int outof: Index of the "out-of" neuron
        :param int into: Index of the "into" neuron
        :param float weight: Weight of the associated connection
        """
        self.genes.append(Gene(outof,into,weight))
#        self.max_innovation = self.genes[-1].innovation
        self.max_innovation = Gene.global_innovation
    
    def getNeuronAwareness(self):
        """Updates the local list of neuron indices tagged in the genome
        """
        self.neurons = set()                # Reset local neurons list
        for i in range(cs.START_HIDDEN):    # Include the inputs/outputs
            self.neurons.add(i)
        for gene in self.genes:             # Include everything in the genome
            self.neurons.add(gene.into)
            self.neurons.add(gene.outof)
    
    def getRandomNeuron(self,do_input):
        """Gets a random neuron from the list of neurons referenced in the genome
        """
        self.getNeuronAwareness()               # Update local neuron list
        
        if do_input:                            # If include inputs, exclude outputs
            local_slice = range(cs.START_OUTPUT,cs.END_OUTPUT)
        else:                                   # If exclude inputs, include outputs
            local_slice = range(cs.START_INPUT,cs.END_INPUT)
        
        for i in local_slice:                   # Remove the selected slice
            self.neurons.discard(i)
            
        return rn.choice(tuple(self.neurons))   # Return a choice of the set
    
    def generateTestGenome(self,num_hidden):
        """Generates an example genome for unit testing
        
        :param int num_hidden: Number of neurons in the one hidden layer
        """
        for i in range(cs.NUM_INPUTS):
            for j in range(cs.NUM_INPUTS+cs.NUM_OUTPUTS,cs.NUM_INPUTS+cs.NUM_OUTPUTS+num_hidden):
                if cs.VERBOSE: print('Connect ', i, ' to ', j)
                self.newGene(i,j,localrand())
        for i in range(cs.NUM_INPUTS+cs.NUM_OUTPUTS,cs.NUM_INPUTS+cs.NUM_OUTPUTS+num_hidden):
            for j in range(cs.NUM_INPUTS,cs.NUM_INPUTS+cs.NUM_OUTPUTS):
                if cs.VERBOSE:
                    print('Connect ', i, ' to ', j)
                self.newGene(i,j,localrand())
  
    def generateNetwork(self):
        """Generates a network based upon the specification of the genome
        """
        self.network = Network()
        for gene in self.genes:
            if gene.enabled:
                while len(self.network.neurons)-1 < gene.into:
                    if cs.VERBOSE: print(len(self.network.neurons),' is not ',gene.into)
                    self.network.newNeuron()
                self.network.neurons[gene.into].outof.append(gene.outof)
                self.network.neurons[gene.into].weights.append(gene.weight)
                while len(self.network.neurons)-1 < gene.outof:
                    if cs.VERBOSE: print(len(self.network.neurons),' is not ',gene.outof)
                    self.network.newNeuron()
                self.network.neurons[gene.outof].into.append(gene.into)
                
#TODO: Define perturbation function?
    def pointMutate(self):
        """Mutates the weights of all connections by perturbation or random assignment
        """
        step = self.mutationRates['step']
        for gene in self.genes:
            if rn.random() < cs.PERTURB_CHANCE:
                gene.weight = gene.weight+rn.random()*step*2-step
            else:
                gene.weight = rn.random()*4-2

    def containsLink(self, local_outof, local_into):
        """Checks if a link exists within the genome
        
        :param int local_into: Link into a neuron
        :param int local_outof: Link out of a neuron
        """
        if len(self.genes) == 0:
            return False
        
        for gene in self.genes:
            if gene.into == local_into and gene.outof == local_outof:
                return True
        else:
            return False

    def linkMutate(self):
        """Gets a random pair of neurons and creates a new gene to link them
        """
        #TODO: How to do this any other way without deep copying the genome?
        for i in range(3):
            local_into = self.getRandomNeuron(False)
            local_outof = self.getRandomNeuron(True)
            
            if not self.containsLink(local_outof, local_into):
                self.newGene(local_outof, local_into, rn.random()*4-2)
                return
        

    def nodeMutate(self):
        """Inserts a new node in between an existing connection
        """
        
        # Make sure that there is at least one connection
        if len(self.genes) == 0:
            return

        #TODO: How to do this without a deep copy?
        for i in range(3): # Just check three times because I can't figure out how to quickly solve this
            local_gene = rn.choice(self.genes)
            if local_gene.enabled:
                break
        else:
            return
        
        local_gene.enable = False       # Disable the gene/existing link
        Neuron.max_neuron += 1          # Increment the number of neurons
        self.newGene(local_gene.outof,Neuron.max_neuron,1.0)
        self.newGene(Neuron.max_neuron,local_gene.into,local_gene.weight)

    def enableDisableMutate(self,to_enable):
        """Enables or disables a random gene in the genome
        """
        if len(self.genes) == 0:
            return
        
        local_gene = rn.choice([gene if gene.enabled is not to_enable \
                                else None for gene in self.genes])
        if local_gene is not None:
            local_gene.enabled = not local_gene.enabled

#TODO:
    def mutate(self):
        """Mutates the local genome
        """
        if cs.VERBOSE: print("MUTATING")
        for mutation, rate in self.mutationRates.items():
            if rn.randint(1,2) == 1:
                self.mutationRates[mutation] = 0.95*rate
            else:
                self.mutationRates[mutation] = 1.05263*rate
        
        if rn.random() < self.mutationRates['connections']:
            self.pointMutate()
            
        p = self.mutationRates['link']
        while p > 0:
            if rn.random() < p:
#                self.linkMutate(False)
                if cs.VERBOSE: print("Link mutate")
                self.linkMutate()
            p = p - 1
#        p = self.mutationRates['bias']
#        while p > 0:
#            if rn.random() < p:
#                self.linkMutate(True)
#            p = p - 1
        p = self.mutationRates['node']
        while p > 0:
            if rn.random() < p:
                if cs.VERBOSE: print("Node mutate")
                self.nodeMutate()
            p = p - 1
            
        p = self.mutationRates['enable']
        while p > 0:
            if rn.random() < p:
                if cs.VERBOSE: print("Enable mutate")
                self.enableDisableMutate(True)
            p = p - 1
            
        p = self.mutationRates['disable']
        while p > 0:
            if rn.random() < p:
                if cs.VERBOSE: print("Disable mutate")
                self.enableDisableMutate(False)
            p = p - 1
            
    def displayGenome(self):
        """Displays the network generated by the local genome
        """

        self.generateNetwork()      # Get the most up-to-date network
        DG = nx.DiGraph()           # Create the directed graph instance
        for gene in self.genes:     # Append all connections to the graph
            DG.add_edge(gene.outof,gene.into)
        
        # Initialize graphing data containers
        local_pos = {}
        local_labels = {}
        local_pos_labels = {}
        to_keep = []
        
        # Define slice lists for input, output, and hidden for convenience
        input_slice = range(cs.START_INPUT, cs.START_INPUT + cs.NUM_INPUTS)
        output_slice = range(cs.START_OUTPUT, cs.START_OUTPUT + cs.NUM_OUTPUTS)
        
        # Define graphing parameters
        dim = 2.5       # Vertical dimension (height)
        xin = -0.5      # x-position of input layer
        xout = 1.5      # x-position of output layer
        yin = -0.5      # Lowest y-position of input layer
        yout = -0.5     # Lowest y-position of output layer
        dlabel = 0.15   # Separation of the input/output labels from their nodes
        
        # Calculate differential steps for evenly spaced input and output layers
        dy_in = dim / cs.NUM_INPUTS
        dy_out = dim / cs.NUM_OUTPUTS
        
        # Inputs: add nodes, calculate positions, generate labels, set to keep
        for i in input_slice:
            DG.add_node(i)
            local_pos[i] = [xin,yin+dy_in*i]
            local_pos_labels[i] = [xin-dlabel,yin+dy_in*i+dlabel]
            local_labels[i] = "I" + str(i)
            to_keep.append(i)
            
        # Outputs: add nodes, calculate positions, generate labels, set to keep
        for i in output_slice:
            DG.add_node(i)
            local_pos[i] = [xout,yout+dy_out*(i-cs.NUM_OUTPUTS)]
            local_pos_labels[i] = [xout+dlabel,yout+dy_out*(i-cs.NUM_OUTPUTS)+dlabel]
            local_labels[i] = "O" + str(i-cs.NUM_OUTPUTS)
            to_keep.append(i)

        # Generate a random spacing for the hidden neurons
        for i in range(cs.START_HIDDEN,Neuron.max_neuron+1):
            local_pos[i] = [rn.random(),rn.random()]
        
        # Get a spring layout of several iterations
        local_pos = nx.spring_layout(DG,pos=local_pos,fixed=to_keep,iterations=2,\
                                     scale=2)
        
        # Draw the input/output labels
        nx.draw_networkx_labels(DG,local_pos_labels,local_labels,font_size=16)
        
        # Draw the network
        nx.draw_networkx(DG,pos=local_pos)


class Species:
    """Class that contains a list of genomes and parameters of fitness
    """
    def __init__(self,genome):
        self.topFitness = 0
        self.staleness = 0
        self.genomes = []
        self.genomes.append(genome)
        self.averageFitness = 0
        
    def calculateAverageFitness(self):
        """Calculates the average fitness of all genomes within the species
        """
        local_sum = 0.0
        for genome in self.genomes:
            local_sum += genome.globalRank
        self.averageFitness = local_sum / len(self.genomes)

    
class Pool:
    """Class for a pool of species and operations for evolution 
    """
    def __init__(self):
        self.species = []
        self.generation = 0
        self.innovation = cs.NUM_OUTPUTS
        self.currentSpecies = 1
        self.currentGenome = 1
        self.currentFrame = 0
        self.maxFitness = 0
      
    def newSpecies(self,genome):
        """Adds a new species to the pool
        
        :param Genome genome): Genome of the new species
        """
        self.species.append(Species(genome))
        
#TODO:
    def addToSpecies(self,genome):
        """Adds a genome to an existing (or new) species
        
        :param Genome genome: Genome of a child species
        """
        
        found_species = False       # Flag for having found the species
        for specie in self.species: # Check all species for a match
            if not found_species and self.sameSpecies(genome,specie.genomes[0]):
                specie.genomes.append(genome)
                found_species = True
        if not found_species:       # Otherwise, create a new species
            self.newSpecies(genome)
#TODO:
    def initializeRun(self):
        self.currentFrame = 0
        timeout = cs.TIMEOUT
#        local_species = self.
        
#def initializeRun():
#	savestate.load(Filename);
#	rightmost = 0
#	pool.currentFrame = 0
#	timeout = TimeoutConstant
#	clearJoypad()
#	
#	local species = pool.species[pool.currentSpecies]
#	local genome = species.genomes[pool.currentGenome]
#	generateNetwork(genome)
#	evaluateCurrent()
#     return
        
#TODO:
    def initializePool(self):
        for i in range(1,cs.POPULATION):
            self.addToSpecies(Genome())
        self.initializeRun()
#def initializePool():
#	pool = newPool()
#
#	for i=1,Population do
#		basic = basicGenome()
#		addToSpecies(basic)
#	end
#
#	initializeRun()
#
#     return

#TODO: This is not pretty
    def disjoint(self,genome_1,genome_2):
        """Calculates the disjoint fraction of two genomes
        """
        i1 = []
        i2 = []
        disjoint_genes = 0
        nmax = max(len(genome_1),len(genome_2))
        
        for gene in genome_1:
            i1.append(gene.innovation)
        for gene in genome_2:
            i2.append(gene.innovation)
        
        for innovation in i1:
            if innovation not in i2:
                disjoint_genes += 1

        return disjoint_genes/nmax

#TODO: This is not pretty
    def weights(self,genome_1,genome_2):
        """Compare the weights of two genome's coincident genes
        """
        local_sum = 0.0
        local_coincident = 0.0
        
        i1 = {}
        for gene in genome_1:
            i1[gene.innovation] = gene

        for gene in genome_2:
            if gene.innovation in i1:
                gene1 = i1[gene.innovation]
                local_sum += abs(gene.weight-gene1.weight)
                local_coincident += 1
        
        # Avoid division by zero
        if local_coincident > 0.0:
            return local_sum/local_coincident
        else:
            return 0.0

    def sameSpecies(self,genome_1,genome_2):
        dd = cs.DELTA_DISJOINT*self.disjoint(genome_1.genes,genome_2.genes)
        dw = cs.DELTA_WEIGHTS*self.weights(genome_1.genes,genome_2.genes)
        return dd + dw < cs.DELTA_THRESHOLD

#TODO:
    def rankGlobally(self):
        pass
#def rankGlobally():
#	local global = {}
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		for g = 1,#species.genomes do
#			table.insert(global, species.genomes[g])
#		end
#	end
#	table.sort(global, function (a,b)              # Dis is bad
#		return (a.fitness < b.fitness)
#	end)
#	
#	for g=1,#global do
#		global[g].globalRank = g
#	end
#

    def totalAverageFitness(self):
        """Calculates the total average fintess of all species in the pool
        """
        local_total = 0.0
        for specie in self.species:
            local_total += specie.averageFitness
            
        return local_total
    
#TODO:
    def cullSpecies(self,cutToOne):
        pass
#def cullSpecies(cutToOne):
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		
#		table.sort(species.genomes, function (a,b)        #Dis is bad too
#			return (a.fitness > b.fitness)
#		end)
#		
#		local remaining = math.ceil(#species.genomes/2)
#		if cutToOne then
#			remaining = 1
#		end
#		while #species.genomes > remaining do
#			table.remove(species.genomes)
#		end
#	end

#TODO:
    def breedChild(self,species):
        pass
#def breedChild(species):
#	local child = {}
#	if math.random() < CrossoverChance then
#		g1 = species.genomes[math.random(1, #species.genomes)]
#		g2 = species.genomes[math.random(1, #species.genomes)]
#		child = crossover(g1, g2)
#	else
#		g = species.genomes[math.random(1, #species.genomes)]
#		child = copyGenome(g) #DO A DEEP COPY HERE
#	end
#	
#	mutate(child)
#	
#	return child
#
        
#TODO:
    def removeStaleSpecies(self):
        pass
#def removeStaleSpecies():
#	local survived = {}
#
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		
#		table.sort(species.genomes, function (a,b)            #Also dis
#			return (a.fitness > b.fitness)
#		end)
#		
#		if species.genomes[1].fitness > species.topFitness then
#			species.topFitness = species.genomes[1].fitness
#			species.staleness = 0
#		else
#			species.staleness = species.staleness + 1
#		end
#		if species.staleness < StaleSpecies or species.topFitness >= pool.maxFitness then
#			table.insert(survived, species)
#		end
#	end
#
#	pool.species = survived

#TODO:
    def removeWeakSpecies(self):
        pass
#def removeWeakSpecies():
#	local survived = {}
#
#	local sum = totalAverageFitness()
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		breed = math.floor(species.averageFitness / sum * Population)
#		if breed >= 1 then
#			table.insert(survived, species)
#		end
#	end
#
#	pool.species = survived
#
#
#

#TODO:
    def newGeneration():
        pass
#def newGeneration():
#	cullSpecies(false) # Cull the bottom half of each species
#	rankGlobally()
#	removeStaleSpecies()
#	rankGlobally()
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		calculateAverageFitness(species)
#	end
#	removeWeakSpecies()
#	local sum = totalAverageFitness()
#	local children = {}
#	for s = 1,#pool.species do
#		local species = pool.species[s]
#		breed = math.floor(species.averageFitness / sum * Population) - 1
#		for i=1,breed do
#			table.insert(children, breedChild(species))
#		end
#	end
#	cullSpecies(true) # Cull all but the top member of each species
#	while #children + #pool.species < Population do
#		local species = pool.species[math.random(1, #pool.species)]
#		table.insert(children, breedChild(species))
#	end
#	for c=1,#children do
#		local child = children[c]
#		addToSpecies(child)
#	end
#	
#	pool.generation = pool.generation + 1
#	
#	writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
#
#	


#TODO:
    def evaluateCurrent(self):
        pass
#def evaluateCurrent():
#	local species = pool.species[pool.currentSpecies]
#	local genome = species.genomes[pool.currentGenome]
#
#	inputs = getInputs()
#	controller = evaluateNetwork(genome.network, inputs)
#	
#	if controller["P1 Left"] and controller["P1 Right"] then
#		controller["P1 Left"] = false
#		controller["P1 Right"] = false
#	end
#	if controller["P1 Up"] and controller["P1 Down"] then
#		controller["P1 Up"] = false
#		controller["P1 Down"] = false
#	end
#
#	joypad.set(controller)
#
#
#    if pool == nil then
#        initializePool()
#    return

#TODO:
    def nextGenome(self):
        pass
#def nextGenome():
#	pool.currentGenome = pool.currentGenome + 1
#     if pool.currentGenome > #pool.species[pool.currentSpecies].genomes then
#		pool.currentGenome = 1
#		pool.currentSpecies = pool.currentSpecies+1
#		if pool.currentSpecies > #pool.species then
#			newGeneration()
#			pool.currentSpecies = 1
#		end
#	end
#     return

#TODO:
    def fitnessAlreadyMeasured(self):
        pass
#def fitnessAlreadyMeasured():
#	local species = pool.species[pool.currentSpecies]
#	local genome = species.genomes[pool.currentGenome]
#	
#	return genome.fitness ~= 0

#TODO:
    def crossover(self,genome_1,genome_2):
        pass
 #def crossover(g1, g2)
#	# Make sure g1 is the higher fitness genome
#	if g2.fitness > g1.fitness then
#		tempg = g1
#		g1 = g2
#		g2 = tempg
#	end
#
#	local child = newGenome()
#	
#	local innovations2 = {}
#	for i=1,#g2.genes do
#		local gene = g2.genes[i]
#		innovations2[gene.innovation] = gene
#	end
#	
#	for i=1,#g1.genes do
#		local gene1 = g1.genes[i]
#		local gene2 = innovations2[gene1.innovation]
#		if gene2 ~= nil and math.random(2) == 1 and gene2.enabled then
#			table.insert(child.genes, copyGene(gene2))
#		else
#			table.insert(child.genes, copyGene(gene1))
#		end
#	end
#	
#	child.maxneuron = math.max(g1.maxneuron,g2.maxneuron)
#	
#	for mutation,rate in pairs(g1.mutationRates) do
#		child.mutationRates[mutation] = rate
#	end
#	
#	return child
#end


#while True
#	local backgroundColor = 0xD0FFFFFF
#	if not forms.ischecked(hideBanner) then
#		gui.drawBox(0, 0, 300, 26, backgroundColor, backgroundColor)
#	end
#
#	local species = pool.species[pool.currentSpecies]
#	local genome = species.genomes[pool.currentGenome]
#	
#	if forms.ischecked(showNetwork) then
#		displayGenome(genome)
#	end
#	
#	if pool.currentFrame%5 == 0 then
#		evaluateCurrent()
#	end
#
#	joypad.set(controller)
#
#	getPositions()
#	if marioX > rightmost then
#		rightmost = marioX
#		timeout = TimeoutConstant
#	end
#	
#	timeout = timeout - 1
#	
#	
#	local timeoutBonus = pool.currentFrame / 4
#	if timeout + timeoutBonus <= 0 then
#		local fitness = rightmost - pool.currentFrame / 2
#		if gameinfo.getromname() == "Super Mario World (USA)" and rightmost > 4816 then
#			fitness = fitness + 1000
#		end
#		if gameinfo.getromname() == "Super Mario Bros." and rightmost > 3186 then
#			fitness = fitness + 1000
#		end
#		if fitness == 0 then
#			fitness = -1
#		end
#		genome.fitness = fitness
#		
#		if fitness > pool.maxFitness then
#			pool.maxFitness = fitness
#			forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
#			writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
#		end
#		
#		console.writeline("Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " fitness: " .. fitness)
#		pool.currentSpecies = 1
#		pool.currentGenome = 1
#		while fitnessAlreadyMeasured() do
#			nextGenome()
#		end
#		initializeRun()
#	end
#
#	local measured = 0
#	local total = 0
#	for _,species in pairs(pool.species) do
#		for _,genome in pairs(species.genomes) do
#			total = total + 1
#			if genome.fitness ~= 0 then
#				measured = measured + 1
#			end
#		end
#	end
#	if not forms.ischecked(hideBanner) then
#		gui.drawText(0, 0, "Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " (" .. math.floor(measured/total*100) .. "%)", 0xFF000000, 11)
#		gui.drawText(0, 12, "Fitness: " .. math.floor(rightmost - (pool.currentFrame) / 2 - (timeout + timeoutBonus)*2/3), 0xFF000000, 11)
#		gui.drawText(100, 12, "Max Fitness: " .. math.floor(pool.maxFitness), 0xFF000000, 11)
#	end
#		
#	pool.currentFrame = pool.currentFrame + 1
#
#	emu.frameadvance();
#end