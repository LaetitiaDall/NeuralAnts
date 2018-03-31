from brain import Brain
from random import randint
from network import Network
import sys
from constants import *


class Ant:

    def __init__(self, world, network=None):
        self.world = world
        self._x = 0
        self._y = 0

        # store how many times it hasn't moved
        self.notMoved = 0

        # store how many time it eat food
        self.foodEaten = 0

        # store current distance to food
        self.distanceToFood = sys.maxsize

        # store the amount of good decisions
        self.goodDecisions = 0

        # keep track of direction for image display
        self.horDirection = "right"
        self.verDirection = "none"

        self.commands = {
            0: self.moveUp,
            1: self.moveDown,
            2: self.moveLeft,
            3: self.moveRight,
            4: self.eatFood,
        }
        self.commandsName = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right',
            4: 'eat-food',
        }

        self.debug = False

        # the last command the ant did
        self.lastCommand = "None"

        # define a starting position
        self.randomPosition()

        # its brain
        self.brain = Brain(network)

        # time units of live
        self.timeUnit = 0

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        if abs(self._x - value) > 1:
            raise Exception()
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def fitness(self):
        """I'm the 'x' property."""
        fit = 0
        self.distanceToFood = self.world.distanceToFood(self)
        # return (self.foodEaten * 10) - self.distanceToFood
        return self.goodDecisions - self.timeUnit

    def randomPosition(self):
        if self.debug:
            print ("randompos")
        #self._x = randint(0, self.world.width - 1)
        #self._y = randint(0, self.world.height - 1)

        self._x = int(self.world.width / 2)
        self._y = int(self.world.height / 2)

    def reset(self):
        self.randomPosition()
        self.foodEaten = 0
        self.distanceToFood = sys.maxsize
        self.goodDecisions = 0
        self.timeUnit = 0
        self.notMoved = 0

    def clone(self):
        clone = Ant(self.world)
        clone.distanceToFood = self.distanceToFood
        clone.goodDecisions = self.goodDecisions
        clone.foodEaten = self.foodEaten
        clone.brain = self.brain.clone()
        return clone

    def move(self, stepX, stepY):
        self.notMoved = 0

        oldDistance = self.world.distanceToFood(self)
        self.x = self.x + stepX
        self.y = self.y + stepY
        newDistance = self.world.distanceToFood(self)

        if (newDistance < oldDistance) and not self.canEatFood():
            self.goodDecisions += 1

    def moveUp(self):
        self.verDirection = "up"
        self.move(0, -1)

    def moveDown(self):
        self.verDirection = "down"
        self.move(0, 1)

    def moveLeft(self):
        self.verDirection = "none"
        self.horDirection = "left"
        self.move(-1, 0)

    def moveRight(self):
        self.verDirection = "none"
        self.horDirection = "right"
        self.move(1, 0)

    def eatFood(self):
        self.notMoved += 1
        if self.canEatFood():
            self.foodEaten += 1
            self.world.foodHasBeenEaten()
            self.goodDecisions += 1




    def canMoveTo(self, x, y):
        """if x >= self.world.width: return False
        if x < 0: return False
        if y >= self.world.height: return False
        if y < 0: return False"""
        return True

    def canEatFood(self):
        return self.world.distanceToFood(self) <= 1

    def runCommand(self, number):
        self.commands[number]()

    def update(self):
        command = self.brain.decideWhatToDoNow(self.world.food, (self.x, self.y), [self.world.width, self.world.height])
        self.runCommand(command)
        self.lastCommand = self.commandsName[command]
        self.timeUnit += 1

    def isDone(self):
        return self.timeUnit > TIME_UNIT_PER_GENERATION

    @staticmethod
    def reproduce(mother, father):
        network = Network.children(mother.brain.network, father.brain.network)
        child = Ant(mother.world, network)
        return child
