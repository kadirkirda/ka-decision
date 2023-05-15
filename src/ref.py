import tools, dataset
from collections import Counter
import numpy as np
import pandas as pd


class Ref1:
    calculated_rank = []
    results = None

    all_tables = {}  # additional tables for report
    """All tables to be reported."""
    table_counts = {}

    def add_table_to_dict(self, table_name, dataframe):
        method_name = "REF-I"
        if method_name in self.table_counts:
            self.table_counts[method_name] += 1
        else:
            self.table_counts[method_name] = 1

        dataframe.at["", dataframe.columns[0]] = ""
        dataframe.at["Table:", dataframe.columns[0]] = table_name
        self.all_tables[
            method_name + "(" + str(self.table_counts[method_name]) + ")"
        ] = dataframe

    def __init__(self, data_path):
        self.data = dataset.Ref1Data(data_path)

    def solve(self):
        self.all_tables = {}
        self.table_counts = {}
        m = self.data.m
        n = self.data.n

        try:
            main_data = self.data.df
            main_data.loc["Criteria Weights", :] = self.data.weights.iloc[0].to_list()
            self.all_tables["DATA"] = main_data
        except:
            pass

        matrix = np.zeros((m, n))
        i = 0
        for criterion in self.data.criteria:
            list = self.process_by_criterion(criterion)
            try:
                matrix[:, i] = list
            except:
                pass
            i += 1

        self.add_table_to_dict(
            "The Distance Matrix",
            pd.DataFrame(
                matrix, index=self.data.alternatives, columns=self.data.criteria
            ),
        )

        norm_matrix = np.zeros((m, n))

        # for j in range(n):
        #     col_sum = np.sum(matrix[:,j])

        #     new_col = (matrix[:,j]/col_sum)*self.get_weight(self.data.criteria[j])
        #     norm_matrix[:,j] = new_col

        for j in range(n):
            col_sum = np.sum(matrix[:, j])

            new_col = matrix[:, j] / col_sum
            norm_matrix[:, j] = new_col

        self.add_table_to_dict(
            "The Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, index=self.data.alternatives, columns=self.data.criteria
            ),
        )

        w_norm_matrix = norm_matrix * np.array(self.data.weights)
        self.add_table_to_dict(
            "The Weighted Normalized Decision Matrix",
            pd.DataFrame(
                w_norm_matrix, index=self.data.alternatives, columns=self.data.criteria
            ),
        )

        score = np.sum(w_norm_matrix, axis=1)
        ranks = tools.ranks(score, True)
        self.calculated_rank = ranks
        results = pd.DataFrame(
            {"Uᵢ": score, "Ranking": ranks}, index=self.data.alternatives
        )
        self.add_table_to_dict(
            "The general performance value (Uᵢ), and ranking of alternatives",
            results.copy(deep=True),
        )

        self.results = results

    def get_queue(self, criterion):
        return self.data.queues.iloc[0][criterion]

    def get_type(self, criterion):
        return self.data.types.iloc[0][criterion]

    def get_weight(self, criterion):
        return self.data.weights.iloc[0][criterion]

    def get_successors(self, criterion):
        return self.data.successors[criterion].dropna().tolist()

    def get_unacc(self, criterion):
        return self.data.unacc[criterion].dropna().tolist()

    def get_upperbound(self, criterion):
        return self.data.bounds.iloc[0][criterion]

    def get_lowerbound(self, criterion):
        return self.data.bounds.iloc[1][criterion]

    def process_by_criterion(self, criterion) -> list:
        type = self.get_type(criterion)
        if type == "C":
            new_values = []

            upper = self.get_upperbound(criterion)
            lower = self.get_lowerbound(criterion)

            values = self.data.main[criterion].tolist()
            new_value = 0
            successors = self.get_successors(criterion)
            unacc = self.get_unacc(criterion)

            for value in list(values):
                new_value = 0

                if value > upper:
                    i = 0
                    min_dif = -1
                    selected_id = -1
                    for s in successors:
                        diff = s - value
                        if diff >= 0:
                            if (min_dif == -1) or (diff < min_dif):
                                min_dif = diff
                                selected_id = i
                        i += 1
                    if selected_id == -1:
                        new_value = value - upper
                    else:
                        new_value = (value - upper) * unacc[selected_id]

                elif value < lower:
                    i = 0
                    min_dif = -1
                    selected_id = -1
                    for s in successors:
                        diff = value - s
                        if diff >= 0:
                            if (min_dif == -1) or (diff < min_dif):
                                min_dif = diff
                                selected_id = i
                        i += 1

                    if selected_id == -1:
                        new_value = lower - value
                    else:
                        new_value = (lower - value) * unacc[selected_id]
                new_values.append(new_value)

            return new_values

        elif type == "N":
            new_values = []
            values = self.data.main[criterion].tolist()
            m = self.data.m
            upper = tools.minmax_frequency(values, type="max") / m
            lower = tools.minmax_frequency(values, type="min") / m

            counter = Counter(values)

            for value in list(values):
                new_values.append((counter[value] / m) - lower)

            return new_values

        elif type == "O":
            new_values = []

            upper = self.get_upperbound(criterion)
            lower = self.get_lowerbound(criterion)
            queue = self.get_queue(criterion)
            values = self.data.main[criterion].tolist()
            new_value = 0
            successors = self.get_successors(criterion)
            unacc = self.get_unacc(criterion)

            for value in list(values):
                new_value = 0

                if value > upper:
                    i = 0
                    min_dif = -1
                    selected_id = -1
                    for s in successors:
                        diff = s - value
                        if diff >= 0:
                            if (min_dif == -1) or (diff < min_dif):
                                min_dif = diff
                                selected_id = i
                        i += 1
                    if selected_id == -1:
                        new_value = (value - upper) / (queue - 1)
                    else:
                        new_value = ((value - upper) / (queue - 1)) * unacc[selected_id]

                elif value < lower:
                    i = 0
                    min_dif = -1
                    selected_id = -1
                    for s in successors:
                        diff = value - s
                        if diff >= 0:
                            if (min_dif == -1) or (diff < min_dif):
                                min_dif = diff
                                selected_id = i
                        i += 1

                    if selected_id == -1:
                        new_value = (lower - value) / (queue - 1)
                    else:
                        new_value = ((lower - value) / (queue - 1)) * unacc[selected_id]
                new_values.append(new_value)

            return new_values

        elif type == "B":
            new_values = []

            values = self.data.main[criterion].tolist()
            lower = self.get_lowerbound(criterion)

            for value in list(values):
                if value == lower:
                    new_values.append(0)
                else:
                    new_values.append(1)

            return new_values


class Ref2:
    calculated_rank = []
    results = None

    all_tables = {}  # additional tables for report
    """All tables to be reported."""
    table_counts = {}

    def add_table_to_dict(self, table_name, dataframe):
        method_name = "REF-II"
        if method_name in self.table_counts:
            self.table_counts[method_name] += 1
        else:
            self.table_counts[method_name] = 1

        dataframe.at["", dataframe.columns[0]] = ""
        dataframe.at["Table:", dataframe.columns[0]] = table_name
        self.all_tables[
            method_name + "(" + str(self.table_counts[method_name]) + ")"
        ] = dataframe

    def __init__(self, data_path):
        self.data = dataset.Ref2Data(data_path)

    def solve(self):
        self.all_tables = {}
        self.table_counts = {}

        try:
            main_data = self.data.df
            main_data.loc["Criteria Weights", :] = self.data.weights.iloc[0].to_list()
            self.all_tables["DATA"] = main_data
        except:
            pass

        norm_matrix = np.zeros((self.data.m, self.data.n))
        i = 0
        for criterion in self.data.criteria:
            list = self.process_by_criterion(criterion)
            try:
                norm_matrix[:, i] = list
            except:
                pass
            i += 1

        self.add_table_to_dict(
            "The Normalized Decision Matrix",
            pd.DataFrame(
                norm_matrix, index=self.data.alternatives, columns=self.data.criteria
            ),
        )

        weighted_matrix = norm_matrix * self.data.weights.to_numpy()

        self.add_table_to_dict(
            "The Weighted Normalized Decision Matrix",
            pd.DataFrame(
                weighted_matrix,
                index=self.data.alternatives,
                columns=self.data.criteria,
            ),
        )

        u_values = np.sum(weighted_matrix, axis=1)
        ranks = tools.ranks(u_values, True)
        self.calculated_rank = ranks

        output_table = pd.DataFrame(
            weighted_matrix, index=self.data.alternatives, columns=self.data.criteria
        )
        output_table["Uᵢ"] = u_values
        output_table["Ranking"] = ranks

        results = pd.DataFrame(
            {"Uᵢ": u_values, "Ranking": ranks}, index=self.data.alternatives
        )

        self.add_table_to_dict(
            "The global scores (Uᵢ), and ranking of alternatives",
            results.copy(deep=True),
        )

        self.results = results

    def get_p(self, criterion):
        return self.data.p.iloc[0][criterion]

    def get_weight(self, criterion):
        return self.data.weights.iloc[0][criterion]

    def get_successors(self, criterion):
        return self.data.successors[criterion].dropna().tolist()

    def get_unacc(self, criterion):
        return self.data.unacc[criterion].dropna().tolist()

    def get_upperbound(self, criterion):
        return self.data.bounds.iloc[0][criterion]

    def get_lowerbound(self, criterion):
        return self.data.bounds.iloc[1][criterion]

    def process_by_criterion(self, criterion):
        new_values = []

        upper = self.get_upperbound(criterion)
        lower = self.get_lowerbound(criterion)

        values = self.data.main[criterion].tolist()
        new_value = 0
        successors = self.get_successors(criterion)
        unacc = self.get_unacc(criterion)

        for value in list(values):
            new_value = 0

            if value > upper:
                i = 0
                min_dif = -1
                selected_id = -1
                for s in successors:
                    diff = s - value
                    if diff >= 0:
                        if (min_dif == -1) or (diff < min_dif):
                            min_dif = diff
                            selected_id = i
                    i += 1

                if selected_id == -1:
                    new_value = (value - upper) / (
                        np.max([np.abs(upper), np.abs(lower)])
                        + pow(10, self.data.p_values[criterion])
                    )
                else:
                    new_value = ((value - upper) * unacc[selected_id]) / (
                        np.max([np.abs(upper), np.abs(lower)])
                        + pow(10, self.data.p_values[criterion])
                    )

            elif value < lower:
                i = 0
                min_dif = -1
                selected_id = -1
                for s in successors:
                    diff = value - s
                    if diff >= 0:
                        if (min_dif == -1) or (diff < min_dif):
                            min_dif = diff
                            selected_id = i
                    i += 1

                if selected_id == -1:
                    new_value = (lower - value) / (
                        np.max([np.abs(upper), np.abs(lower)])
                        + pow(10, self.data.p_values[criterion])
                    )
                else:
                    new_value = ((lower - value) * unacc[selected_id]) / (
                        np.max([np.abs(upper), np.abs(lower)])
                        + pow(10, self.data.p_values[criterion])
                    )
            new_values.append(new_value)
        return new_values
