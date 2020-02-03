from numpy import array, random, reshape
from neuralNetwork import NeuralNetwork
from simulation import simulation

class IndividualLight:
    dimensions = (9, 5, 5, 1)  # 5 inputs

    def __init__(self, weights=None, mutate_prob=0.08):
        if weights is None:
            self.nn = NeuralNetwork(IndividualLight.dimensions)
        else:
            self.nn = NeuralNetwork(IndividualLight.dimensions, weights=weights, mutate_prob=mutate_prob)
        
        self.timeAlloted = None

    def getTime(self, X):
        self.timeAlloted = self.nn.feed_forward(X)
        return self.timeAlloted

    def RunSimulation(self, simulation_no, file):  # run at the end of simulation compare with queues
        ## run simulation here 
        ## in loop for each road  
            # ## get input state
            # time_green = self.timeAlloted(input_state) ## does the feed forward work
            # ## perform rest of sim and get total waiting time
        p = [0.08,0.2,0.2,0.6]
        file.write(str(simulation_no)+") ")
        self.fitness = -1*simulation(p, self.nn, file)
        file.write(str(self.fitness)+"\n\n")
        file.flush()

    def findFitness(self):
        return self.fitness

class Population:

    def __init__(self, pop_size=10, mutate_prob=0.08, retain_prob=0.01, select=0.333):
        self.pop_size = pop_size                # population size of generation
        self.mutate_prob = mutate_prob          # probability of mutation of genes
        self.retain_prob = retain_prob          # probability of selecting unfittest parents
        self.select_prob = select                    # ratio of fittest parents select

        self.fitness_history = []               # stores fitness history of generation as list
        self.generation = 1                     # current generation

        self.individuals = [IndividualLight() for i in range(self.pop_size)]   # initializes individuals of population
        self.population_fitness = -1e18
        self.bestModel = None

    def runSimulation(self, file):
        simulation_no = 0
        for individual in self.individuals:
                individual.RunSimulation(simulation_no, file)
                simulation_no += 1

    # population fitness
    def grade(self):
        for i in self.individuals:
            self.population_fitness = max([i.findFitness(), self.population_fitness])
            if self.population_fitness == i.findFitness():
                self.bestModel = i.nn.weights

        
        self.fitness_history.append(self.population_fitness)
    
    def select_parents(self):
        retain_length = int(self.select_prob * self.pop_size)
        # sorts individual based on their filighttness
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness, reverse=True) 
        self.parents = self.individuals[:retain_length]
        # selecting random unfittest parents
        unfittest = self.individuals[retain_length:]
        for individual in unfittest:
            if self.retain_prob > random.rand():
                self.parents.append(individual)

    def crossover(self, weights1, weights2):
        weights = []

        for w1, w2 in zip(weights1, weights2):
            w = []
            for column1, column2 in zip(w1, w2):
                column = []
                for theta1, theta2 in zip(column1, column2):
                    # selecting randomly from father or mother genes
                    choosen = random.choice((theta1, theta2))       
                    column.append(choosen)
                w.append(column)
            weights.append(array(w))
        return weights
    
    def breed(self):

        # filling rest of population
        target_children_size = self.pop_size - len(self.parents)
        children = []
        if len(self.parents) > 0:
            while len(children) < target_children_size:
                father = random.choice(self.parents)
                mother = random.choice(self.parents)
                if father != mother:
                    child_weights = self.crossover(father.nn.weights, mother.nn.weights)
                    # mutation
                    child = IndividualLight(weights=child_weights)
                    children.append(child)
            self.individuals = self.parents + children

    def evolve(self):

        self.grade()
        self.select_parents()
        self.breed()
        self.parents = []
        self.generation += 1