from numpy import mat, ones, zeros, random, append, argmax
from sigmoid import sigmoid


def predict(features_input, weights_layer_1, weight_outputs):
    A1 = mat(append(mat([[1]]), features_input, axis=1))

    a2 = sigmoid(A1 * weights_layer_1.T)

    A2 = mat(append(ones((a2.shape[0], 1)), a2, axis=1))

    A3 = sigmoid(A2 * weight_outputs.T)

    return argmax(A3)
