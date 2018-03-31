from random import randint
from numpy import mat, ones, zeros, random, append, argmax, round, multiply
from sigmoid import sigmoid
from constants import *
import pygame


class Network:

    def __init__(self, layers, input_count, output_count, activation_count):
        self.layers = layers
        self.input_count = input_count
        self.output_count = output_count
        self.activation_count = activation_count
        self.surface = pygame.Surface((len(self.layers) * self.activation_count, self.activation_count),
                                      pygame.SRCALPHA)
        self.prepare_surface()

    def clone(self):
        cloned_layers = []
        for weights in self.layers:
            cloned_layers.append(weights.copy())
        return Network(cloned_layers, self.input_count, self.output_count, self.activation_count)

    def hash_code(self):
        hash = 0
        hash += len(self.layers) * 1000000
        for layer in self.layers:
            hash += (layer.shape[0] * 100000)
            hash += (layer.shape[1] * 10000)

            for j in range(layer.shape[1]):
                for i in range(layer.shape[0]):
                    hash += layer[i][j]

        return str(hash)

    def prepare_surface(self):
        cw = 5
        ch = 5
        self.surface = pygame.Surface((len(self.layers) * self.activation_count * cw, self.activation_count * ch),
                                      pygame.SRCALPHA)
        for l in range(len(self.layers)):
            layer = self.layers[l]
            for i in range(layer.shape[0]):
                for j in range(layer.shape[1]):
                    color = (round((layer[i][j] + 0.5) * 255), round((layer[i][j] + 0.5) * 255),
                             round((layer[i][j] + 0.5) * 255))

                    surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
                    surf.fill(color)
                    self.surface.blit(surf, ((i + (l * self.activation_count)) * cw, j * ch))

    def draw(self, screen):
        screen.blit(self.surface, (screen.get_rect().width - self.surface.get_rect().width,
                                   0))

    def alter_one_random_weight(self):
        layer = self.layers[randint(0, len(self.layers) - 1)]
        i = randint(0, layer.shape[0] - 1)
        j = randint(0, layer.shape[1] - 1)
        layer[i][j] = random.rand(1) - 0.5

    def invert_one_random_weight(self):
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
    def get_random_parent_layer(father, mother, num):
        if randint(0, 1):
            return mother.layers[num]
        else:
            return father.layers[num]

    @staticmethod
    def get_random_parent_layer_weight(father, mother, num, i, j):
        if randint(0, 1):
            return mother.layers[num][i][j]
        else:
            return father.layers[num][i][j]

    @staticmethod
    def children(mother_network, father_network):
        father = father_network.clone()
        mother = mother_network.clone()
        layers = []
        max_possible_layers = len(mother.layers)

        for layerNumber in range(0, max_possible_layers):
            # find random layer in mom or dad
            layer = Network.get_random_parent_layer(father, mother, layerNumber)

            weights = zeros(layer.shape)
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    weights[i][j] = Network.get_random_parent_layer_weight(father, mother, layerNumber, i, j)

            layers.append(weights)

        return Network(layers, mother.input_count, mother.output_count, mother.activation_count)


class RandomNetwork(Network):

    def __init__(self, max_layers=MAX_LAYER_COUNT, max_activations=ACTIVATION_COUNT_PER_LAYER,
                 input_count=FEATURES_COUNT,
                 output_count=COMMAND_COUNT):
        layers = []

        layer_count = max_layers
        last_layer_activation_count = max_activations

        # first layer (input -> first activation_count)
        layers.append(self.random_layer_matrix(input_count, last_layer_activation_count))

        for i in range(2, layer_count):
            new_layer_activation_count = max_activations
            layers.append(self.random_layer_matrix(last_layer_activation_count, new_layer_activation_count))
            last_layer_activation_count = new_layer_activation_count

        # last layer
        layers.append(self.random_layer_matrix(last_layer_activation_count, output_count))

        Network.__init__(self, layers, input_count, output_count, max_activations)

    def random_layer_matrix(self, prev_layer_count, next_layer_count):
        return (random.rand(next_layer_count, prev_layer_count + 1) - 0.5)
