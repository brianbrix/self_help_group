# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'print_statement.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrintStatement(object):
    def setupUi(self, PrintStatement):
        PrintStatement.setObjectName("PrintStatement")
        PrintStatement.resize(600, 268)
        self.gridLayout = QtWidgets.QGridLayout(PrintStatement)
        self.gridLayout.setObjectName("gridLayout")
        self.monthly = QtWidgets.QRadioButton(PrintStatement)
        self.monthly.setChecked(True)
        self.monthly.setObjectName("monthly")
        self.gridLayout.addWidget(self.monthly, 0, 2, 1, 1)
        self.quaterly = QtWidgets.QRadioButton(PrintStatement)
        self.quaterly.setObjectName("quaterly")
        self.gridLayout.addWidget(self.quaterly, 0, 3, 1, 2)
        self.select_year = QtWidgets.QComboBox(PrintStatement)
        self.select_year.setObjectName("select_year")
        self.gridLayout.addWidget(self.select_year, 1, 1, 1, 1)
        self.select_month = QtWidgets.QComboBox(PrintStatement)
        self.select_month.setObjectName("select_month")
        self.gridLayout.addWidget(self.select_month, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(PrintStatement)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(PrintStatement)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(PrintStatement)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 3, 1, 2)
        self.yearly = QtWidgets.QRadioButton(PrintStatement)
        self.yearly.setObjectName("yearly")
        self.gridLayout.addWidget(self.yearly, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(PrintStatement)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.select_quarter = QtWidgets.QComboBox(PrintStatement)
        self.select_quarter.setObjectName("select_quarter")
        self.gridLayout.addWidget(self.select_quarter, 2, 1, 1, 1)

        self.retranslateUi(PrintStatement)
        self.buttonBox.accepted.connect(PrintStatement.accept)
        self.buttonBox.rejected.connect(PrintStatement.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintStatement)

    def retranslateUi(self, PrintStatement):
        _translate = QtCore.QCoreApplication.translate
        PrintStatement.setWindowTitle(_translate("PrintStatement", "Print Statement"))
        self.monthly.setText(_translate("PrintStatement", "Monthly"))
        self.quaterly.setText(_translate("PrintStatement", "Quarterly"))
        self.label.setText(_translate("PrintStatement", "Select Year:"))
        self.label_2.setText(_translate("PrintStatement", "Select Month:"))
        self.yearly.setText(_translate("PrintStatement", "Yearly"))
        self.label_3.setText(_translate("PrintStatement", "Select Quarter:"))
