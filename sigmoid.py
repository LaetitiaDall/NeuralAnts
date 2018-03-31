from numpy import exp
def sigmoid(z):
    s = 1.0 / (1.0 + exp(-z))
    return s
