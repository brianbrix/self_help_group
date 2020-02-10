import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView, QMessageBox
import csv
import pandas as pd
import new_member, members_list, new_payment, PandasModel,all_payments, statement


class All_Members(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = members_list.Ui_MainWindow()
        self.ui.setupUi(self)


class Add_Member(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = new_member.Ui_Dialog()
        self.ui.setupUi(self)


class New_Payment(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = new_payment.Ui_Dialog()
        self.ui.setupUi(self)

class All_Payments(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = all_payments.Ui_Frame()
        self.ui.setupUi(self)

class TheApp:
    def __init__(self):
        self.all_members = All_Members()
        self.all_members.show()
        self.displayMembers()
        self.add_member = Add_Member()
        self.new_payment = New_Payment()
        self.all_payments=All_Payments()
        # self.model=PandasModel.PandasModel()
        self.all_members.ui.addMemberBtn.clicked.connect(self.memberDetails)
        self.all_members.ui.members_list.clicked.connect(self.tableHasBeenClicked)
        self.all_members.ui.remove_member_btn.clicked.connect(self.deleteMember)
        self.all_members.ui.add_payment_btn.clicked.connect(self.paymentDetails)
        self.all_members.ui.view_all_payments.clicked.connect(self.viewAllPayments)
        self.new_payment.ui.select_date.toggled.connect(self.radioToggled)
        self.name = ""
        self.national_id = ""
        self.email = ""

    def radioToggled(self):
        if self.new_payment.ui.select_date.isChecked():
            self.new_payment.ui.pay_date.setEnabled(True)
        else:
            self.new_payment.ui.pay_date.setEnabled(False)

    def memberDetails(self):
        self.add_member.ui.member_name.clear()
        self.add_member.ui.member_nat_id.clear()
        self.add_member.ui.member_number.clear()
        self.add_member.ui.member_email.clear()
        self.add_member.ui.phone_number.clear()
        self.add_member.show()
        if self.add_member.exec_():
            self.addMember()

    def addMember(self):
        members_file = 'members.csv'
        with open(members_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self.add_member.ui.member_name.text(), self.add_member.ui.member_nat_id.text(),
                             self.add_member.ui.member_number.text(), self.add_member.ui.phone_number.text(),
                             self.add_member.ui.member_email.text()])
        self.displayMembers()

    def displayMembers(self):
        if os.path.exists("members.csv"):
            df = pd.read_csv('members.csv', names=["NAME", "NATIONAL ID", "MEMBER NUMBER", "PHONE NUMBER", "EMAIL"])
            df = df.reset_index()
            df = df.drop(['index'], axis=1)
            self.model = PandasModel.PandasModel(df)
            self.all_members.ui.members_list.setModel(self.model)
            self.all_members.ui.members_list.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)
            # self.all_members.ui.members_list.resizeRowsToContents()
            self.all_members.ui.members_list.setSelectionBehavior(
                QTableView.SelectRows)
            self.all_members.ui.members_list.font().setPointSize(42);
            self.all_members.ui.members_list.setSortingEnabled(True)

    def tableHasBeenClicked(self):
        self.all_members.ui.remove_member_btn.setEnabled(True)
        self.all_members.ui.add_payment_btn.setEnabled(True)
        self.all_members.ui.statement_btn.setEnabled(True)
        for index in sorted(self.all_members.ui.members_list.selectionModel().selectedRows()):
            row = index.row()
            self.national_id = str(self.model.data(self.model.index(row, 1)).value())
            self.email = str(self.model.data(self.model.index(row, 4)).value())
            self.name = str(self.model.data(self.model.index(row, 0)).value())

    def deleteMember(self):
        lines = list()
        confirm = QMessageBox.question(self.all_members, "Confirm delete",
                                       "Are you sure you want to delete: " + self.name + ": " + self.national_id + "?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            with open('members.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    lines.append(row)
                    if row[1] == self.national_id and row[4] == self.email:
                        lines.remove(row)
            with open('members.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
        self.displayMembers()

    def paymentDetails(self):
        self.new_payment.ui.amount_paid.clear()
        self.new_payment.ui.transaction_code.clear()
        self.new_payment.ui.payment_mode.clear()
        self.new_payment.ui.pay_date.clear()
        self.new_payment.show()
        self.new_payment.ui.payment_for.setText("New Payment By: " + self.name)
        if self.new_payment.exec_():
            self.newPayment()

    def newPayment(self):
        import datetime
        pay_file = 'payment.csv'
        date = None
        if self.new_payment.ui.date_today.isChecked():
            date = datetime.date.today().strftime("%d/%m/%Y")
        else:
            date = self.new_payment.ui.pay_date.date().toString("dd/MM/yyyy")
        with open(pay_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([self.name, self.national_id, date, self.new_payment.ui.amount_paid.text(),
                             self.new_payment.ui.transaction_code.text(), self.new_payment.ui.payment_mode.text()])

    def viewAllPayments(self):
        self.all_payments.show()
        df = pd.read_csv('payment.csv', names=["NAME", "NATIONAL ID", "DATE", "AMOUNT", "TRANSACTION CODE", "PAYMENT MODE"])
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        self.model2 = PandasModel.PandasModel(df)
        self.all_payments.ui.all_payments_view.setModel(self.model2)
        self.all_payments.ui.all_payments_view.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        # self.all_members.ui.members_list.resizeRowsToContents()
        self.all_payments.ui.all_payments_view.setSelectionBehavior(
            QTableView.SelectRows)
        self.all_payments.ui.all_payments_view.font().setPointSize(42);
        self.all_payments.ui.all_payments_view.setSortingEnabled(True)



app = QApplication([])
a = TheApp()
app.exec_()
