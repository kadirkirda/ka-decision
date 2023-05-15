from PyQt6 import QtCore, QtGui, QtWidgets
import os, sys
import pandas as pd
import dataset, solver, ref, aggregations, weights
import webbrowser

default_dir = os.path.normpath(os.path.expanduser("~/Desktop"))


class Ui_TabWidget(object):
    def __init__(self):
        super().__init__()
        self.dataWindow = DataWindow()
        self.mcdm = None
        self.ref1 = None
        self.ref2 = None
        self.mcdm_default_weights = None
        self.ref1_default_weights = None
        self.ref2_default_weights = None

    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.setFixedSize(694, 569)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(13)
        description_font = QtGui.QFont()
        description_font.setFamily("Arial")
        description_font.setPixelSize(13)
        TabWidget.setFont(font)
        TabWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        TabWidget.setWindowTitle("ka-decision")
        TabWidget.setToolTip("")
        TabWidget.setAutoFillBackground(False)
        TabWidget.setStyleSheet("")
        TabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tab_mcdm = QtWidgets.QWidget()
        self.tab_mcdm.setObjectName("tab_mcdm")
        self.groupBox_method_selection = QtWidgets.QGroupBox(self.tab_mcdm)
        self.groupBox_method_selection.setGeometry(QtCore.QRect(10, 220, 211, 311))
        self.groupBox_method_selection.setTitle("MCDM Method Selection")
        self.groupBox_method_selection.setObjectName("groupBox_method_selection")

        # region layouts and buttons
        self.cb_wsm = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_wsm.setGeometry(QtCore.QRect(13, 145, 57, 20))
        self.cb_wsm.setText("WSM")
        self.cb_wsm.setObjectName("cb_wsm")
        self.cb_moosra = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_moosra.setGeometry(QtCore.QRect(13, 53, 82, 20))
        self.cb_moosra.setText("MOOSRA")
        self.cb_moosra.setObjectName("cb_moosra")
        self.cb_topsis = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_topsis.setGeometry(QtCore.QRect(13, 30, 72, 20))
        self.cb_topsis.setText("TOPSIS")
        self.cb_topsis.setObjectName("cb_topsis")
        self.cb_psi = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_psi.setGeometry(QtCore.QRect(13, 99, 45, 20))
        self.cb_psi.setText("PSI")
        self.cb_psi.setObjectName("cb_psi")
        self.cb_waspas = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_waspas.setGeometry(QtCore.QRect(13, 195, 90, 20))
        self.cb_waspas.setText("WASPAS* ")
        self.cb_waspas.setObjectName("cb_waspas")
        self.cb_rov = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_rov.setGeometry(QtCore.QRect(13, 122, 53, 20))
        self.cb_rov.setText("ROV")
        self.cb_rov.setObjectName("cb_rov")
        self.cb_wpm = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_wpm.setGeometry(QtCore.QRect(13, 168, 57, 20))
        self.cb_wpm.setText("WPM")
        self.cb_wpm.setObjectName("cb_wpm")
        self.cb_mabac = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_mabac.setGeometry(QtCore.QRect(13, 76, 72, 20))
        self.cb_mabac.setText("MABAC")
        self.cb_mabac.setObjectName("cb_mabac")
        self.txt_lambda = QtWidgets.QLineEdit(self.groupBox_method_selection)
        self.txt_lambda.setEnabled(True)
        self.txt_lambda.setGeometry(QtCore.QRect(145, 194, 41, 21))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_lambda.sizePolicy().hasHeightForWidth())
        self.txt_lambda.setSizePolicy(sizePolicy)
        self.txt_lambda.setInputMask("")
        self.txt_lambda.setText("0.5")
        self.txt_lambda.setCursorPosition(0)
        self.txt_lambda.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.txt_lambda.setPlaceholderText("")
        self.txt_lambda.setObjectName("txt_lambda")
        self.cb_ref1 = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_ref1.setGeometry(QtCore.QRect(13, 256, 58, 20))
        self.cb_ref1.setText("REF-I")
        self.cb_ref1.setObjectName("cb_ref1")
        self.cb_ref2 = QtWidgets.QCheckBox(self.groupBox_method_selection)
        self.cb_ref2.setGeometry(QtCore.QRect(13, 279, 62, 20))
        self.cb_ref2.setText("REF-II")
        self.cb_ref2.setObjectName("cb_ref2")
        self.lbl_lambda = QtWidgets.QLabel(self.groupBox_method_selection)
        self.lbl_lambda.setGeometry(QtCore.QRect(15, 225, 152, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_lambda.setText("*Lambda value is required.")
        self.lbl_lambda.setObjectName("lbl_lambda")
        self.lbl_lambda.setFont(description_font)
        self.groupBox_data = QtWidgets.QGroupBox(self.tab_mcdm)
        self.groupBox_data.setGeometry(QtCore.QRect(10, 90, 671, 131))
        self.groupBox_data.setTitle("Data Operations")
        self.groupBox_data.setObjectName("groupBox_data")
        self.lbl_criteria_count = QtWidgets.QLabel(self.groupBox_data)
        self.lbl_criteria_count.setGeometry(QtCore.QRect(15, 33, 191, 29))
        self.lbl_criteria_count.setText(
            "How many criteria will be used in the solution of the problem?"
        )
        self.lbl_criteria_count.setWordWrap(True)
        self.lbl_criteria_count.setObjectName("lbl_criteria_count")
        self.txt_num_cr = QtWidgets.QLineEdit(self.groupBox_data)
        self.txt_num_cr.setGeometry(QtCore.QRect(210, 30, 30, 30))
        self.txt_num_cr.setInputMask("")
        self.txt_num_cr.setText("")
        self.txt_num_cr.setPlaceholderText("")
        self.txt_num_cr.setObjectName("txt_num_cr")
        self.lbl_alternative_count = QtWidgets.QLabel(self.groupBox_data)
        self.lbl_alternative_count.setGeometry(QtCore.QRect(15, 70, 191, 51))
        self.lbl_alternative_count.setText(
            "How many alternatives is considered the solution of the problem?"
        )
        self.lbl_alternative_count.setWordWrap(True)
        self.lbl_alternative_count.setObjectName("lbl_alternative_count")
        self.txt_num_alt = QtWidgets.QLineEdit(self.groupBox_data)
        self.txt_num_alt.setGeometry(QtCore.QRect(210, 80, 30, 30))
        self.txt_num_alt.setInputMask("")
        self.txt_num_alt.setText("")
        self.txt_num_alt.setPlaceholderText("")
        self.txt_num_alt.setObjectName("txt_num_alt")
        self.btn_create = QtWidgets.QPushButton(self.groupBox_data)
        self.btn_create.setGeometry(QtCore.QRect(240, 30, 140, 90))
        self.btn_create.setText("Generate\nData Form")
        self.btn_create.setObjectName("btn_create")
        self.btn_showdata = QtWidgets.QPushButton(self.groupBox_data)
        self.btn_showdata.setEnabled(False)
        self.btn_showdata.setGeometry(QtCore.QRect(520, 30, 140, 90))
        self.btn_showdata.setText("Show Data")
        self.btn_showdata.setObjectName("btn_showdata")
        self.btn_importdata = QtWidgets.QPushButton(self.groupBox_data)
        self.btn_importdata.setGeometry(QtCore.QRect(380, 30, 140, 90))
        self.btn_importdata.setText("Import Data\n(Excel)")
        self.btn_importdata.setObjectName("btn_importdata")
        self.groupBox_operations = QtWidgets.QGroupBox(self.tab_mcdm)
        self.groupBox_operations.setGeometry(QtCore.QRect(240, 270, 251, 261))
        self.groupBox_operations.setTitle("Main Operations")
        self.groupBox_operations.setObjectName("groupBox_operations")
        self.btn_ranking = QtWidgets.QPushButton(self.groupBox_operations)
        self.btn_ranking.setEnabled(False)
        self.btn_ranking.setGeometry(QtCore.QRect(0, 120, 250, 100))
        self.btn_ranking.setText("Show Ranking")
        self.btn_ranking.setObjectName("btn_ranking")
        self.btn_calculate = QtWidgets.QPushButton(self.groupBox_operations)
        self.btn_calculate.setEnabled(False)
        self.btn_calculate.setGeometry(QtCore.QRect(0, 20, 250, 100))
        self.btn_calculate.setText("Calculate")
        self.btn_calculate.setObjectName("btn_calculate")
        self.btn_outputtables = QtWidgets.QPushButton(self.groupBox_operations)
        self.btn_outputtables.setEnabled(False)
        self.btn_outputtables.setGeometry(QtCore.QRect(0, 220, 250, 40))
        self.btn_outputtables.setText("Save Output Tables")
        self.btn_outputtables.setObjectName("btn_outputtables")
        self.groupBox_aggregation = QtWidgets.QGroupBox(self.tab_mcdm)
        self.groupBox_aggregation.setGeometry(QtCore.QRect(510, 220, 171, 311))
        self.groupBox_aggregation.setTitle("Aggregation")
        self.groupBox_aggregation.setObjectName("groupBox_aggregation")
        self.btn_aggregate = QtWidgets.QPushButton(self.groupBox_aggregation)
        self.btn_aggregate.setEnabled(False)
        self.btn_aggregate.setGeometry(QtCore.QRect(10, 60, 150, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_aggregate.setFont(font)
        self.btn_aggregate.setAcceptDrops(False)
        self.btn_aggregate.setText("Aggregate")
        self.btn_aggregate.setObjectName("btn_aggregate")
        self.comboBox_aggregation = QtWidgets.QComboBox(self.groupBox_aggregation)
        self.comboBox_aggregation.setGeometry(QtCore.QRect(10, 30, 151, 26))
        self.comboBox_aggregation.setObjectName("comboBox_aggregation")
        self.comboBox_aggregation.addItem("")
        self.comboBox_aggregation.setItemText(0, "Select...")
        self.comboBox_aggregation.addItem("")
        self.comboBox_aggregation.setItemText(1, "BORDA")
        self.lbl_description = QtWidgets.QLabel(self.tab_mcdm)
        self.lbl_description.setGeometry(QtCore.QRect(10, 10, 671, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_description.setFont(font)
        self.lbl_description.setAcceptDrops(False)
        self.lbl_description.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.lbl_description.setText(
            "Please fill out the required fields on the spreadsheet and upload it to the program. "
            + "In the optimization orientation cells, enter 1 for benefit criteria and 0 for the "
            + "cost criteria. Make sure that the criteria's weight values are in the range of 0-1 and that "
            + "their sum is one. Some MCDM methods have trouble calculating negative and zero-valued criteria. "
            + "In order to prevent this, T-Score transformation method is used on the basis of criteria. "
            + "Please, take this into consideration when entering data."
        )
        self.lbl_description.setFont(description_font)
        self.lbl_description.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.lbl_description.setWordWrap(True)
        self.lbl_description.setObjectName("lbl_description")
        self.groupBox_weight = QtWidgets.QGroupBox(self.tab_mcdm)
        self.groupBox_weight.setGeometry(QtCore.QRect(240, 220, 251, 51))
        self.groupBox_weight.setTitle("Weighting Method Selection")
        self.groupBox_weight.setObjectName("groupBox_weight")
        self.slc_w_method = QtWidgets.QComboBox(self.groupBox_weight)
        self.slc_w_method.setGeometry(QtCore.QRect(0, 20, 241, 26))
        self.slc_w_method.setCurrentText("Use default values")
        self.slc_w_method.setObjectName("slc_w_method")
        self.slc_w_method.addItem("")
        self.slc_w_method.setItemText(0, "Use default values")
        self.slc_w_method.addItem("")
        self.slc_w_method.setItemText(1, "Equal Weighting")
        self.slc_w_method.addItem("")
        self.slc_w_method.setItemText(2, "Entropy Weighting")
        self.slc_w_method.addItem("")
        self.slc_w_method.setItemText(3, "Critic Weighting")

        TabWidget.addTab(self.tab_mcdm, "Methods and Aggregation")
        self.tab_ref1 = QtWidgets.QWidget()
        self.tab_ref1.setEnabled(True)
        self.tab_ref1.setObjectName("tab_ref1")
        self.groupBox_data_ref1 = QtWidgets.QGroupBox(self.tab_ref1)
        self.groupBox_data_ref1.setGeometry(QtCore.QRect(10, 170, 671, 191))
        self.groupBox_data_ref1.setTitle("Data Operations")
        self.groupBox_data_ref1.setObjectName("groupBox_data_ref1")
        self.lbl_cr_count_ref1 = QtWidgets.QLabel(self.groupBox_data_ref1)
        self.lbl_cr_count_ref1.setGeometry(QtCore.QRect(10, 30, 350, 30))
        self.lbl_cr_count_ref1.setText(
            "How many binary structured criteria will be used in the solution of the problem?"
        )
        self.lbl_cr_count_ref1.setWordWrap(True)
        self.lbl_cr_count_ref1.setObjectName("lbl_cr_count_ref1")
        self.txt_num_binary = QtWidgets.QLineEdit(self.groupBox_data_ref1)
        self.txt_num_binary.setGeometry(QtCore.QRect(350, 30, 20, 25))
        self.txt_num_binary.setObjectName("txt_num_binary")
        self.lbl_nominal_ref1 = QtWidgets.QLabel(self.groupBox_data_ref1)
        self.lbl_nominal_ref1.setGeometry(QtCore.QRect(10, 60, 350, 30))
        self.lbl_nominal_ref1.setText(
            "How many nominal structured criteria will be used in the solution of the problem?"
        )
        self.lbl_nominal_ref1.setWordWrap(True)
        self.lbl_nominal_ref1.setObjectName("lbl_nominal_ref1")
        self.txt_num_nominal = QtWidgets.QLineEdit(self.groupBox_data_ref1)
        self.txt_num_nominal.setGeometry(QtCore.QRect(350, 60, 20, 25))
        self.txt_num_nominal.setObjectName("txt_num_nominal")
        self.lbl_ordinal_ref1 = QtWidgets.QLabel(self.groupBox_data_ref1)
        self.lbl_ordinal_ref1.setGeometry(QtCore.QRect(10, 90, 350, 30))
        self.lbl_ordinal_ref1.setText(
            "How many ordinal structured criteria will be used in the solution of the problem?"
        )
        self.lbl_ordinal_ref1.setWordWrap(True)
        self.lbl_ordinal_ref1.setObjectName("lbl_ordinal_ref1")
        self.txt_num_ordinal = QtWidgets.QLineEdit(self.groupBox_data_ref1)
        self.txt_num_ordinal.setGeometry(QtCore.QRect(350, 90, 20, 25))
        self.txt_num_ordinal.setObjectName("txt_num_ordinal")
        self.lbl_cardinal_ref1 = QtWidgets.QLabel(self.groupBox_data_ref1)
        self.lbl_cardinal_ref1.setGeometry(QtCore.QRect(10, 120, 350, 30))
        self.lbl_cardinal_ref1.setText(
            "How many cardinal structured criteria will be used in the solution of the problem?"
        )
        self.lbl_cardinal_ref1.setWordWrap(True)
        self.lbl_cardinal_ref1.setObjectName("lbl_cardinal_ref1")
        self.txt_num_cardinal = QtWidgets.QLineEdit(self.groupBox_data_ref1)
        self.txt_num_cardinal.setGeometry(QtCore.QRect(350, 120, 20, 25))
        self.txt_num_cardinal.setObjectName("txt_num_cardinal")
        self.lbl_alternatives_ref1 = QtWidgets.QLabel(self.groupBox_data_ref1)
        self.lbl_alternatives_ref1.setGeometry(QtCore.QRect(10, 150, 350, 30))
        self.lbl_alternatives_ref1.setText(
            "How many alternatives is considered the solution of the problem?"
        )
        self.lbl_alternatives_ref1.setWordWrap(True)
        self.lbl_alternatives_ref1.setObjectName("lbl_alternatives_ref1")
        self.txt_num_alt_ref1 = QtWidgets.QLineEdit(self.groupBox_data_ref1)
        self.txt_num_alt_ref1.setGeometry(QtCore.QRect(350, 150, 20, 25))
        self.txt_num_alt_ref1.setObjectName("txt_num_alt_ref1")
        self.btn_create_ref1 = QtWidgets.QPushButton(self.groupBox_data_ref1)
        self.btn_create_ref1.setGeometry(QtCore.QRect(380, 25, 121, 161))
        self.btn_create_ref1.setText("Generate\nData Form")
        self.btn_create_ref1.setObjectName("btn_create_ref1")
        self.btn_importdata_ref1 = QtWidgets.QPushButton(self.groupBox_data_ref1)
        self.btn_importdata_ref1.setGeometry(QtCore.QRect(510, 25, 150, 80))
        self.btn_importdata_ref1.setText("Import Data\n(Excel)")
        self.btn_importdata_ref1.setObjectName("btn_importdata_ref1")
        self.btn_showdata_ref1 = QtWidgets.QPushButton(self.groupBox_data_ref1)
        self.btn_showdata_ref1.setEnabled(False)
        self.btn_showdata_ref1.setGeometry(QtCore.QRect(510, 105, 150, 80))
        self.btn_showdata_ref1.setText("Show Data")
        self.btn_showdata_ref1.setObjectName("btn_showdata_ref1")
        self.groupBox_operations_ref1 = QtWidgets.QGroupBox(self.tab_ref1)
        self.groupBox_operations_ref1.setGeometry(QtCore.QRect(230, 370, 451, 161))
        self.groupBox_operations_ref1.setTitle("Main Operations")
        self.groupBox_operations_ref1.setObjectName("groupBox_operations_ref1")
        self.btn_calculate_ref1 = QtWidgets.QPushButton(self.groupBox_operations_ref1)
        self.btn_calculate_ref1.setEnabled(False)
        self.btn_calculate_ref1.setGeometry(QtCore.QRect(10, 30, 140, 125))
        self.btn_calculate_ref1.setText("Calculate")
        self.btn_calculate_ref1.setObjectName("btn_calculate_ref1")
        self.btn_results_ref1 = QtWidgets.QPushButton(self.groupBox_operations_ref1)
        self.btn_results_ref1.setEnabled(False)
        self.btn_results_ref1.setGeometry(QtCore.QRect(155, 30, 140, 125))
        self.btn_results_ref1.setText("Show Results")
        self.btn_results_ref1.setObjectName("btn_results_ref1")
        self.btn_outputtables_ref1 = QtWidgets.QPushButton(
            self.groupBox_operations_ref1
        )
        self.btn_outputtables_ref1.setEnabled(False)
        self.btn_outputtables_ref1.setGeometry(QtCore.QRect(300, 30, 140, 125))
        self.btn_outputtables_ref1.setText("Save\nOutput Tables")
        self.btn_outputtables_ref1.setObjectName("btn_outputtables_ref1")
        self.lbl_description_ref1 = QtWidgets.QLabel(self.tab_ref1)
        self.lbl_description_ref1.setGeometry(QtCore.QRect(10, 10, 671, 151))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_description_ref1.setFont(font)
        self.lbl_description_ref1.setAcceptDrops(False)
        self.lbl_description_ref1.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.lbl_description_ref1.setText(
            "It is fundamental to include preferences in a quantitative form in the solutions "
            + "obtained by multi-criteria decision-making methods. Preferences can, however, be "
            + "stated over categorical variables in real life. REF-I aims to find the best possible "
            + "solution for decision makers' preferences in various criteria. It is possible to "
            + "benefit from binary, nominal, ordinal, or cardinal (by measured using interval or "
            + "ratio scales) criteria in this context. In binary criteria, reference can be determined "
            + "based on compatibility, incompatibility, or frequency between two categories, while in "
            + "nominal criteria, reference can be determined based on compatibility, incompatibility, "
            + "or frequency between two or more categories. It is possible to use a specific value or "
            + "range as a reference in the ordinal and cardinal structured criteria. For each criterion "
            + "of decision makers, this software can determine up to five successors. Don't forget to "
            + "fill out the following windows with information about the problem."
        )
        self.lbl_description_ref1.setFont(description_font)
        self.lbl_description_ref1.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.lbl_description_ref1.setWordWrap(True)
        self.lbl_description_ref1.setObjectName("lbl_description_ref1")
        self.groupBox_weight_ref1 = QtWidgets.QGroupBox(self.tab_ref1)
        self.groupBox_weight_ref1.setGeometry(QtCore.QRect(10, 370, 211, 51))
        self.groupBox_weight_ref1.setTitle("Weighting Method Selection")
        self.groupBox_weight_ref1.setObjectName("groupBox_weight_ref1")
        self.slc_w_method_ref1 = QtWidgets.QComboBox(self.groupBox_weight_ref1)
        self.slc_w_method_ref1.setGeometry(QtCore.QRect(0, 20, 211, 26))
        self.slc_w_method_ref1.setCurrentText("Use default values")
        self.slc_w_method_ref1.setObjectName("slc_w_method_ref1")
        self.slc_w_method_ref1.addItem("")
        self.slc_w_method_ref1.setItemText(0, "Use default values")
        self.slc_w_method_ref1.addItem("")
        self.slc_w_method_ref1.setItemText(1, "Equal Weighting")

        self.btn_guide_ref1 = QtWidgets.QPushButton(self.tab_ref1)
        self.btn_guide_ref1.setGeometry(QtCore.QRect(10, 430, 215, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_guide_ref1.setFont(font)
        self.btn_guide_ref1.setStyleSheet("color: rgb(0, 0, 255)")
        self.btn_guide_ref1.setText("REF-I GUIDE")
        self.btn_guide_ref1.setObjectName("btn_guide_ref1")
        TabWidget.addTab(self.tab_ref1, "Detailed REF-I")
        self.tab_ref2 = QtWidgets.QWidget()
        self.tab_ref2.setObjectName("tab_ref2")
        self.groupBox_data_ref2 = QtWidgets.QGroupBox(self.tab_ref2)
        self.groupBox_data_ref2.setGeometry(QtCore.QRect(10, 130, 671, 201))
        self.groupBox_data_ref2.setTitle("Data Operations")
        self.groupBox_data_ref2.setObjectName("groupBox_data_ref2")
        self.lbl_cr_count_ref2 = QtWidgets.QLabel(self.groupBox_data_ref2)
        self.lbl_cr_count_ref2.setGeometry(QtCore.QRect(15, 58, 313, 32))
        self.lbl_cr_count_ref2.setText(
            "How many criteria will be used in the solution of the problem?"
        )
        self.lbl_cr_count_ref2.setWordWrap(True)
        self.lbl_cr_count_ref2.setObjectName("lbl_cr_count_ref2")
        self.txt_num_cr_ref2 = QtWidgets.QLineEdit(self.groupBox_data_ref2)
        self.txt_num_cr_ref2.setGeometry(QtCore.QRect(342, 60, 30, 25))
        self.txt_num_cr_ref2.setInputMask("")
        self.txt_num_cr_ref2.setText("")
        self.txt_num_cr_ref2.setObjectName("txt_num_cr_ref2")
        self.btn_create_ref2 = QtWidgets.QPushButton(self.groupBox_data_ref2)
        self.btn_create_ref2.setGeometry(QtCore.QRect(380, 30, 121, 161))
        self.btn_create_ref2.setText("Generate\nData Form")
        self.btn_create_ref2.setObjectName("btn_create_ref2")
        self.lbl_alt_count_ref2 = QtWidgets.QLabel(self.groupBox_data_ref2)
        self.lbl_alt_count_ref2.setGeometry(QtCore.QRect(15, 125, 313, 32))
        self.lbl_alt_count_ref2.setText(
            "How many alternatives is considered the solution of the problem?"
        )
        self.lbl_alt_count_ref2.setWordWrap(True)
        self.lbl_alt_count_ref2.setObjectName("lbl_alt_count_ref2")
        self.txt_num_alt_ref2 = QtWidgets.QLineEdit(self.groupBox_data_ref2)
        self.txt_num_alt_ref2.setGeometry(QtCore.QRect(342, 120, 30, 25))
        self.txt_num_alt_ref2.setInputMask("")
        self.txt_num_alt_ref2.setText("")
        self.txt_num_alt_ref2.setObjectName("txt_num_alt_ref2")
        self.btn_importdata_ref2 = QtWidgets.QPushButton(self.groupBox_data_ref2)
        self.btn_importdata_ref2.setGeometry(QtCore.QRect(510, 30, 150, 80))
        self.btn_importdata_ref2.setText("Import Data\n(Excel)")
        self.btn_importdata_ref2.setObjectName("btn_importdata_ref2")
        self.btn_showdata_ref2 = QtWidgets.QPushButton(self.groupBox_data_ref2)
        self.btn_showdata_ref2.setEnabled(False)
        self.btn_showdata_ref2.setGeometry(QtCore.QRect(510, 110, 150, 80))
        self.btn_showdata_ref2.setText("Show Data")
        self.btn_showdata_ref2.setObjectName("btn_showdata_ref2")
        self.lbl_description_ref2 = QtWidgets.QLabel(self.tab_ref2)
        self.lbl_description_ref2.setGeometry(QtCore.QRect(10, 10, 671, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_description_ref2.setFont(font)
        self.lbl_description_ref2.setAcceptDrops(False)
        self.lbl_description_ref2.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.lbl_description_ref2.setText(
            "It is sometimes required to retest the obtained solutions with new alternatives or to "
            + "eliminate some of the existing alternatives in multi-criteria decision problems. At "
            + "this point, the validity and reliability of some methods' first solutions are controversial. "
            + "Most of the discussion on this topic is on rank reversal problems. The problem of rank "
            + "reversal and the need for recalculation for existing alternatives are no longer a "
            + "problem using REF-II. REF-II allows references to be specified as intervals and to be used successors."
        )
        self.lbl_description_ref2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.lbl_description_ref2.setFont(description_font)
        self.lbl_description_ref2.setWordWrap(True)
        self.lbl_description_ref2.setObjectName("lbl_description_ref2")
        self.groupBox_weight_ref2 = QtWidgets.QGroupBox(self.tab_ref2)
        self.groupBox_weight_ref2.setGeometry(QtCore.QRect(10, 370, 211, 51))
        self.groupBox_weight_ref2.setTitle("Weighting Method Selection")
        self.groupBox_weight_ref2.setObjectName("groupBox_weight_ref2")
        self.slc_w_method_ref2 = QtWidgets.QComboBox(self.groupBox_weight_ref2)
        self.slc_w_method_ref2.setGeometry(QtCore.QRect(0, 20, 210, 26))
        self.slc_w_method_ref2.setCurrentText("Use default values")
        self.slc_w_method_ref2.setObjectName("slc_w_method_ref2")
        self.slc_w_method_ref2.addItem("")
        self.slc_w_method_ref2.setItemText(0, "Use default values")
        self.slc_w_method_ref2.addItem("")
        self.slc_w_method_ref2.setItemText(1, "Equal Weighting")
        self.slc_w_method_ref2.addItem("")
        self.slc_w_method_ref2.setItemText(2, "Entropy Weighting")
        self.slc_w_method_ref2.addItem("")
        self.slc_w_method_ref2.setItemText(3, "Critic Weighting")
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab_ref2)
        self.groupBox_9.setGeometry(QtCore.QRect(230, 370, 451, 161))
        self.groupBox_9.setTitle("Main Operations")
        self.groupBox_9.setObjectName("groupBox_9")
        self.btn_calculate_ref2 = QtWidgets.QPushButton(self.groupBox_9)
        self.btn_calculate_ref2.setEnabled(False)
        self.btn_calculate_ref2.setGeometry(QtCore.QRect(10, 30, 140, 125))
        self.btn_calculate_ref2.setText("Calculate")
        self.btn_calculate_ref2.setObjectName("btn_calculate_ref2")
        self.btn_results_ref2 = QtWidgets.QPushButton(self.groupBox_9)
        self.btn_results_ref2.setEnabled(False)
        self.btn_results_ref2.setGeometry(QtCore.QRect(155, 30, 140, 125))
        self.btn_results_ref2.setText("Show Results")
        self.btn_results_ref2.setObjectName("btn_results_ref2")
        self.btn_outputtables_ref2 = QtWidgets.QPushButton(self.groupBox_9)
        self.btn_outputtables_ref2.setEnabled(False)
        self.btn_outputtables_ref2.setGeometry(QtCore.QRect(300, 30, 140, 125))
        self.btn_outputtables_ref2.setText("Save\nOutput Tables")
        self.btn_outputtables_ref2.setObjectName("btn_outputtables_ref2")
        self.btn_guide_ref2 = QtWidgets.QPushButton(self.tab_ref2)
        self.btn_guide_ref2.setGeometry(QtCore.QRect(10, 430, 215, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.btn_guide_ref2.setFont(font)
        self.btn_guide_ref2.setStyleSheet("color: rgb(0, 0, 255)")
        self.btn_guide_ref2.setText("REF-II GUIDE")
        self.btn_guide_ref2.setObjectName("btn_guide_ref2")
        TabWidget.addTab(self.tab_ref2, "Detailed REF-II")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)
        TabWidget.setTabOrder(self.txt_num_cr, self.txt_num_alt)
        TabWidget.setTabOrder(self.txt_num_alt, self.btn_create)
        TabWidget.setTabOrder(self.btn_create, self.btn_importdata)
        TabWidget.setTabOrder(self.btn_importdata, self.btn_showdata)
        TabWidget.setTabOrder(self.btn_showdata, self.cb_topsis)
        TabWidget.setTabOrder(self.cb_topsis, self.cb_moosra)
        TabWidget.setTabOrder(self.cb_moosra, self.cb_mabac)
        TabWidget.setTabOrder(self.cb_mabac, self.cb_psi)
        TabWidget.setTabOrder(self.cb_psi, self.cb_rov)
        TabWidget.setTabOrder(self.cb_rov, self.cb_wsm)
        TabWidget.setTabOrder(self.cb_wsm, self.cb_wpm)
        TabWidget.setTabOrder(self.cb_wpm, self.cb_waspas)
        TabWidget.setTabOrder(self.cb_waspas, self.txt_lambda)
        TabWidget.setTabOrder(self.txt_lambda, self.cb_ref1)
        TabWidget.setTabOrder(self.cb_ref1, self.cb_ref2)
        TabWidget.setTabOrder(self.cb_ref2, self.slc_w_method)
        TabWidget.setTabOrder(self.slc_w_method, self.btn_calculate)
        TabWidget.setTabOrder(self.btn_calculate, self.btn_ranking)
        TabWidget.setTabOrder(self.btn_ranking, self.btn_outputtables)
        TabWidget.setTabOrder(self.btn_outputtables, self.comboBox_aggregation)
        TabWidget.setTabOrder(self.comboBox_aggregation, self.btn_aggregate)
        TabWidget.setTabOrder(self.btn_aggregate, self.btn_guide_ref1)
        TabWidget.setTabOrder(self.btn_guide_ref1, self.txt_num_binary)
        TabWidget.setTabOrder(self.txt_num_binary, self.txt_num_nominal)
        TabWidget.setTabOrder(self.txt_num_nominal, self.txt_num_ordinal)
        TabWidget.setTabOrder(self.txt_num_ordinal, self.txt_num_cardinal)
        TabWidget.setTabOrder(self.txt_num_cardinal, self.txt_num_alt_ref1)
        TabWidget.setTabOrder(self.txt_num_alt_ref1, self.btn_create_ref1)
        TabWidget.setTabOrder(self.btn_create_ref1, self.btn_importdata_ref1)
        TabWidget.setTabOrder(self.btn_importdata_ref1, self.btn_showdata_ref1)
        TabWidget.setTabOrder(self.btn_showdata_ref1, self.slc_w_method_ref1)
        TabWidget.setTabOrder(self.slc_w_method_ref1, self.btn_calculate_ref1)
        TabWidget.setTabOrder(self.btn_calculate_ref1, self.btn_results_ref1)
        TabWidget.setTabOrder(self.btn_results_ref1, self.btn_outputtables_ref1)
        TabWidget.setTabOrder(self.btn_outputtables_ref1, self.btn_guide_ref2)
        TabWidget.setTabOrder(self.btn_guide_ref2, self.txt_num_cr_ref2)
        TabWidget.setTabOrder(self.txt_num_cr_ref2, self.txt_num_alt_ref2)
        TabWidget.setTabOrder(self.txt_num_alt_ref2, self.btn_create_ref2)
        TabWidget.setTabOrder(self.btn_create_ref2, self.btn_importdata_ref2)
        TabWidget.setTabOrder(self.btn_importdata_ref2, self.btn_showdata_ref2)
        TabWidget.setTabOrder(self.btn_showdata_ref2, self.slc_w_method_ref2)
        TabWidget.setTabOrder(self.slc_w_method_ref2, self.btn_calculate_ref2)
        TabWidget.setTabOrder(self.btn_calculate_ref2, self.btn_results_ref2)
        TabWidget.setTabOrder(self.btn_results_ref2, self.btn_outputtables_ref2)
        # endregion

        ####################################
        # BUTTON CONNECTIONS FOR FUNCTIONS #
        ####################################
        # tab-1 connections
        self.btn_create.clicked.connect(self.generate_mcdm_form)
        self.btn_importdata.clicked.connect(self.import_mcdm_data)
        self.btn_showdata.clicked.connect(self.show_mcdm_data)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_ranking.clicked.connect(self.show_ranking)
        self.btn_outputtables.clicked.connect(self.save_outputs)
        self.btn_aggregate.clicked.connect(self.aggregate)

        # tab-2 connections (REF-I)
        self.btn_create_ref1.clicked.connect(self.generate_form_ref1)
        self.btn_importdata_ref1.clicked.connect(self.import_data_ref1)
        self.btn_showdata_ref1.clicked.connect(self.show_data_ref1)
        self.btn_calculate_ref1.clicked.connect(self.calculate_ref1)
        self.btn_results_ref1.clicked.connect(self.show_results_ref1)
        self.btn_outputtables_ref1.clicked.connect(self.save_outputs_ref1)
        self.btn_guide_ref1.clicked.connect(self.show_ref1_guide)

        # tab-3 connections (REF-II)
        self.btn_create_ref2.clicked.connect(self.generate_form_ref2)
        self.btn_importdata_ref2.clicked.connect(self.import_data_ref2)
        self.btn_showdata_ref2.clicked.connect(self.show_data_ref2)
        self.btn_calculate_ref2.clicked.connect(self.calculate_ref2)
        self.btn_results_ref2.clicked.connect(self.show_results_ref2)
        self.btn_outputtables_ref2.clicked.connect(self.save_outputs_ref2)
        self.btn_guide_ref2.clicked.connect(self.show_ref2_guide)

    def retranslateUi(self, TabWidget):
        pass

    def show_data_winodw(self, df, title):
        self.dataWindow.displayInfo()
        self.dataWindow.update_table(df, title)

    ##########################################
    # METHODS AND AGGREGATION TAB FUNCTIONS  #
    ##########################################
    def generate_mcdm_form(self):
        try:
            num_cr = int(self.txt_num_cr.text())
            num_alt = int(self.txt_num_alt.text())
            df = dataset.create_mcdm_df(num_cr, num_alt)
            default_file = f"{default_dir}/MCDM Data Form.xlsx"
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File", default_file, "Excel File (*.xls)", options=options
            )
            if fileName:
                df.to_excel(fileName)
                show_alert("Succesfully saved.")
        except Exception as ex:
            show_alert("Please check your input values.")
            print(str(ex))

    def import_mcdm_data(self):
        try:
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Import Data File",
                default_dir,
                "Excel Files (*.xlsx)",
                options=options,
            )

            self.mcdm = solver.Solver(fileName, lambda_value=0.5)
            self.mcdm_default_weights = self.mcdm.data.weights

            show_alert("Data imported successfully.")

            self.btn_showdata.setEnabled(True)
            self.btn_calculate.setEnabled(True)

            self.btn_ranking.setDisabled(True)
            self.btn_outputtables.setDisabled(True)
            self.btn_aggregate.setDisabled(True)
        except dataset.DataSetException as ex:
            show_alert(str(ex))
        except Exception as ex:
            show_alert("No data imported.")
            print(str(ex))

    def show_mcdm_data(self):
        if self.mcdm is None:
            show_alert("Please import data.")
        else:
            self.show_data_winodw(self.mcdm.data.df, "User DataSet")

    def check_selected_methods(self):
        selected_methods = []
        if self.cb_topsis.isChecked() == True:
            selected_methods.append("topsis")
        if self.cb_moosra.isChecked() == True:
            selected_methods.append("moosra")
        if self.cb_mabac.isChecked() == True:
            selected_methods.append("mabac")
        if self.cb_psi.isChecked() == True:
            selected_methods.append("psi")
        if self.cb_rov.isChecked() == True:
            selected_methods.append("rov")
        if self.cb_wsm.isChecked() == True:
            selected_methods.append("wsm")
        if self.cb_wpm.isChecked() == True:
            selected_methods.append("wpm")
        if self.cb_waspas.isChecked() == True:
            selected_methods.append("waspas")
        if self.cb_ref1.isChecked() == True:
            selected_methods.append("ref_I")
        if self.cb_ref2.isChecked() == True:
            selected_methods.append("ref_II")

        return selected_methods

    def calculate(self):
        method_list = self.check_selected_methods()
        if len(method_list) == 0:
            show_alert("You must select at least one method.")
            return

        # Get lambda value if WASPAS is selected.
        if self.cb_waspas.isChecked() == True:
            try:
                lambda_value = float(self.txt_lambda.text())
                if 0 <= lambda_value <= 1:
                    self.mcdm.lambda_value = lambda_value
                else:
                    show_alert("Lambda value must be between 0 and 1")
                    return
            except:
                show_alert("Please insert numeric value for lambda.")
                return

        # Check combobox for weighting method
        weighting_method = self.slc_w_method.currentIndex()
        if weighting_method == 0:
            self.mcdm.data.weights = self.mcdm_default_weights
        elif weighting_method == 1:
            self.mcdm.data.weights = weights.equal_weigths(self.mcdm.data.n)
        elif weighting_method == 2:
            self.mcdm.data.weights = weights.entropy(self.mcdm.data.matrix)
        elif weighting_method == 3:
            self.mcdm.data.weights = weights.critic(
                self.mcdm.data.matrix, self.mcdm.data.types
            )
        else:
            pass

        self.mcdm.solve(method_list)
        show_alert("Calculations succesfully completed.")

        self.btn_ranking.setEnabled(True)
        self.btn_outputtables.setEnabled(True)
        self.btn_aggregate.setEnabled(True)

    def show_ranking(self):
        if len(self.mcdm.calculated_ranks_by_methods) > 0:
            calculated_ranks_by_methods = pd.DataFrame(
                self.mcdm.calculated_ranks_by_methods, index=self.mcdm.data.alternatives
            )
            self.show_data_winodw(
                calculated_ranks_by_methods, "Ranking Values of the Methods"
            )
        else:
            show_alert("First, calculate data.")

    def save_outputs(self):
        output_saver(self.mcdm.all_tables, "MCDM Output Tables")

    def aggregate(self):
        if self.comboBox_aggregation.currentIndex() == 0:
            show_alert("Please select an Aggregation Method.")
            return
        elif self.comboBox_aggregation.currentIndex() == 1:
            if self.mcdm == None:
                show_alert("Please first import data and make calculations.")
            elif len(self.mcdm.calculated_ranks_by_methods) == 0:
                show_alert("Please first make calculations.")
            else:
                df = pd.DataFrame(
                    self.mcdm.calculated_ranks_by_methods,
                    index=self.mcdm.data.alternatives,
                )

                weights = [1] * len(df.columns)
                agg = aggregations.borda(df, weights)

                self.show_data_winodw(agg, "Borda Aggregation Results")

    ##################################
    #       REF-I TAB FUNCTIONS      #
    ##################################

    def generate_form_ref1(self):
        try:
            num_binary = int(self.txt_num_binary.text())
            num_nominal = int(self.txt_num_nominal.text())
            num_ordinal = int(self.txt_num_ordinal.text())
            num_cardinal = int(self.txt_num_cardinal.text())
            num_alt = int(self.txt_num_alt_ref1.text())
            df = dataset.create_ref1_df(
                num_binary, num_nominal, num_ordinal, num_cardinal, num_alt
            )
            default_file = f"{default_dir}/REF-I Data Form.xlsx"
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File", default_file, "Excel File (*.xls)", options=options
            )
            if fileName:
                df.to_excel(fileName)
                show_alert("Succesfully saved.")
        except:
            show_alert("Please check your input values.")

    def import_data_ref1(self):
        try:
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Import Data File",
                default_dir,
                "Excel Files (*.xlsx)",
                options=options,
            )

            self.ref1 = ref.Ref1(fileName)

            self.ref1_default_weights = self.ref1.data.weights

            self.btn_showdata_ref1.setEnabled(True)
            self.btn_calculate_ref1.setEnabled(True)
            self.btn_results_ref1.setDisabled(True)
            self.btn_outputtables_ref1.setDisabled(True)

            show_alert("Data imported successfully.")

        except dataset.DataSetException as ex:
            show_alert(str(ex))

        except Exception as ex:
            show_alert("No data imported.")
            print(str(ex))

    def show_data_ref1(self):
        if self.ref1 is None:
            show_alert("No data imported.")
        else:
            self.show_data_winodw(self.ref1.data.df, "User DataSet for REF-I")

    def calculate_ref1(self):
        # Check combobox for weighting method
        weighting_method = self.slc_w_method_ref1.currentIndex()

        if weighting_method == 0:
            self.ref1.data.weights = self.ref1_default_weights
        elif weighting_method == 1:
            self.ref1.data.weights = pd.DataFrame(
                [weights.equal_weigths(self.ref1.data.n)],
                columns=self.ref1.data.criteria,
            )
        else:
            pass

        self.ref1.solve()
        show_alert("Calculations succesfully completed.")

        self.btn_results_ref1.setEnabled(True)
        self.btn_outputtables_ref1.setEnabled(True)

    def show_results_ref1(self):
        self.show_data_winodw(self.ref1.results, "REF-I Results")

    def save_outputs_ref1(self):
        output_saver(self.ref1.all_tables, "REF-I Output Tables")

    def show_ref1_guide(self):
        webbrowser.open(
            "https://github.com/kadirkirda/ka-decision/blob/main/documentation/REF-I.md"
        )

    ###################################
    #      REF-II TAB FUNCTIONS       #
    ###################################

    def generate_form_ref2(self):
        try:
            num_cr = int(self.txt_num_cr_ref2.text())
            num_alt = int(self.txt_num_alt_ref2.text())
            df = dataset.create_ref2_df(num_cr, num_alt)
            default_file = f"{default_dir}/REF-II Data Form.xlsx"
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File", default_file, "Excel File (*.xls)", options=options
            )
            if fileName:
                df.to_excel(fileName)
                show_alert("Succesfully saved.")
        except Exception as ex:
            show_alert("Please check your input values.")
            print(str(ex))

    def import_data_ref2(self):
        try:
            options = QtWidgets.QFileDialog.Option(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog
            )
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Import Data File",
                default_dir,
                "Excel Files (*.xlsx)",
                options=options,
            )

            self.ref2 = ref.Ref2(fileName)

            self.ref2_default_weights = self.ref2.data.weights

            self.btn_showdata_ref2.setEnabled(True)
            self.btn_calculate_ref2.setEnabled(True)
            self.btn_results_ref2.setDisabled(True)
            self.btn_outputtables_ref2.setDisabled(True)

            show_alert("Data imported successfully.")

        except dataset.DataSetException as ex:
            show_alert(str(ex))
        except Exception as ex:
            show_alert("No data imported.")
            print(str(ex))

    def show_data_ref2(self):
        if self.ref2 is None:
            show_alert("No data imported.")
        else:
            self.show_data_winodw(self.ref2.data.df, "User DataSet for REF-II")

    def calculate_ref2(self):
        # Check combobox for weighting method
        weighting_method = self.slc_w_method_ref2.currentIndex()

        if weighting_method == 0:
            self.ref2.data.weights = self.ref2_default_weights
        elif weighting_method == 1:
            self.ref2.data.weights = pd.DataFrame(
                [weights.equal_weigths(self.ref2.data.n)],
                columns=self.ref2.data.criteria,
            )
        elif weighting_method == 2:
            self.ref2.data.weights = pd.DataFrame(
                [weights.entropy(self.ref2.data.matrix)],
                columns=self.ref2.data.criteria,
            )
        elif weighting_method == 3:
            self.ref2.data.weights = pd.DataFrame(
                [weights.critic(self.ref2.data.matrix, [1] * self.ref2.data.m)],
                columns=self.ref2.data.criteria,
            )
        else:
            pass

        self.ref2.solve()
        show_alert("Calculations succesfully completed.")
        print(self.ref2.data.p_values)
        self.btn_results_ref2.setEnabled(True)
        self.btn_outputtables_ref2.setEnabled(True)

    def show_results_ref2(self):
        self.show_data_winodw(self.ref2.results, "REF-II Results")

    def save_outputs_ref2(self):
        output_saver(self.ref2.all_tables, "REF-II Output Tables")

    def show_ref2_guide(self):
        webbrowser.open(
            "https://github.com/kadirkirda/ka-decision/blob/main/documentation/REF-II.md"
        )

    ###################################
    #     DATA PRESENTATION CLASS     #
    ###################################


class DataWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame()
        self.title = ""
        self.resize(694, 569)
        mainLayout = QtWidgets.QVBoxLayout()
        self.mainTable = QtWidgets.QTableWidget()
        mainLayout.addWidget(self.mainTable)
        self.setLayout(mainLayout)

        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.clicked.connect(self.save_results)
        mainLayout.addWidget(self.saveButton)
        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        mainLayout.addWidget(self.closeButton)

    def save_results(self):
        default_file = f"{default_dir}/{self.title}.xlsx"
        options = QtWidgets.QFileDialog.Option(
            QtWidgets.QFileDialog.Option.DontUseNativeDialog
        )
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", default_file, "Excel File (*.xlsx)", options=options
        )
        if fileName:
            self.data.to_excel(fileName)
            show_alert("File saved.")

    def update_table(self, data, title):
        self.title = title
        self.data = data
        NumRows = len(data.index)
        self.setWindowTitle(title)
        self.mainTable.setColumnCount(len(data.columns))
        self.mainTable.setRowCount(NumRows)
        self.mainTable.setHorizontalHeaderLabels(data.columns)
        self.mainTable.setVerticalHeaderLabels(data.index)
        for i in range(NumRows):
            for j in range(len(data.columns)):
                cell_value = str(data.iat[i, j])
                if cell_value == "nan":
                    cell_value = ""
                self.mainTable.setItem(i, j, QtWidgets.QTableWidgetItem(cell_value))

        self.mainTable.resizeColumnsToContents()
        self.mainTable.resizeRowsToContents()

    def displayInfo(self):
        self.show()

    ##################################
    #         HELPER METHODS         #
    ##################################


def show_alert(text):
    alert = QtWidgets.QMessageBox()
    alert.setText(text)
    alert.exec()


def output_saver(tables_dict: dict, output_name: str):
    default_file = f"{default_dir}/{output_name}.xlsx"
    options = QtWidgets.QFileDialog.Option(
        QtWidgets.QFileDialog.Option.DontUseNativeDialog
    )
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
        None, "Save File", default_file, "Excel File (*.xlsx)", options=options
    )
    if fileName:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(fileName, engine="xlsxwriter")

        # Write each dataframe to a different worksheet.

        for key in tables_dict.keys():
            df = tables_dict[key]
            df.to_excel(writer, sheet_name=key)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        show_alert("File saved.")

    ##################################
    #       START APPLICATION        #
    ##################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    sys.exit(app.exec())
