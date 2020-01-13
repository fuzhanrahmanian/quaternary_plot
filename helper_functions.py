import numpy as np
import itertools as iter

def map_elemnts(elements, grouping, nrows, ncols):
    element_combinations = np.empty((nrows, ncols), dtype=object)
    element_combinations_list = list(iter.combinations(elements, grouping))
    counter = 0
    for i in range(nrows):
        for j in range(ncols):
            element_combinations[i][j] = element_combinations_list[counter]
            counter += 1
    return element_combinations