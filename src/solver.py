import numpy as np
import pandas as pd
import math
import tools, dataset
from ref import Ref1, Ref2


class Solver:
    calculated_ranks_by_methods = {}

    all_tables = {}  # tables for report
    """All tables to be reported."""
    table_counts = {}

    def __init__(self, data_path, **kwargs):
        self.data = dataset.Data(data_path)
        self.m, self.n = self.data.matrix.shape
        self.lambda_value = 0.5
        try:
            self.lambda_value = kwargs["lambda_value"]
        except:
            pass

    methods = [
        "topsis",
        "moosra",
        "wsm",
        "wpm",
        "waspas",
        "psi",
        "mabac",
        "rov",
        "ref_I",
        "ref_II",
    ]

    def add_table_to_list(self, method_name, table_name, dataframe):
        if method_name in self.table_counts:
            self.table_counts[method_name] += 1
        else:
            self.table_counts[method_name] = 1

        dataframe.at["", dataframe.columns[0]] = ""
        dataframe.at["Table:", dataframe.columns[0]] = table_name
        self.all_tables[
            method_name + "(" + str(self.table_counts[method_name]) + ")"
        ] = dataframe

    def get_table_names(self, method):  # gets keys by method
        return list(
            filter(lambda x: x.startswith(method), list(self.all_tables.keys()))
        )

    def solve(self, method_list):
        self.calculated_ranks_by_methods = {}
        self.all_tables = {}
        self.table_counts = {}

        main_data = pd.DataFrame(
            columns=self.data.criteria,
            index=["Types", "Weights"] + self.data.alternatives,
        )
        main_data.loc["Types", :] = self.data.types
        main_data.loc["Weights", :] = self.data.weights
        main_data.loc[
            main_data.index.str.contains("A[0-9]", regex=True)
        ] = self.data.main

        self.all_tables["DATA"] = main_data

        for method in method_list:
            func = getattr(self, method)
            func()

    def topsis(self):
        sq_matrix = np.square(self.data.matrix)
        # norm_matrix = normalize(sq_matrix)

        norm_matrix = self.data.matrix / np.sum(sq_matrix, axis=0) ** (1 / 2.0)

        self.add_table_to_list(
            "TOPSIS",
            "Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, index=self.data.alternatives, columns=self.data.criteria
            ),
        )

        weighted_matrix = norm_matrix * self.data.weights

        # A* and A- values
        minmax = np.zeros((2, self.n))
        for i in range(self.n):
            if self.data.types[i] == 1:
                minmax[0, i] = np.max(weighted_matrix[:, i])
                minmax[1, i] = np.min(weighted_matrix[:, i])
            else:
                minmax[0, i] = np.min(weighted_matrix[:, i])
                minmax[1, i] = np.max(weighted_matrix[:, i])

        weighted = pd.DataFrame(
            weighted_matrix, index=self.data.alternatives, columns=self.data.criteria
        )
        new_rows = pd.DataFrame(minmax, columns=self.data.criteria, index=["A*", "A-"])

        self.add_table_to_list(
            "TOPSIS",
            "Weighted Normalized Decision Matrix and Artificial Alternatives",
            pd.concat([weighted, new_rows], ignore_index=False),
        )

        ideals = np.zeros((self.m, self.n))
        anti_ideals = np.zeros((self.m, self.n))
        for i in range(self.n):
            ideals[:, i] = np.square(weighted_matrix[:, i] - minmax[0, i])
            anti_ideals[:, i] = np.square(weighted_matrix[:, i] - minmax[1, i])

        # S values
        ideals_s = np.sqrt(np.sum(ideals, axis=1))
        anti_ideals_s = np.sqrt(np.sum(anti_ideals, axis=1))

        c_values = anti_ideals_s / (ideals_s + anti_ideals_s)

        ranks = tools.ranks(c_values)
        self.calculated_ranks_by_methods["TOPSIS"] = ranks

        self.add_table_to_list(
            "TOPSIS",
            "Distances of Alternatives to Ideal and Anti-Ideal Solution, and Ranking of Alternatives",
            pd.DataFrame(
                {
                    "Sᵢ*": ideals_s,
                    "Sᵢ-": anti_ideals_s,
                    "Cᵢ*": c_values,
                    "Ranking": ranks,
                },
                index=self.data.alternatives,
            ),
        )

    def moosra(self):
        matrix = tools.tskor(self.data.matrix)

        sq_matrix = np.square(matrix)

        norm_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            norm_matrix[:, i] = matrix[:, i] / np.sum(sq_matrix[:, i]) ** (1 / 2.0)

        self.add_table_to_list(
            "MOOSRA",
            "The Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        w_norm_matrix = norm_matrix * self.data.weights

        self.add_table_to_list(
            "MOOSRA",
            "The Weighted Normalized Decision Matrix",
            pd.DataFrame(
                w_norm_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        b = np.zeros(self.m)
        c = np.zeros(self.m)

        for i in range(self.m):
            for j in range(self.n):
                if self.data.types[j] == 1:
                    b[i] += w_norm_matrix[i, j]
                else:
                    c[i] += w_norm_matrix[i, j]

        p = b / c

        ranks = tools.ranks(p)
        results = pd.DataFrame(
            {"bᵢ": b, "cᵢ": c, "pᵢ": p, "Ranking": ranks}, index=self.data.alternatives
        )

        self.add_table_to_list(
            "MOOSRA", "Performance Scores, and Ranking of Alternatives", results
        )

        self.calculated_ranks_by_methods["MOOSRA"] = ranks

    def wsm(self):
        matrix = tools.tskor(self.data.matrix)
        norm_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            if self.data.types[i] == 1:
                norm_matrix[:, i] = matrix[:, i] / np.max(matrix[:, i])
            else:
                norm_matrix[:, i] = np.min(matrix[:, i]) / matrix[:, i]
        wsm_matrix = norm_matrix * self.data.weights
        results = pd.DataFrame(
            wsm_matrix, index=self.data.alternatives, columns=self.data.criteria
        )

        wsm_q = np.sum(wsm_matrix, axis=1)
        results["Qi"] = wsm_q

        ranks = tools.ranks(wsm_q)
        results["Ranking"] = ranks

        self.calculated_ranks_by_methods["WSM"] = ranks
        # results = pd.DataFrame({"Scores":wsm_q,"Ranking":ranks}, index=self.data.alternatives)

        self.add_table_to_list("WSM", "WSM Scores", results)

    def wpm(self):
        matrix = tools.tskor(self.data.matrix)
        wpm_matrix = np.empty_like(matrix)
        for i in range(self.n):
            if self.data.types[i] == 1:
                wpm_matrix[:, i] = np.power(
                    (matrix[:, i] / np.max(matrix[:, i])),
                    self.data.weights[i],
                )
            else:
                wpm_matrix[:, i] = np.power(
                    (np.min(matrix[:, i]) / matrix[:, i]),
                    self.data.weights[i],
                )

        results = pd.DataFrame(
            wpm_matrix, index=self.data.alternatives, columns=self.data.criteria
        )

        wpm_q = np.prod(wpm_matrix, axis=1)
        results["Qi"] = wpm_q

        ranks = tools.ranks(wpm_q)
        results["Ranking"] = ranks

        self.calculated_ranks_by_methods["WPM"] = ranks

        # results = pd.DataFrame({"Scores":wpm_q,"Ranking":ranks}, index=self.data.alternatives)

        self.add_table_to_list("WPM", "WPM Scores", results)

    def waspas(self):
        matrix = tools.tskor(self.data.matrix)
        norm_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            if self.data.types[i] == 1:
                norm_matrix[:, i] = matrix[:, i] / np.max(matrix[:, i])
            else:
                norm_matrix[:, i] = np.min(matrix[:, i]) / matrix[:, i]
        wsm_matrix = norm_matrix * self.data.weights

        wsm_q = np.sum(wsm_matrix, axis=1)

        wpm_matrix = np.empty_like(matrix)
        for i in range(self.n):
            if self.data.types[i] == 1:
                wpm_matrix[:, i] = np.power(
                    (matrix[:, i] / np.max(matrix[:, i])),
                    self.data.weights[i],
                )
            else:
                wpm_matrix[:, i] = np.power(
                    (np.min(matrix[:, i]) / matrix[:, i]),
                    self.data.weights[i],
                )
        wpm_q = np.prod(wpm_matrix, axis=1)

        waspas_df = pd.DataFrame(
            {"WSM": wsm_q, "WPM": wpm_q}, index=self.data.alternatives
        )

        waspas_df["Unified Q"] = waspas_df["WSM"] * self.lambda_value + waspas_df[
            "WPM"
        ] * (1 - self.lambda_value)

        ranks = tools.ranks(np.array(waspas_df["Unified Q"]))
        waspas_df["Ranking"] = ranks

        self.calculated_ranks_by_methods["WASPAS"] = ranks

        self.add_table_to_list(
            "WASPAS", f"WASPAS Scores with Lambda: {self.lambda_value}", waspas_df
        )

        return waspas_df

    def psi(self):
        matrix = tools.tskor(self.data.matrix)
        norm_matrix = np.zeros((self.m, self.n))

        for i in range(self.n):
            if self.data.types[i] == 1:
                norm_matrix[:, i] = matrix[:, i] / np.max(matrix[:, i])
            else:
                norm_matrix[:, i] = np.min(matrix[:, i]) / matrix[:, i]

        self.add_table_to_list(
            "PSI",
            "The Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        means = np.mean(norm_matrix, axis=0)
        pref_var_matrix = np.zeros((self.m, self.n))

        for i in range(self.n):
            pref_var_matrix[:, i] = np.power((norm_matrix[:, i] - means[i]), 2)

        self.add_table_to_list(
            "PSI",
            "The Weighted Normalized Decision Matrix",
            pd.DataFrame(
                pref_var_matrix,
                columns=self.data.criteria,
                index=self.data.alternatives,
            ),
        )

        pv = np.sum(pref_var_matrix, axis=0)
        phi = np.abs(1 - pv)
        psi = phi / np.sum(phi)
        last_matrix = norm_matrix * psi
        I = np.sum(last_matrix, axis=1)
        ranks = tools.ranks(I)
        self.calculated_ranks_by_methods["PSI"] = ranks
        results = pd.DataFrame(
            {"Preferences Indices": I, "Ranking": ranks}, index=self.data.alternatives
        )
        self.add_table_to_list("PSI", "Ranking of Alternatives", results)

        return results

    def mabac(self):
        norm_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            min = np.min(self.data.matrix[:, i])
            max = np.max(self.data.matrix[:, i])
            diff = max - min
            if self.data.types[i] == 1:
                norm_matrix[:, i] = (self.data.matrix[:, i] - min) / diff
            else:
                norm_matrix[:, i] = (max - self.data.matrix[:, i]) / diff

        self.add_table_to_list(
            "MABAC",
            "Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        w_matrix = (norm_matrix + 1) * self.data.weights
        self.add_table_to_list(
            "MABAC",
            "Weighted Normalized Decision Matrix",
            pd.DataFrame(
                w_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        g_vector = np.power(np.prod(w_matrix, axis=0), (1 / self.m))
        self.add_table_to_list(
            "MABAC",
            "Border Approximation Area Matrix",
            pd.DataFrame([g_vector], columns=self.data.criteria, index=["Gᵢ"]),
        )

        dist_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            dist_matrix[:, i] = w_matrix[:, i] - g_vector[i]
        s_values = np.sum(dist_matrix, axis=1)
        ranks = tools.ranks(s_values)
        self.calculated_ranks_by_methods["MABAC"] = ranks
        dist_pd = pd.DataFrame(
            dist_matrix, index=self.data.alternatives, columns=self.data.criteria
        )
        dist_pd["Sᵢ"] = s_values
        dist_pd["Ranking"] = ranks

        self.add_table_to_list(
            "MABAC", "Performance Scores, and Ranking of Alternatives", dist_pd
        )

        alt_members = np.zeros((self.m, self.n))
        for i in range(self.n):
            alt_members[:, i] = [1 if x > 0 else 0 for x in dist_matrix[:, i]]
        # g_members = np.sum(alt_members, axis=1)
        return pd.DataFrame(
            {"Sᵢ": s_values, "Ranking": ranks}, index=self.data.alternatives
        )

    def rov(self):
        norm_matrix = np.zeros((self.m, self.n))
        for i in range(self.n):
            min = np.min(self.data.matrix[:, i])
            max = np.max(self.data.matrix[:, i])
            diff = max - min
            if self.data.types[i] == 1:
                norm_matrix[:, i] = (self.data.matrix[:, i] - min) / diff
            else:
                norm_matrix[:, i] = (max - self.data.matrix[:, i]) / diff

        self.add_table_to_list(
            "ROV",
            "Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        last_matrix = norm_matrix * self.data.weights

        self.add_table_to_list(
            "ROV",
            "Weighted Normalized Decision Matrix",
            pd.DataFrame(
                last_matrix, columns=self.data.criteria, index=self.data.alternatives
            ),
        )

        u_plus = np.sum((last_matrix * self.data.types), axis=1)
        u_minus = np.sum((last_matrix * (1 - np.array(self.data.types))), axis=1)

        u_average = (u_plus + u_minus) / 2
        ranks = tools.ranks(u_average)
        self.calculated_ranks_by_methods["ROV"] = ranks
        results = pd.DataFrame(
            {
                "The Best Utility Value": u_plus,
                "The Worst Utility Value": u_minus,
                "The Midpoint Utility Value": u_average,
                "Ranking": ranks,
            },
            index=self.data.alternatives,
        )

        self.add_table_to_list("ROV", "Ranking of Alternatives", results)

    def ref_I(self):
        """Simplified Ref-I method to solve using the same data."""
        ref1 = Ref1(None)
        ref1.data.main = self.data.main
        ref1.data.criteria = self.data.criteria
        ref1.data.alternatives = self.data.alternatives
        ref1.data.m, ref1.data.n = self.m, self.n
        ref1.data.queues = pd.DataFrame(columns=self.data.criteria)
        ref1.data.types = pd.DataFrame(
            [["C" for x in range(self.n)]], columns=self.data.criteria
        )
        ref1.data.weights = pd.DataFrame(
            [self.data.weights], columns=self.data.criteria
        )
        ref1.data.successors = pd.DataFrame(columns=self.data.criteria)
        ref1.data.unacc = pd.DataFrame(columns=self.data.criteria)
        ref1.data.bounds = pd.DataFrame(
            np.zeros((2, self.n)), columns=self.data.criteria
        )

        col_num = 0
        for column in self.data.criteria:
            if self.data.types[col_num] == 1:
                ref1.data.bounds.iat[0, col_num] = np.max(self.data.main[column])
                ref1.data.bounds.iat[1, col_num] = np.max(self.data.main[column])
            else:
                ref1.data.bounds.iat[0, col_num] = np.min(self.data.main[column])
                ref1.data.bounds.iat[1, col_num] = np.min(self.data.main[column])
            col_num += 1

        ref1.solve()
        self.calculated_ranks_by_methods["REF-I"] = ref1.calculated_rank

        self.all_tables = {**self.all_tables, **ref1.all_tables}

    def ref_II(self):
        """Simplified Ref-II method to solve using the same data."""
        ref2 = Ref2(None)
        ref2.data.main = self.data.main
        ref2.data.criteria = self.data.criteria
        ref2.data.alternatives = self.data.alternatives
        ref2.data.m, ref2.data.n = self.m, self.n
        ref2.data.queues = pd.DataFrame(columns=self.data.criteria)
        ref2.data.p_values = pd.DataFrame(
            [[0 for i in range(self.n)]], columns=self.data.criteria
        )
        ref2.data.weights = pd.DataFrame(
            [self.data.weights], columns=self.data.criteria
        )
        ref2.data.successors = pd.DataFrame(columns=self.data.criteria)
        ref2.data.unacc = pd.DataFrame(columns=self.data.criteria)
        ref2.data.bounds = pd.DataFrame(
            np.zeros((2, self.n)), columns=self.data.criteria
        )

        col_num = 0
        for column in self.data.criteria:
            if self.data.types[col_num] == 1:
                ref2.data.bounds.iat[0, col_num] = np.max(self.data.main[column])
                ref2.data.bounds.iat[1, col_num] = np.max(self.data.main[column])
            else:
                ref2.data.bounds.iat[0, col_num] = np.min(self.data.main[column])
                ref2.data.bounds.iat[1, col_num] = np.min(self.data.main[column])
            col_num += 1

        # Ro value calculation
        for cr in self.data.criteria:
            col_max = np.max(np.abs(ref2.data.main[cr]))
            abs_max_value = math.ceil(
                np.max(
                    [
                        np.abs(ref2.data.bounds.iloc[0].at[cr]),
                        np.abs(ref2.data.bounds.iloc[1].at[cr]),
                        col_max,
                    ]
                )
            )

            upper = np.abs(ref2.data.bounds.iloc[0].at[cr])
            lower = np.abs(ref2.data.bounds.iloc[1].at[cr])

            if (np.abs(upper) >= col_max) or (np.abs(lower) >= col_max):
                ref2.data.p_values[cr] = 0
            else:
                ref2.data.p_values[cr] = len(str(int(abs_max_value)))

        ref2.solve()
        self.calculated_ranks_by_methods["REF-II"] = ref2.calculated_rank
        self.all_tables = {**self.all_tables, **ref2.all_tables}
