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

        self.bestAnt = None
        self.diffAnts = self.amountOfDifferentAnts()

    def getCount(self):
        return self.generation

    def makeAntsDoStuff(self, iterations=200):
        for ant in self.ants:
            for i in range(RETRIES):
                self.world.spawnFood()
                ant.randomPosition()
                for i in range(iterations):
                    ant.update()

    def amountOfDifferentAnts(self):
        dict = {}
        for ant in self.ants:
            dict[ant.brain.network.hashCode()] = True
        return len(dict.keys())

    def selectBestAntsAndBuildNewGeneration(self):
        self.generation += 1
        print("Generation: " + str(self.generation), len(self.ants), "ants")

        oldAnts = self.ants[:]

        self.ants.sort(key=lambda x: x.fitness, reverse=True)
        bestFitAnts = self.ants[0:BEST_ANTS_SELECTION_SIZE]

        self.ants = bestFitAnts[:KEEP_BEST_ANTS_COUNT]
        self.bestAnt = bestFitAnts[0].clone()

        print("Best fitness: " + str(self.bestAnt.fitness))

        # Reproduce
        for i in range(CHILD_GENERATION_COUNT - 10):
            mother = bestFitAnts[randint(0, len(bestFitAnts) - 1)]
            father = bestFitAnts[randint(0, len(bestFitAnts) - 1)]
            self.ants.append(Ant.reproduce(mother, father))

        for i in range(10):
            mother = bestFitAnts[i]
            father = Ant(mother.world, RandomNetwork())
            self.ants.append(Ant.reproduce(mother, father))

        # Keep random
        for i in range(KEEP_RANDOM_COUNT):
            ant = oldAnts[randint(0, len(oldAnts) - 1)].clone()
            self.ants.append(ant)

        # Create randoms
        for i in range(CREATE_RANDOM_COUNT):
            ant = Ant(self.world)
            self.ants.append(ant)

        for i in range(MUTATE_COUNT):
            ant = bestFitAnts[randint(0, len(bestFitAnts) - 1)].clone()
            ant.brain.modifyJustALittle()
            self.ants.append(ant)

        for i in range(MUTATE_ON_ALL_COUNT):
            ant = choice(self.ants)
            ant.brain.modifyJustALittle()

        for ant in self.ants:
            ant.reset()

        self.diffAnts = self.amountOfDifferentAnts()

    def doGenerations(self, maxGenerations=MAX_GENERATIONS, maxTimeUnit=TIME_UNIT_PER_GENERATION):
        self.fitnesses = []
        for gene in range(0, maxGenerations):
            self.makeAntsDoStuff(maxTimeUnit)
            self.selectBestAntsAndBuildNewGeneration()
            self.fitnesses.append(self.bestAnt.fitness)
            self.bestAnt.reset()
            self.world.spawnFood()

    def run(self):
        self.doGenerations()

    def getLastBestAnt(self):
        if self.bestAnt:
            return self.bestAnt.clone()

    def getLastFitnessMean(self):
        if not self.fitnesses: return 0
        return numpy.mean(self.fitnesses[-20:])

    def getLastFitness(self):
        if not self.fitnesses: return 0
        return self.fitnesses[-1]
