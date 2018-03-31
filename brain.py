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
        self.last_inputs = [0, 0]

    def clone(self):
        clone = Brain(self.network.clone())
        return clone

    def decide_what_to_do_now(self, food_position, ant_position, world_size):
        rel_pos_x = (food_position[0] - ant_position[0]) / world_size[0]
        rel_pos_y = (food_position[1] - ant_position[1]) / world_size[1]

        self.last_inputs = [rel_pos_x, rel_pos_y]

        return self.network.predict(mat([self.last_inputs]))

    def modify_just_a_little(self):
        for i in range(0, MUTATION_AMOUNT):
            mutation_variant_per = randint(0, 100)
            mutation_inverse_per = randint(0, 100)

            if mutation_inverse_per <= MUTATION_INVERSE_CHANCE:
                self.network.invert_one_random_weight()

            if mutation_variant_per <= MUTATION_VARIANT_CHANCE:
                self.network.alter_one_random_weight()
