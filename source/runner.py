
from simulation import simulation
from neuralNetwork import NeuralNetwork
import numpy as np
import pickle as pkl

with open('./results/best_model.pkl', 'rb') as f:
    
    models = []
    count = 0
    while True:
        try:
            weights = pkl.load(f)
            with open("./results/xyz.txt", "a") as file:
                file.write(str(count) + "\n" + str(weights) + "\n\n\n")
            count += 1
            # models.append(weights)
        except EOFError:
            break
    dimensions = (9, 5, 5, 1)
    # nn = NeuralNetwork(dimensions, models[-1], 0)
    # print("avg waiting time : ", simulation(nn, 1))
