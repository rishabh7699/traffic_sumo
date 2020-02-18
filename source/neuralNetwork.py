from numpy import dot, random, concatenate
class NeuralNetwork:

    def __init__(self, dimensions, weights=None, mutate_prob=0.08):
        
        self.total_layers = len(dimensions)     
        if weights is None or random.rand()<0.05:
            self.weights = []
            for i in range(self.total_layers - 1):
                w = 2*random.rand(dimensions[i]+1, dimensions[i+1]) - 1
                self.weights.append(w)
        else:
            self.weights = []
            for weight in weights:
                self.weights.append(weight.copy())
            for layer in self.weights:
                for column in layer:
                    for i in range(len(column)):
                        if mutate_prob > random.rand():
                            column[i] += 0.25*(2*random.rand() - 1)
    
    def activation(self, X):
        for i in range(len(X)):
            if X[i] < 0:
                X[i] = 0
        return X
    
    def feed_forward(self, X):
        l = X
        layers = len(self.weights)
        for layer in range(layers):
            l = concatenate(([1], l))
            l = dot(l, self.weights[layer])
            if layer != layers-1:
                l = self.activation(l)
        result = l
        return result
