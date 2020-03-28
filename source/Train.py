from geneticAlgo import Population 
from os import mkdir

population_size = 70
num_of_generation = 3000
mutate_prob = 0.1
retain_prob = 0.03
select_prob = 0.4
type_evolution = 1  # 1 for no crossover, 0 for crossover
dimensions = (8, 10, 5, 1)
training_no = 8
traffic = 1.0

class Train:
    
    def __init__(self):
        mkdir("./results/training"+str(training_no))
        with open("./results/training"+str(training_no)+"/logs.txt", "w") as file:
            file.write("population_size : " + str(population_size) + "\n")
            file.write("num_of_generation : " + str(num_of_generation) + "\n")
            file.write("mutate_prob : " + str(mutate_prob) + "\n")
            file.write("retain_prob : " + str(retain_prob) + "\n")
            file.write("select_prob : " +  str(select_prob) + "\n")
            file.write("type_evolution : " + str(type_evolution) + "\n")
            file.write("dimensions : " + str(dimensions) + "\n")
            file.write("training_no : " + str(training_no) + "\n")
            file.write("traffic : " + str(traffic) + "\n")
        self.population = Population(population_size,mutate_prob,retain_prob,select_prob, dimensions, training_no, traffic)
        self.best = None

    def execute(self):
        for generation in range(num_of_generation):
            with open("./results/training"+str(training_no)+"/res.txt", "a") as file:
                file.write("Generation No : "+str(generation)+"\n\n")
            self.population.runSimulation()
            self.population.evolve(type_evolution)
            self.best = self.population.population_fitness
            with open("./results/training"+str(training_no)+"/res.txt", "a") as file:
                file.write("Generation best : " + str(self.best) + "\n\n\n")
            self.bestModel = self.population.bestModel

train = Train()
train.execute()

