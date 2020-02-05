from numpy import dot, random
class NeuralNetwork:

    def __init__(self, dimensions, weights=None, mutate_prob=0.08):
        
        self.total_layers = len(dimensions)     
        if weights is None:
            self.weights = []
            for i in range(self.total_layers - 1):
                w = 2*random.rand(dimensions[i], dimensions[i+1]) - 1
                self.weights.append(w)
        else:
            for layer in weights:
                for column in layer:
                    for i in range(len(column)):
                        if mutate_prob > random.rand():
                            column[i] = 2*random.rand() - 1
            self.weights = weights
    
    def activation(self, X):
        for i in range(len(X)):
            if X[i] < 0:
                X[i] = 0
        return X
    
    def feed_forward(self, X):
        l = X
        for w in self.weights:
            l = self.activation(dot(l, w))
        result = l
        return result