from simulation import simulation
from neuralNetwork import NeuralNetwork
import numpy as np
import pickle as pkl

with open('./results/best_model.pkl', 'rb') as f:
    
    models = []
    while True:
        try:
            weights = pkl.loads(f)
            models.append(weights)
        except EOFError:
            break
    dimensions = (9, 5, 5, 1)
    nn = NeuralNetwork(dimensions, models[-1], 0)
    simulation(nn, 1)
