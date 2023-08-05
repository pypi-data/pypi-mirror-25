import math
import random


def generate_random_id():
    return str(math.floor(random.random() * 1800000)) + str(math.floor(random.random() * 4000000)) + str(
        math.floor(random.random() * 55000))
