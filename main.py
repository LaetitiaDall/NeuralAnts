from numpy import mat, ones, zeros, random, append, argmax
from sigmoid import sigmoid
from predict import predict
import os, sys
from world import World
from generation import Generation
import pygame
from constants import *

# Create the world
world = World(WIDTH, HEIGHT)

# Display world
world_for_display = World(WIDTH, HEIGHT)

# Generate ants
generation = Generation(world)

# Initialize pygame
pygame.init()

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
FONT = pygame.font.SysFont("monospace", 20)

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIDTH * CASE_WIDTH, HEIGHT * CASE_WIDTH]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Ant life")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# start generations
done = False
generation.start()
ant = None

# load images
antImage = pygame.image.load(os.path.join("img/ant_small.png"))
antImage.convert()

grassImage = pygame.image.load(os.path.join("img/grass.png"))
grassImage.convert()

chipImage = pygame.image.load(os.path.join("img/chip_small.png"))
chipImage.convert()

brownSurf = pygame.Surface((CASE_WIDTH, CASE_WIDTH), pygame.SRCALPHA)
brownSurf.fill(BROWN)

darkerBrownSurf = pygame.Surface((CASE_WIDTH, CASE_WIDTH), pygame.SRCALPHA)
darkerBrownSurf.fill(DARKER_BROWN)

last_hash_code = 0

while True:

    # display the best ant for the last generation util it doesn't move or its fitness is really bad
    if not ant or ant.is_done():

        ant = generation.get_last_generation_best_ant()

        if not ant: continue
        ant.debug = True
        cur_hash_code = ant.brain.network.hash_code()
        hash_diff = cur_hash_code != last_hash_code
        last_hash_code = ant.brain.network.hash_code()

        ant.world = world_for_display
        ant.reset()
        world_for_display.spawn_food()

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.quit()
            sys.exit(0)

    # Fill the screen with grass
    for x in range(0, SCREEN_WIDTH, 100):
        for y in range(0, SCREEN_HEIGHT, 100):
            screen.blit(grassImage, (x, y))

    # Draw the grid
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if (x + y) % 2:
                screen.blit(brownSurf, (x * CASE_WIDTH, y * CASE_WIDTH))
            else:
                screen.blit(darkerBrownSurf, (x * CASE_WIDTH, y * CASE_WIDTH))

    # Draw the food
    screen.blit(chipImage, (world_for_display.food[0] * CASE_WIDTH, world_for_display.food[1] * CASE_WIDTH))

    # Draw the ant
    img = antImage
    if ant.hor_direction == "left":
        img = pygame.transform.flip(antImage, True, False)
    if ant.ver_direction == "up":
        img = pygame.transform.rotate(img, 90)
    if ant.ver_direction == "down":
        img = pygame.transform.rotate(img, -90)

    screen.blit(img, (ant.x * CASE_WIDTH, ant.y * CASE_WIDTH))

    # render text
    label = FONT.render("Fitness: " + str(ant.fitness), 1, (255, 255, 255))
    screen.blit(label, (0, 0))

    # render text
    label = FONT.render("Last command: " + str(ant.last_command), 1, (255, 255, 255))
    screen.blit(label, (0, 30))

    # render text
    label = FONT.render("Time unit: " + str(ant.time_unit), 1, (255, 255, 255))
    screen.blit(label, (0, 60))

    # render text
    label = FONT.render("Generation: " + str(generation.get_count()), 1, (255, 255, 255))
    screen.blit(label, (0, 90))

    # render text
    label = FONT.render("Distance to food: " + str("%.5f" % ant.distance_to_food), 1, (255, 255, 255))
    screen.blit(label, (0, 120))

    # render text
    label = FONT.render("Mean fitness (20 last): " + str("%.5f" % generation.calc_fitness_mean()), 1, (255, 255, 255))
    screen.blit(label, (0, 150))

    # render text
    label = FONT.render("Last fitness: " + str("%.5f" % generation.get_last_best_fitness()), 1, (255, 255, 255))
    screen.blit(label, (0, 180))

    # render text
    label = FONT.render("Network changed:" + str(hash_diff), 1, (255, 255, 255))
    screen.blit(label, (0, 210))

    # render text
    label = FONT.render("Last inputs: " + str("%.5f" % ant.brain.last_inputs[0]) + (" - %.5f" % ant.brain.last_inputs[1]),
                        1, (255, 255, 255))
    screen.blit(label, (0, 240))

    # render text
    label = FONT.render("Amount of different ants: " + str(generation.amount_diff_ants), 1, (255, 255, 255))
    screen.blit(label, (0, 270))

    ant.brain.network.draw(screen)

    # Limit to 1 frames per second
    clock.tick(10)

    # update the best ant from last generation
    ant.update()

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
