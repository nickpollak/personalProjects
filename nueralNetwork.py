import numpy as np

def thruPut(x):
    return 1 / (1+np.exp(-x))

class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def feedForward(self, inputs):
        total = np.dot(self.weights, inputs) + self.bias
        return thruPut(total)
    
weights = np.array([2,1])
bias = 4
n = Neuron(weights, bias)
x = np.array([15, 26])
print(n.feedForward(x))