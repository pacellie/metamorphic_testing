import random


def randint(min_value, max_value):
    # silence bandit security warning, we are not doing anything security related here
    return lambda: random.randint(min_value, max_value) # nosec
