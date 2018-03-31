from numpy import mat, ones, zeros, random, append, argmax
from sigmoid import sigmoid


def predict(featuresInput, weightsLayer1, weightOutputs):
    A1 = mat(append(mat([[1]]), featuresInput, axis=1))

    a2 = sigmoid(A1 * weightsLayer1.T)

    A2 = mat(append(ones((a2.shape[0], 1)), a2, axis=1))

    A3 = sigmoid(A2 * weightOutputs.T)

    return argmax(A3)
