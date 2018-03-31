from random import randint
from numpy import mat, ones, zeros, random, append, argmax, round, multiply
from sigmoid import sigmoid
from constants import *
import pygame


class Network:

    def __init__(self, layers, inputCount, outputCount, activationCount):
        self.layers = layers
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.activationCount = activationCount
        self.surface = pygame.Surface((len(self.layers) * self.activationCount, self.activationCount), pygame.SRCALPHA)
        self.prepareSurface()

    def clone(self):
        clonedLayers = []
        for weights in self.layers:
            clonedLayers.append(weights.copy())
        return Network(clonedLayers, self.inputCount, self.outputCount, self.activationCount)

    def hashCode(self):
        hash = 0
        hash += len(self.layers) * 1000000
        for layer in self.layers:
            hash += (layer.shape[0] * 100000)
            hash += (layer.shape[1] * 10000)

            for j in range(layer.shape[1]):
                for i in range(layer.shape[0]):
                    hash += layer[i][j]

        return str(hash)

    def prepareSurface(self):
        cw = 5
        ch = 5
        self.surface = pygame.Surface((len(self.layers) * self.activationCount * cw, self.activationCount * ch), pygame.SRCALPHA)
        for l in range(len(self.layers)):
            layer = self.layers[l]
            for i in range(layer.shape[0]):
                for j in range(layer.shape[1]):
                    color = (round((layer[i][j] + 0.5) * 255), round((layer[i][j] + 0.5) * 255),
                             round((layer[i][j] + 0.5) * 255))

                    surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
                    surf.fill(color)
                    self.surface.blit(surf, ((i + (l * self.activationCount))* cw, j * ch))


    def draw(self, screen):
        screen.blit(self.surface, (screen.get_rect().width - self.surface.get_rect().width,
                                   0))

    def alterOneRandomWeight(self):
        layer = self.layers[randint(0, len(self.layers) - 1)]
        i = randint(0, layer.shape[0] - 1)
        j = randint(0, layer.shape[1] - 1)
        layer[i][j] = random.rand(1) - 0.5

    def invertOneRandomWeight(self):
        layer = self.layers[randint(0, len(self.layers) - 1)]
        i = randint(0, layer.shape[0] - 1)
        j = randint(0, layer.shape[1] - 1)
        val = layer[i][j]
        layer[i][j] = -val

    def predict(self, featuresInput):
        a = mat(append(mat([[1]]), featuresInput, axis=1))

        for layer in range(0, len(self.layers)):
            A = sigmoid(a * self.layers[layer].T)
            a = mat(append(ones((A.shape[0], 1)), A, axis=1))

        return argmax(A)

    @staticmethod
    def getRandomParentLayer(father, mother, num):
        if randint(0, 1):
            return mother.layers[num]
        else:
            return father.layers[num]

    @staticmethod
    def getRandomParentLayerWeight(father, mother, num, i, j):
        if randint(0, 1):
            return mother.layers[num][i][j]
        else:
            return father.layers[num][i][j]

    @staticmethod
    def children(motherNetwork, fatherNetwork):
        father = fatherNetwork.clone()
        mother = motherNetwork.clone()
        layers = []
        maxPossibleLayers = len(mother.layers)

        for layerNumber in range(0, maxPossibleLayers):
            # find random layer in mom or dad
            layer = Network.getRandomParentLayer(father, mother, layerNumber)

            weights = zeros(layer.shape)
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    weights[i][j] = Network.getRandomParentLayerWeight(father, mother, layerNumber, i, j)

            layers.append(weights)

        return Network(layers, mother.inputCount, mother.outputCount, mother.activationCount)


class RandomNetwork(Network):

    def __init__(self, maxLayers=MAX_LAYER_COUNT, maxActivations=ACTIVATION_COUNT_PER_LAYER, inputCount=FEATURES_COUNT,
                 outputCount=COMMAND_COUNT):
        layers = []

        layerCount = maxLayers
        lastLayerActivationCount = maxActivations

        # first layer (input -> first activationCount)
        layers.append(self.randomLayerMatrix(inputCount, lastLayerActivationCount))

        for i in range(2, layerCount):
            newLayerActivationCount = maxActivations
            layers.append(self.randomLayerMatrix(lastLayerActivationCount, newLayerActivationCount))
            lastLayerActivationCount = newLayerActivationCount

        # last layer
        layers.append(self.randomLayerMatrix(lastLayerActivationCount, outputCount))

        Network.__init__(self, layers, inputCount, outputCount, maxActivations)

    def randomLayerMatrix(self, prevlayerCount, nextLayerCount):
        return (random.rand(nextLayerCount, prevlayerCount + 1) - 0.5)
