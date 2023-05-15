import pandas as pd
import numpy as np
import tools


def borda(df, weights):
    m, n = df.shape

    matrix = np.array(df)
    borda_matrix = np.empty((m, n))
    for i in range(n):
        borda_matrix[:, i] = m - matrix[:, i]
    w_borda_matrix = borda_matrix * weights

    borda_points = np.sum(w_borda_matrix, axis=1)
    ranks = tools.ranks(borda_points)

    concat = pd.DataFrame({"BORDA": borda_points, "Ranking": ranks}, index=df.index)
    return pd.concat((df, concat), axis=1)
