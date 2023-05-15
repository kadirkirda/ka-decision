import numpy as np
import normalizations


def equal_weigths(n):
    return np.full((n), 1 / n)


def entropy(matrix):
    m, n = matrix.shape
    norm_matrix = normalizations.normalize(matrix)
    log_matrix = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            k = norm_matrix[i, j]
            if k == 0:
                log_matrix[i, j] = 0
            else:
                log_matrix[i, j] = np.log(k)

    entropies = np.zeros((n))

    for i in range(n):
        entropies[i] = -(np.sum(norm_matrix[:, i] * log_matrix[:, i]) / np.log(m))

    degree_of_divers = 1 - entropies

    w = degree_of_divers / np.sum(degree_of_divers)

    return w


def critic(matrix, types):
    m, n = matrix.shape

    norm_matrix = np.zeros((m, n))
    for i in range(n):
        min = np.min(matrix[:, i])
        max = np.max(matrix[:, i])
        diff = max - min
        if types[i] == 1:
            norm_matrix[:, i] = (matrix[:, i] - min) / diff
        else:
            norm_matrix[:, i] = (max - matrix[:, i]) / diff

    std_dev = np.std(norm_matrix, axis=0)

    corr_matrix = np.corrcoef(norm_matrix, rowvar=False)

    c_values = []

    for i in range(corr_matrix.shape[0]):
        c_values.append(std_dev[i] * np.sum(1 - corr_matrix[i, :]))

    w = c_values / np.sum(c_values)

    return w
