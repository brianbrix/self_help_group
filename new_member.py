# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_member.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(489, 199)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.member_number = QtWidgets.QLineEdit(Dialog)
        self.member_number.setObjectName("member_number")
        self.gridLayout.addWidget(self.member_number, 2, 1, 1, 1)
        self.phone_number = QtWidgets.QLineEdit(Dialog)
        self.phone_number.setObjectName("phone_number")
        self.gridLayout.addWidget(self.phone_number, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.member_nat_id = QtWidgets.QLineEdit(Dialog)
        self.member_nat_id.setObjectName("member_nat_id")
        self.gridLayout.addWidget(self.member_nat_id, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.member_email = QtWidgets.QLineEdit(Dialog)
        self.member_email.setObjectName("member_email")
        self.gridLayout.addWidget(self.member_email, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.member_name = QtWidgets.QLineEdit(Dialog)
        self.member_name.setObjectName("member_name")
        self.gridLayout.addWidget(self.member_name, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "Email: "))
        self.member_number.setPlaceholderText(_translate("Dialog", "TECH/12345"))
        self.phone_number.setPlaceholderText(_translate("Dialog", "07xxxxxxxxx"))
        self.label_2.setText(_translate("Dialog", "Id Number:"))
        self.member_nat_id.setPlaceholderText(_translate("Dialog", "34555566"))
        self.label_4.setText(_translate("Dialog", "Membership No:"))
        self.member_email.setPlaceholderText(_translate("Dialog", "email@mail.com"))
        self.label_3.setText(_translate("Dialog", "Phone Number:"))
        self.label.setText(_translate("Dialog", "Name:"))
        self.member_name.setPlaceholderText(_translate("Dialog", "FirstName LastName"))
