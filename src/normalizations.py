import numpy as np


def normalize(matrix):
    shape = np.shape(matrix)
    new_matrix = np.empty(shape)
    for i in range(shape[1]):
        new_matrix[:, i] = matrix[:, i] / np.sum(matrix[:, i])
    return new_matrix
