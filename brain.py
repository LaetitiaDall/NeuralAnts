from numpy import mat, ones, zeros, random, append, argmax, round, multiply
from predict import predict
from random import randint
from constants import *
from network import RandomNetwork


class Brain:

    def __init__(self, network=None):
        if network is None:
            network = RandomNetwork()
        self.network = network
        self.lastInputs = [0, 0]

    def clone(self):
        clone = Brain(self.network.clone())
        return clone

    def decideWhatToDoNow(self, foodPosition, antPosition, worldSize):
        relPosX = (foodPosition[0] - antPosition[0]) / worldSize[0]
        relPosY = (foodPosition[1] - antPosition[1]) / worldSize[1]

        self.lastInputs = [relPosX, relPosY]

        return self.network.predict(mat([self.lastInputs]))

    def modifyJustALittle(self):
        for i in range(0, MUTATION_AMOUNT):
            mutationVariantPer = randint(0, 100)
            mutationInversePer = randint(0, 100)

            if mutationInversePer <= MUTATION_INVERSE_CHANCE:
                self.network.invertOneRandomWeight()

            if mutationVariantPer <= MUTATION_VARIANT_CHANCE:
                self.network.alterOneRandomWeight()
