# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'members_list.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.members_list = QtWidgets.QTableView(self.centralwidget)
        self.members_list.setEnabled(True)
        self.members_list.setObjectName("members_list")
        self.gridLayout.addWidget(self.members_list, 1, 0, 1, 2)
        self.view_all_payments = QtWidgets.QPushButton(self.centralwidget)
        self.view_all_payments.setObjectName("view_all_payments")
        self.gridLayout.addWidget(self.view_all_payments, 3, 0, 1, 2)
        self.addMemberBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addMemberBtn.setObjectName("addMemberBtn")
        self.gridLayout.addWidget(self.addMemberBtn, 0, 0, 1, 1)
        self.remove_member_btn = QtWidgets.QPushButton(self.centralwidget)
        self.remove_member_btn.setEnabled(False)
        self.remove_member_btn.setObjectName("remove_member_btn")
        self.gridLayout.addWidget(self.remove_member_btn, 0, 1, 1, 1)
        self.statement_btn = QtWidgets.QPushButton(self.centralwidget)
        self.statement_btn.setEnabled(False)
        self.statement_btn.setObjectName("statement_btn")
        self.gridLayout.addWidget(self.statement_btn, 2, 1, 1, 1)
        self.add_payment_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_payment_btn.setEnabled(False)
        self.add_payment_btn.setObjectName("add_payment_btn")
        self.gridLayout.addWidget(self.add_payment_btn, 2, 0, 1, 1)
        self.run_backup = QtWidgets.QPushButton(self.centralwidget)
        self.run_backup.setObjectName("run_backup")
        self.gridLayout.addWidget(self.run_backup, 4, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HOME"))
        self.view_all_payments.setText(_translate("MainWindow", "View All Payments"))
        self.addMemberBtn.setText(_translate("MainWindow", "Add People"))
        self.remove_member_btn.setText(_translate("MainWindow", "Remove Selected"))
        self.statement_btn.setText(_translate("MainWindow", "Download Statement for selected"))
        self.add_payment_btn.setText(_translate("MainWindow", "Add Payment for selected"))
        self.run_backup.setText(_translate("MainWindow", "Backup"))

