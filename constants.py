# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BROWN = (136, 115, 87, 100)
DARKER_BROWN = (112, 95, 71, 100)
FOOD = (240, 234, 104)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 35
CASE_WIDTH = 20
SCREEN_WIDTH = WIDTH * CASE_WIDTH
SCREEN_HEIGHT = HEIGHT * CASE_WIDTH


# network generation
MAX_LAYER_COUNT = 5
ACTIVATION_COUNT_PER_LAYER = 15
FEATURES_COUNT=2
COMMAND_COUNT=5

# mutations
MUTATION_AMOUNT = 100
MUTATION_INVERSE_CHANCE = 50
MUTATION_VARIANT_CHANCE = 50


BEST_ANTS_SELECTION_SIZE = 10
MUTATE_ON_ALL_COUNT = 20


KEEP_BEST_ANTS_COUNT = 20
CHILD_GENERATION_COUNT = 0
KEEP_RANDOM_COUNT = 0
CREATE_RANDOM_COUNT = 0
MUTATE_COUNT = 0

POPULATION_SIZE = KEEP_BEST_ANTS_COUNT + CHILD_GENERATION_COUNT + KEEP_RANDOM_COUNT + MUTATE_COUNT + CREATE_RANDOM_COUNT

MAX_GENERATIONS = 1000
TIME_UNIT_PER_GENERATION = 100
RETRIES = 1
