import pandas as pd
import numpy as np
import math


class Data:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path, index_col=0, header=0)
        self.main = self.df.loc[self.df.index.str.contains("A[0-9]", regex=True)]
        check_all_numeric(self.main, "Criteria table contains missing or string value.")
        self.m, self.n = self.main.shape
        check_enough_number(self.m, 2, "Please use two or more alternatives.")
        check_enough_number(self.n, 2, "Please use two or more criteria.")

        self.alternatives = list(self.main.index)
        self.criteria = list(self.df.columns)

        self.types = list(self.df.loc["Types"])

        check_enough_number(len(self.types), self.n, "Missing Types values.")
        check_types_list(self.types, "Please use 0 and 1 for Types.")

        self.weights = list(self.df.loc["Weights"])

        check_all_float(
            self.weights, "Please use double values between 0 and 1 for Weights."
        )
        check_weights_total(self.weights)

        self.matrix = self.main.to_numpy()

    def print_data(self):
        print("Data Set:")
        print(
            pd.DataFrame(
                data=self.matrix, columns=self.criteria, index=self.alternatives
            )
        )
        print("Types:")
        print(self.types)
        print("Weights:")
        print(self.weights)


class Ref1Data:
    def __init__(self, file_path):
        if file_path is None:
            self.df = None
            self.main = None
            self.m, self.n = None, None
            self.criteria = None
            self.alternatives = None
            self.queues = None
            self.types = None
            self.weights = None
            self.successors = None
            self.unacc = None
            self.bounds = None
        else:
            self.df = pd.read_excel(file_path, index_col=0, header=0)
            self.main = self.df.loc[self.df.index.str.contains("A[0-9]", regex=True)]
            self.m, self.n = self.main.shape
            self.criteria = list(self.df.columns)
            self.alternatives = list(self.main.index)
            self.queues = self.df.loc[self.df.index.str.contains("Queue")]
            self.types = self.df.loc[self.df.index.str.contains("Type")]
            self.types_list = list(self.types.iloc[0, :])
            self.weights = self.df.loc[self.df.index.str.contains("Weight")]
            self.weights_list = list(self.weights.iloc[0, :])
            self.successors = self.df.loc[self.df.index.str.startswith("Successor")]
            self.unacc = self.df.loc[
                self.df.index.str.startswith("ꞵ")
            ]  # Unacceptance Degrees
            self.bounds = self.df.loc[self.df.index.str.startswith("Reference")]

            # DATA CONTROLS FOR USER FAULTS
            # Check types. Types must be one of them: B, N, O, C
            check_ref1_types(self.types_list, "Allowed types: B, N, O, C")
            check_ref1_main_data(self.types_list, self.main)
            check_successors_unacc(self.successors, self.unacc)
            check_queue_values(self.types_list, self.queues)
            check_all_float(
                self.weights_list,
                "Please use double values between 0 and 1 for Weights.",
            )
            check_weights_total(self.weights_list)
            check_missing_in_df(self.bounds, "Reference can not be missing.")
            check_ref1_reference(self.types_list, self.bounds)


class Ref2Data:
    def __init__(self, file_path):
        if file_path is None:
            self.df = None
            self.main = None
            self.m, self.n = None, None
            self.criteria = None
            self.alternatives = None
            self.queues = None
            self.p_values = None
            self.weights = None
            self.successors = None
            self.unacc = None
            self.bounds = None
            self.matrix = None
        else:
            self.df = pd.read_excel(file_path, index_col=0, header=0)
            self.main = self.df.loc[self.df.index.str.contains("A[0-9]", regex=True)]
            self.m, self.n = self.main.shape
            self.criteria = list(self.df.columns)
            self.alternatives = list(self.main.index)
            self.queues = self.df.loc[self.df.index.str.contains("Queue")]
            self.p_values = {}
            self.weights = self.df.loc[self.df.index.str.contains("Weight")]
            self.weights_list = list(self.weights.iloc[0, :])
            self.successors = self.df.loc[self.df.index.str.startswith("Successor")]
            self.unacc = self.df.loc[
                self.df.index.str.startswith("ꞵ")
            ]  # Unaccaptance Degrees
            self.bounds = self.df.loc[self.df.index.str.startswith("Reference")]
            self.matrix = self.main.to_numpy()

            check_ref2_main_data(self.main)
            check_successors_unacc(self.successors, self.unacc)
            check_all_float(
                self.weights_list,
                "Please use double values between 0 and 1 for Weights.",
            )
            check_weights_total(self.weights_list)
            check_missing_in_df(self.bounds, "Reference can not be missing.")
            check_all_numeric(
                self.bounds, "Reference values must contain numerical values."
            )
            try:
                # Ro values calculation
                for cr in self.criteria:
                    col_max = np.max(np.abs(self.main[cr]))
                    abs_max_value = math.ceil(
                        np.max(
                            [
                                np.abs(self.bounds.iloc[0].at[cr]),
                                np.abs(self.bounds.iloc[1].at[cr]),
                                col_max,
                            ]
                        )
                    )

                    upper = np.abs(self.bounds.iloc[0].at[cr])
                    lower = np.abs(self.bounds.iloc[1].at[cr])

                    if (np.abs(upper) >= col_max) or (np.abs(lower) >= col_max):
                        self.p_values[cr] = 0
                    else:
                        self.p_values[cr] = len(str(int(abs_max_value)))
            except:
                raise DataSetException("Ro values error.")


#################################
# Methods for Empty Data Sheets #
#################################
def create_mcdm_df(num_cr, num_alt):
    column_names = ["C{}".format(i) for i in range(1, num_cr + 1)]
    index_names = ["Types", "Weights"] + [
        "A{}".format(i) for i in range(1, num_alt + 1)
    ]
    return pd.DataFrame(columns=column_names, index=index_names)


def create_ref1_df(num_binary, num_nominal, num_ordinal, num_cardinal, num_alt):
    column_names = ["Binary {}".format(i) for i in range(1, num_binary + 1)]
    column_names += ["Nominal {}".format(i) for i in range(1, num_nominal + 1)]
    column_names += ["Ordinal {}".format(i) for i in range(1, num_ordinal + 1)]
    column_names += ["Cardinal {}".format(i) for i in range(1, num_cardinal + 1)]

    index_names = ["Successor {}".format(i) for i in range(1, 6)]
    index_names += ["ꞵ {}".format(i) for i in range(1, 6)]
    index_names += [
        "Queue",
        "Criteria Weights",
        "Criteria Type",
        "Reference-Upper Bound",
        "Reference-Lower Bound",
    ]
    index_names += ["A{}".format(i) for i in range(1, num_alt + 1)]

    df = pd.DataFrame(columns=column_names, index=index_names)
    df.loc["Criteria Type", (col for col in df.columns if "Binary" in col)] = "B"
    df.loc["Criteria Type", (col for col in df.columns if "Nominal" in col)] = "N"
    df.loc["Criteria Type", (col for col in df.columns if "Ordinal" in col)] = "O"
    df.loc["Criteria Type", (col for col in df.columns if "Cardinal" in col)] = "C"

    return df


def create_ref2_df(num_cr, num_alt):
    column_names = ["C{}".format(i) for i in range(1, num_cr + 1)]

    index_names = ["Successor {}".format(i) for i in range(1, 6)]
    index_names += ["ꞵ {}".format(i) for i in range(1, 6)]
    index_names += [
        "Criteria Weights",
        "Reference-Upper Bound",
        "Reference-Lower Bound",
    ]
    index_names += ["A{}".format(i) for i in range(1, num_alt + 1)]

    df = pd.DataFrame(columns=column_names, index=index_names)

    return df


def select_ro_value(value_list) -> int:
    abs_values = [np.abs(x) for x in value_list]
    max_value = np.max(abs_values)
    if max_value < 1:
        return 0
    else:
        return len(str(int(max_value)))


####################################
# User Data Control and Exceptions #
####################################


class DataSetException(Exception):
    """Customized exception class to send messages to user interface."""


def check_all_numeric(df: pd.DataFrame, error_message: str):
    if (
        all(df.apply(lambda s: pd.to_numeric(s, errors="coerce").notnull().all()))
    ) != True:
        raise DataSetException(error_message)


def check_enough_number(count: int, min_value: int, error_message: str):
    if count < min_value:
        raise DataSetException(error_message)


def check_types_list(types_list: list, error_message: str):
    if not set(types_list).issubset({0, 1}):
        raise DataSetException(error_message)


def check_all_float(values: list, error_message: str):
    non_float_list = [x for x in values if float(x) != x]

    if len(non_float_list) > 0:
        raise DataSetException(error_message)


def check_weights_total(weights_list):
    if not (math.isclose(sum(weights_list), 1, abs_tol=0.01)):
        raise DataSetException("Sum of the weights must be equal to 1.")


def check_ref1_types(types_list: list, error_message: str):
    if not set(types_list).issubset({"B", "N", "O", "C"}):
        raise DataSetException(error_message)


def check_ref1_main_data(types_list: list, main_data: pd.DataFrame):
    if main_data.isna().values.any():
        raise DataSetException("Missing value in main data.")

    # Check by types.
    index_list = []
    i = 0
    for item in types_list:
        if item in ["O", "C"]:
            index_list.append(i)
        i += 1

    check_all_numeric(
        main_data.iloc[:, index_list],
        "Ordinal and Cardinal type columns can only contain numerical values.",
    )


def check_ref2_main_data(main_data: pd.DataFrame):
    check_all_numeric(main_data, "Criteria table contains missing or string value.")


def check_successors_unacc(successors, unacc):
    # Check if is all numeric
    new_data = pd.concat([successors, unacc])
    new_data = new_data.fillna(0)
    check_all_numeric(new_data, "Successors and Unacceptance values must be numerical.")

    # Check corrisponding values
    succ_isna = successors.isna().values
    unacc_isna = unacc.isna().values

    if not (succ_isna == unacc_isna).all():
        raise DataSetException(
            "Successors must have corresponding Unacceptance values."
        )


def check_queue_values(types_list, queues):
    # Check by types
    index_list = []
    i = 0
    for item in types_list:
        if item == "O":
            index_list.append(i)
        i += 1

    check_all_numeric(
        queues.iloc[:, index_list], "Ordinal type columns must have Queue values."
    )


def check_missing_in_df(main_data: pd.DataFrame, error_message: str):
    if main_data.isna().values.any():
        raise DataSetException(error_message)


def check_ref1_reference(types_list, bounds):
    index_list = []
    i = 0
    for item in types_list:
        if item in ["O", "C"]:
            index_list.append(i)
        i += 1

    check_all_numeric(
        bounds.iloc[:, index_list],
        "Ordinal and Cardinal type columns can only contain numerical Reference values.",
    )
