# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_payment.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(463, 213)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pay_date = QtWidgets.QDateEdit(Dialog)
        self.pay_date.setEnabled(False)
        self.pay_date.setObjectName("pay_date")
        self.gridLayout.addWidget(self.pay_date, 5, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.select_date = QtWidgets.QRadioButton(Dialog)
        self.select_date.setObjectName("select_date")
        self.gridLayout.addWidget(self.select_date, 4, 2, 1, 1)
        self.payment_mode = QtWidgets.QLineEdit(Dialog)
        self.payment_mode.setObjectName("payment_mode")
        self.gridLayout.addWidget(self.payment_mode, 3, 1, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.amount_paid = QtWidgets.QLineEdit(Dialog)
        self.amount_paid.setObjectName("amount_paid")
        self.gridLayout.addWidget(self.amount_paid, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.date_today = QtWidgets.QRadioButton(Dialog)
        self.date_today.setChecked(True)
        self.date_today.setObjectName("date_today")
        self.gridLayout.addWidget(self.date_today, 4, 1, 1, 1)
        self.transaction_code = QtWidgets.QLineEdit(Dialog)
        self.transaction_code.setObjectName("transaction_code")
        self.gridLayout.addWidget(self.transaction_code, 2, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.payment_for = QtWidgets.QLabel(Dialog)
        self.payment_for.setText("")
        self.payment_for.setObjectName("payment_for")
        self.gridLayout.addWidget(self.payment_for, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Amount:"))
        self.label_3.setText(_translate("Dialog", "Date/Time;"))
        self.select_date.setText(_translate("Dialog", "Select Date"))
        self.payment_mode.setText(_translate("Dialog", "MPESA"))
        self.label_2.setText(_translate("Dialog", "Transaction Code:"))
        self.date_today.setText(_translate("Dialog", "Today"))
        self.label_4.setText(_translate("Dialog", "Payment Mode:"))
