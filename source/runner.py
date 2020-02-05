from simulation import simulation
from neuralNetwork import NeuralNetwork
import numpy as np
import pickle as pkl

with open('./results/best_model.pkl', 'rb') as f:
    weights = pkl.load(f)
    dimensions = (9, 5, 5, 1)
    nn = NeuralNetwork(dimensions, weights, 0)
    simulation(nn, 1)
