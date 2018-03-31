from ant import Ant
import numpy
import threading
from random import randint, choice
from constants import *
from network import RandomNetwork


class Generation(threading.Thread):
    def __init__(self, world, size=POPULATION_SIZE):
        threading.Thread.__init__(self)
        self.size = size
        self.world = world
        self.ants = []
        self.generation = 0
        self.fitnesses = []

        for i in range(size):
            ant = Ant(world)
            self.ants.append(ant)

        self.best_ant = None
        self.amount_diff_ants = self.calc_differents_ants()

    def get_count(self):
        return self.generation

    def have_ants_do_their_life(self, iterations=200):
        for ant in self.ants:
            for i in range(RETRIES):
                self.world.spawn_food()
                ant.random_position()
                for i in range(iterations):
                    ant.update()

    def calc_differents_ants(self):
        dict = {}
        for ant in self.ants:
            dict[ant.brain.network.hash_code()] = True
        return len(dict.keys())

    def select_best_ants_build_new_generation(self):
        self.generation += 1
        print("Generation: " + str(self.generation), len(self.ants), "ants")

        old_ants = self.ants[:]

        self.ants.sort(key=lambda x: x.fitness, reverse=True)
        best_ants = self.ants[0:BEST_ANTS_SELECTION_SIZE]

        self.ants = best_ants[:KEEP_BEST_ANTS_COUNT]
        self.best_ant = best_ants[0].clone()

        print("Best fitness: " + str(self.best_ant.fitness))

        # Reproduce
        for i in range(CHILD_GENERATION_COUNT - 10):
            mother = best_ants[randint(0, len(best_ants) - 1)]
            father = best_ants[randint(0, len(best_ants) - 1)]
            self.ants.append(Ant.reproduce(mother, father))

        for i in range(10):
            mother = best_ants[i]
            father = Ant(mother.world, RandomNetwork())
            self.ants.append(Ant.reproduce(mother, father))

        # Keep random
        for i in range(KEEP_RANDOM_COUNT):
            ant = old_ants[randint(0, len(old_ants) - 1)].clone()
            self.ants.append(ant)

        # Create randoms
        for i in range(CREATE_RANDOM_COUNT):
            ant = Ant(self.world)
            self.ants.append(ant)

        for i in range(MUTATE_COUNT):
            ant = best_ants[randint(0, len(best_ants) - 1)].clone()
            ant.brain.modify_just_a_little()
            self.ants.append(ant)

        for i in range(MUTATE_ON_ALL_COUNT):
            ant = choice(self.ants)
            ant.brain.modify_just_a_little()

        for ant in self.ants:
            ant.reset()

        self.amount_diff_ants = self.calc_differents_ants()

    def do_generations(self, maxGenerations=MAX_GENERATIONS, maxTimeUnit=TIME_UNIT_PER_GENERATION):
        self.fitnesses = []
        for gene in range(0, maxGenerations):
            self.have_ants_do_their_life(maxTimeUnit)
            self.select_best_ants_build_new_generation()
            self.fitnesses.append(self.best_ant.fitness)
            self.best_ant.reset()
            self.world.spawn_food()

    def run(self):
        self.do_generations()

    def get_last_generation_best_ant(self):
        if self.best_ant:
            return self.best_ant.clone()

    def calc_fitness_mean(self):
        if not self.fitnesses: return 0
        return numpy.mean(self.fitnesses[-20:])

    def get_last_best_fitness(self):
        if not self.fitnesses: return 0
        return self.fitnesses[-1]
