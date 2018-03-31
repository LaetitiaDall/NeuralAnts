import math
from random import randint, choice


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = [width - 1, height / 2]
        self.spawn_food()

    def distance_to_food(self, ant):
        return math.sqrt((ant.x - self.food[0]) ** 2 + (ant.y - self.food[1]) ** 2)

    def spawn_food(self):
        # self.food = [randint(0, self.width - 1), randint(0, self.height - 1)]
        # self.food = [choice([2, self.width - 2]), choice([2, self.height - 2])]
        self.food = [ self.width - 2, self.height - 2]

    def food_has_been_eaten(self):
        print("Food was eaten at : ", self.food)
        self.spawn_food()
