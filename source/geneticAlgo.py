from numpy import array, random, reshape
from neuralNetwork import NeuralNetwork
from simulation import simulation
import pickle as pkl

class IndividualLight:

    def __init__(self, weights, mutate_prob, dimensions):
        if weights is None:
            self.nn = NeuralNetwork(dimensions)
        else:
            self.nn = NeuralNetwork(dimensions, weights=weights, mutate_prob=mutate_prob)
        self.fitness = None
        self.timeAlloted = None

    def getTime(self, X):
        self.timeAlloted = self.nn.feed_forward(X)
        return self.timeAlloted

    def findFitness(self):
        return self.fitness

class Population:

    def __init__(self, pop_size=10, mutate_prob=0.08, retain_prob=0.01, select=0.333, dimensions = (12, 15, 5, 1), training_no = 4, traffic = 1):
        self.pop_size = pop_size                # population size of generation
        self.mutate_prob = mutate_prob          # probability of mutation of genes
        self.retain_prob = retain_prob          # probability of selecting unfittest parents
        self.select_prob = select                    # ratio of fittest parents select

        self.fitness_history = []               # stores fitness history of generation as list
        self.generation = 1                     # current generation
        self.training_no = training_no
        self.dimensions = dimensions #(12, 15, 5, 1)  # 5 inputs
        self.individuals = [IndividualLight(None, mutate_prob, dimensions) for i in range(self.pop_size)]   # initializes individuals of population
        self.population_fitness = -1e18
        self.average_fittness = 0
        self.traffic = traffic
        self.bestModel = None

    def runSimulation(self):
        simulation_no = 0
        self.average_fittness = 0
        for individual in self.individuals:
            individual.fitness = 0
            for ch in ['A', 'B', 'C']:
                f, p, T = simulation(individual.nn, 0, self.traffic)
                self.average_fittness += f
                if individual.fitness is None:
                    individual.fitness = f
                individual.fitness += f
                with open("./results/training"+str(self.training_no)+"/res.txt", "a") as file:
                    file.write(str(simulation_no) +ch+ ") " + str(p) + "\n" + str(T) + "\n\n")
                    file.write("fitness value : " + str(f)+"\n\n")
            individual.fitness /= 3
            simulation_no += 1
        self.average_fittness /= 3*self.pop_size
        with open("./results/training"+str(self.training_no)+"/graph.txt", "a") as file:
            file.write(str(self.average_fittness) + " ")

    # population fitness
    def grade(self):
        self.population_fitness = -1e18
        for i in self.individuals:
            self.population_fitness = max([i.findFitness(), self.population_fitness])
            if self.population_fitness == i.findFitness():
                self.bestModel = i.nn.weights
        with open("./results/training"+str(self.training_no)+"/best_model.pkl", 'ab') as f:
            pkl.dump(self.bestModel, f)
        with open("./results/training"+str(self.training_no)+"/graph.txt", "a") as file:
            file.write(str(self.population_fitness) + "\n")
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
                    child = IndividualLight(weights=child_weights, mutate_prob=self.mutate_prob, dimensions = self.dimensions)
                    children.append(child)
            self.individuals = self.parents + children

    def non_breed(self):
        target_children_size = self.pop_size - len(self.parents)
        children = []
        if len(self.parents) > 0:
            while len(children) < target_children_size:
                parent = random.choice(self.parents)
                parent_weight = parent.nn.weights
                child = IndividualLight(weights=parent_weight, mutate_prob=self.mutate_prob ,dimensions = self.dimensions)
                children.append(child)
            self.individuals = self.parents + children
            
    def evolve(self, type=0):

        self.grade()
        self.select_parents()
        if type:
            self.non_breed()
        else:
            self.breed()
        self.parents = []
        self.generation += 1