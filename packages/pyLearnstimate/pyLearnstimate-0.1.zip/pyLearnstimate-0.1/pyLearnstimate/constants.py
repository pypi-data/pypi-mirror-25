# -*- coding: utf-8 -*-
"""
.. module:: constants.py
   :platform: Unix, Windows
   :synopsis: Global constant variables for the pyLearnstimate module.

.. moduleauthor:: Sasha Petrenko <sap625@mst.edu>
"""

BOX_RADIUS = 6
INPUT_SIZE = (BOX_RADIUS*2+1)*(BOX_RADIUS*2+1)

#NUM_INPUTS = InputSize+1
NUM_INPUTS = 4
NUM_OUTPUTS = 4
NUM_TEST = 10
ButtonNames = ['a','b','c','d']

VERBOSE = False

# Derived constants
START_INPUT = 0
START_OUTPUT = NUM_INPUTS
START_HIDDEN = NUM_INPUTS + NUM_OUTPUTS

END_INPUT = NUM_INPUTS
END_OUTPUT = NUM_INPUTS + NUM_OUTPUTS
#END_HIDDEN = NUM_INPUTS + NUM_OUTPUTS + NUM_HIDDEN

# Pool constants
POPULATION = 300
DELTA_DISJOINT = 2.0
DELTA_WEIGHTS = 0.4
DELTA_THRESHOLD = 1.0

StaleSpecies = 15

MUTATE_CONNECTIONS_CHANCE = 0.25
PERTURB_CHANCE = 0.90
CrossoverChance = 0.75
LINK_MUTATION_CHANCE = 2.0
NODE_MUTATION_CHANCE = 0.50
BIAS_MUTATION_CHANCE = 0.40
STEP_SIZE = 0.1
DISABLE_MUTATION_CHANCE = 0.4
ENABLE_MUTATION_CHANCE = 0.2

TIMEOUT = 20

MaxNodes = 1000000
