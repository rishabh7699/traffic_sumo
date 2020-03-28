
from simulation import simulation
from neuralNetwork import NeuralNetwork
import numpy as np
import pickle as pkl

with open('./results/training7/best_model.pkl', 'rb') as f:
    
    models = []
    count = 0
    while True:
        try:
            weights = pkl.load(f)
            count += 1
            models.append(weights)
        except EOFError:
            break
    dimensions = (8, 10, 5, 1)
    for model in models:
        avg = 0
        for i in range(20):
            nn = NeuralNetwork(dimensions, model, 0)
            avg += simulation(nn, 0)[0]
        avg /= 20
        with open("./results/training7/xyz.txt", "a") as file:
            file.write(str(avg) + "\n")

avg = 0
for i in range(20):
    avg += simulation(0, 0)[0]
avg /= 20
print(avg)

