from geneticAlgo import Population 

class LightBrain:
    def __init__(self):
        self.population = Population(pop_size=50)
        self.best = None
        self.lastState = None

    def execute(self, num_of_generation): # input the state of current 

        file = open("res.txt", "w")
        for generation in range(num_of_generation):
            
            file.write("Generation No : "+str(generation)+"\n\n")
            self.population.runSimulation(file)
            self.population.evolve()
            self.best = self.population.population_fitness
            file.write("Generation best : " + str(self.best) + "\n\n\n")
            self.bestModel = self.population.bestModel
            ## save the best light model 
        file.close()



runner = LightBrain()
runner.execute(100)

