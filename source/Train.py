from geneticAlgo import Population 

class Train:
    def __init__(self, population_size, mutate_probability,retain_prob,select):
        self.population = Population(population_size,mutate_probability,retain_prob,select)
        self.best = None
        self.lastState = None

    def execute(self, num_of_generation): # input the state of current 

        for generation in range(num_of_generation):
            
            with open("./results/res.txt", "a") as file:
                file.write("Generation No : "+str(generation)+"\n\n")
            self.population.runSimulation()
            self.population.evolve()
            self.best = self.population.population_fitness
            with open("./results/res.txt", "a") as file:
                file.write("Generation best : " + str(self.best) + "\n\n\n")
            self.bestModel = self.population.bestModel


population_size = 50
generation = 100
mutate_probability = 0.08
retain_prob = 0.01
select = 0.33
train = Train(population_size, mutate_probability,retain_prob,select)
train.execute(generation)

