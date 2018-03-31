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
        self.didnt_move = 0

        # store how many time it eat food
        self.amount_of_food_eaten = 0

        # store current distance to food
        self.distance_to_food = sys.maxsize

        # store the amount of good decisions
        self.good_decisions_taken = 0

        # keep track of direction for image display
        self.hor_direction = "right"
        self.ver_direction = "none"

        self.commands = {
            0: self.move_up,
            1: self.move_down,
            2: self.move_left,
            3: self.move_right,
            4: self.eat_food,
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
        self.last_command = "None"

        # define a starting position
        self.random_position()

        # its brain
        self.brain = Brain(network)

        # time units of live
        self.time_unit = 0

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
        self.distance_to_food = self.world.distance_to_food(self)
        # return (self.foodEaten * 10) - self.distance_to_food
        return self.good_decisions_taken - self.time_unit

    def random_position(self):
        self._x = int(self.world.width / 2)
        self._y = int(self.world.height / 2)

    def reset(self):
        self.random_position()
        self.amount_of_food_eaten = 0
        self.distance_to_food = sys.maxsize
        self.good_decisions_taken = 0
        self.time_unit = 0
        self.didnt_move = 0

    def clone(self):
        clone = Ant(self.world)
        clone.distance_to_food = self.distance_to_food
        clone.good_decisions_taken = self.good_decisions_taken
        clone.amount_of_food_eaten = self.amount_of_food_eaten
        clone.brain = self.brain.clone()
        return clone

    def move(self, stepX, stepY):
        self.didnt_move = 0

        old_distance = self.world.distance_to_food(self)
        self.x = self.x + stepX
        self.y = self.y + stepY
        new_distance = self.world.distance_to_food(self)

        if (new_distance < old_distance) and not self.can_eat_food():
            self.good_decisions_taken += 1

    def move_up(self):
        self.ver_direction = "up"
        self.move(0, -1)

    def move_down(self):
        self.ver_direction = "down"
        self.move(0, 1)

    def move_left(self):
        self.ver_direction = "none"
        self.hor_direction = "left"
        self.move(-1, 0)

    def move_right(self):
        self.ver_direction = "none"
        self.hor_direction = "right"
        self.move(1, 0)

    def eat_food(self):
        self.didnt_move += 1
        if self.can_eat_food():
            self.amount_of_food_eaten += 1
            self.world.food_has_been_eaten()
            self.good_decisions_taken += 1

    def can_move_to(self, x, y):
        return True

    def can_eat_food(self):
        return self.world.distance_to_food(self) <= 1

    def run_command(self, number):
        self.commands[number]()

    def update(self):
        command = self.brain.decide_what_to_do_now(self.world.food, (self.x, self.y), [self.world.width, self.world.height])
        self.run_command(command)
        self.last_command = self.commandsName[command]
        self.time_unit += 1

    def is_done(self):
        return self.time_unit > TIME_UNIT_PER_GENERATION

    @staticmethod
    def reproduce(mother, father):
        network = Network.children(mother.brain.network, father.brain.network)
        child = Ant(mother.world, network)
        return child
