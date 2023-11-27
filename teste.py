# Usar no cruzamento

import numpy as np


def ordered_crossover(parent1, parent2):
    size = len(parent1)
    cut1, cut2 = sorted(np.random.choice(range(size), size=2, replace=False))
    child1 = [-1] * size
    child2 = [-1] * size
    child1[cut1 : cut2 + 1] = parent1[cut1 : cut2 + 1]
    child2[cut1 : cut2 + 1] = parent2[cut1 : cut2 + 1]
    fill_values(child1, parent2, cut2 + 1)
    fill_values(child2, parent1, cut2 + 1)
    fill_values(child1, parent2, 0, cut1)
    fill_values(child2, parent1, 0, cut1)

    return child1, child2


def fill_values(child, parent, start, end=None):
    size = len(child)
    end = size if end is None else end

    index = end
    for value in parent[end:] + parent[:end]:
        if value not in child:
            child[index % size] = value
            index += 1


parent1 = [2, 3, 9, 8, 1, 6, 4]
parent2 = [1, 6, 4, 3, 9, 2, 8]

child1, child2 = ordered_crossover(parent1, parent2)

print("Parent1:", parent1)
print("Parent2:", parent2)
print("Child1: ", child1)
print("Child2: ", child2)
