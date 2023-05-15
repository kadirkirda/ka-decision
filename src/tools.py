import numpy as np


def ranks(array, reversed=False):
    ranks = []
    tmp = array.argsort()
    ranks = np.empty_like(tmp)
    ranks[tmp] = np.arange(len(array)) + 1
    if reversed:
        return ranks
    else:
        return len(ranks) + 1 - ranks


# Gets minimum or maximum frequency of array by type parameter (min/max)
def minmax_frequency(array, type="min"):
    uniques = list(set(array))
    counts = list()
    for i in uniques:
        counts.append(list(array).count(i))
    if type == "max":
        return np.max(counts)
    else:
        return np.min(counts)


def tskor(matrix: np.array) -> np.array:
    tskor_cols = []
    for i in range(matrix.shape[1]):
        if np.min(matrix[:, i]) <= 0:
            tskor_cols.append(i)

    tskor_matrix = matrix.copy()

    for i in tskor_cols:
        tskor_matrix[:, i] = (
            10 * ((matrix[:, i] - np.mean(matrix[:, i])) / np.std(matrix[:, i])) + 50
        )

    return tskor_matrix
