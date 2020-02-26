import csv
import datetime
import os
from functools import partial

import pandas as pd
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView, QMessageBox, QFileDialog, QShortcut, \
    QAbstractItemView

import PandasModel
import all_payments
import members_list
import new_member
import new_payment
import print_statement
import statement


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
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = all_payments.Ui_Frame()
        self.ui.setupUi(self)


class PrintStatement(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = print_statement.Ui_PrintStatement()
        self.ui.setupUi(self)


class TheApp:
    def __init__(self):
        self.all_members = All_Members()
        self.all_members.show()
        self.displayMembers()
        self.add_member = Add_Member()
        self.new_payment = New_Payment()
        self.all_payments = All_Payments()
        self.print_statement = PrintStatement()
        # self.model=PandasModel.PandasModel()
        self.all_members.ui.addMemberBtn.clicked.connect(self.memberDetails)
        self.all_members.ui.members_list.clicked.connect(self.tableHasBeenClicked)
        self.all_members.ui.remove_member_btn.clicked.connect(self.deleteMember)
        self.all_members.ui.add_payment_btn.clicked.connect(self.paymentDetails)
        self.all_members.ui.view_all_payments.clicked.connect(self.viewAllPayments)
        self.all_members.ui.statement_btn.clicked.connect(self.printStatement)
        self.new_payment.ui.select_date.toggled.connect(self.radioToggled)
        self.print_statement.ui.yearly.toggled.connect(self.printRadioToggled)
        self.print_statement.ui.monthly.toggled.connect(self.printRadioToggled)
        self.print_statement.ui.quaterly.toggled.connect(self.printRadioToggled)
        self.all_payments.ui.all_payments_view.clicked.connect(partial(self.all_payments.ui.delete_selected_button.setEnabled,True))
        # self.all_payments.ui.all_payments_view.setEditTriggers(QAbstractItemView.SelectedClicked)
        # keyPress=QShortcut(QKeySequence(Qt.Qt.Key_Return), self.all_payments.ui.all_payments_view)
        # keyPress.activated.connect(self.editPayment)
        self.all_payments.ui.delete_selected_button.clicked.connect(self.deletePayment)
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                            "October", "November", "December"]
        quarters = ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"]
        years_back = 5
        year = datetime.datetime.today().year
        YEARS = [str(year - i) for i in range(years_back + 1)]
        self.print_statement.ui.select_month.addItems(months)
        self.print_statement.ui.select_year.addItems(YEARS)
        self.print_statement.ui.select_quarter.addItems(quarters)
        self.name = ""
        self.national_id = ""
        self.email = ""
        self.paragraph = {}

    def keyPressEvent(self, e):
        print("event", e)
        if e.key() == Qt.Qt.Key_Return or e.key() == Qt.Qt.Key_Enter:
            print(' return')

    def deletePayment(self):
        name = ""
        t_code = ""
        amount = ""
        for index in sorted(self.all_payments.ui.all_payments_view.selectionModel().selectedRows()):
            row = index.row()
            t_code = str(self.model2.data(self.model2.index(row, 4)).value())
            amount = str(self.model2.data(self.model2.index(row, 3)).value())
            name = str(self.model2.data(self.model2.index(row, 0)).value())
        lines = list()
        confirm = QMessageBox.question(self.all_payments, "Confirm delete",
                                       "Are you sure you want to delete transaction " + t_code + " of Ksh " + amount + " for " + name + "?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            with open('payment.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    lines.append(row)
                    if row[0] == name and row[4] == t_code:
                        lines.remove(row)
            with open('payment.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
        self.viewAllPayments()
        self.all_payments.ui.delete_selected_button.setEnabled(False)

    def printStatement(self):
        self.printRadioToggled()
        quarterly = False
        self.print_statement.show()
        if self.print_statement.exec_():
            fileName, _ = QFileDialog.getSaveFileName(
                self.all_members, 'Save as... File', './', filter='PDF Files(*.pdf)')
            if fileName:
                df = pd.read_csv("payment.csv",
                                 names=["NAME", "NATIONAL ID", "DATE", "AMOUNT", "TRANSACTION CODE", "PAYMENT MODE"])
                df = df[df["NAME"] == self.name]

                df = df[df["NATIONAL ID"] == int(self.national_id)]
                df = df.drop(columns=['NAME', 'NATIONAL ID'])
                df2 = pd.DataFrame(columns=df.columns)
                year = str(self.print_statement.ui.select_year.currentText())
                month = str(self.print_statement.ui.select_month.currentText())
                selected_quarter = str(self.print_statement.ui.select_quarter.currentText())
                if self.print_statement.ui.monthly.isChecked():
                    for index, row in df.iterrows():
                        if month + "/" + year in str(row['DATE']):
                            df2 = df2.append(row, ignore_index=True)
                    totals = ["TOTAL", df2["AMOUNT"].apply(pd.to_numeric).sum(), "", ""]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    self.paragraph["Period"] = self.month_names[int(month) - 1] + "\t" + year
                elif self.print_statement.ui.yearly.isChecked():
                    for index, row in df.iterrows():
                        if year in str(row['DATE']):
                            df2 = df2.append(row, ignore_index=True)
                    totals = ["TOTAL", df2["AMOUNT"].apply(pd.to_numeric).sum(), "", ""]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    self.paragraph["Period"] = "Year " + year
                elif self.print_statement.ui.quaterly.isChecked():
                    monthly = []
                    if selected_quarter == "First Quarter":
                        monthly.append({"Month": "January", "Total": ""})
                        monthly.append({"Month": "February", "Total": ""})
                        monthly.append({"Month": "March", "Total": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if year in str(row['DATE']):
                                if "01" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "January":
                                            x["Total"] = str(first_monthly_sum)
                                if "02" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "February":
                                            x["Total"] = str(second_monthly_sum)
                                if "03" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "March":
                                            x["Total"] = str(third_mothly_sum)
                    if selected_quarter == "Second Quarter":
                        monthly.append({"Month": "April", "Total": ""})
                        monthly.append({"Month": "May", "Total": ""})
                        monthly.append({"Month": "June", "Total": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if year in str(row['DATE']):
                                if "04" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "April":
                                            x["Total"] = str(first_monthly_sum)
                                if "05" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "May":
                                            x["Total"] = str(second_monthly_sum)
                                if "06" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "June":
                                            x["Total"] = str(third_mothly_sum)
                    if selected_quarter == "Third Quarter":
                        monthly.append({"Month": "July", "Total": ""})
                        monthly.append({"Month": "August", "Total": ""})
                        monthly.append({"Month": "September", "Total": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if year in str(row['DATE']):
                                if "07" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "July":
                                            x["Total"] = str(first_monthly_sum)
                                if "08" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "August":
                                            x["Total"] = str(second_monthly_sum)
                                if "09" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "September":
                                            x["Total"] = str(third_mothly_sum)
                    if selected_quarter == "Fourth Quarter":
                        monthly.append({"Month": "October", "Total": ""})
                        monthly.append({"Month": "November", "Total": ""})
                        monthly.append({"Month": "December", "Total": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if year in str(row['DATE']):
                                if "10" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "October":
                                            x["Total"] = str(first_monthly_sum)
                                if "11" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "November":
                                            x["Total"] = str(second_monthly_sum)
                                if "12" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "December":
                                            x["Total"] = str(third_mothly_sum)

                    df2 = pd.DataFrame.from_records(monthly)
                    df2.columns = map(str.upper, df2.columns)
                    totals = ["TOTAL QUARTERLY", df2["AMOUNT"].apply(pd.to_numeric).sum()]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    self.paragraph["Period"] = "Year " + year + " " + selected_quarter
                    quarterly = True
                statement.render_statement(df2, self.paragraph, quarterly, fileName)

    def printRadioToggled(self):
        if self.print_statement.ui.yearly.isChecked():
            self.print_statement.ui.select_year.setEnabled(True)
            self.print_statement.ui.select_month.setEnabled(False)
            self.print_statement.ui.select_quarter.setEnabled(False)
        if self.print_statement.ui.monthly.isChecked():
            self.print_statement.ui.select_year.setEnabled(True)
            self.print_statement.ui.select_month.setEnabled(True)
            self.print_statement.ui.select_quarter.setEnabled(False)
        if self.print_statement.ui.quaterly.isChecked():
            self.print_statement.ui.select_year.setEnabled(True)
            self.print_statement.ui.select_month.setEnabled(False)
            self.print_statement.ui.select_quarter.setEnabled(True)

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
            membr_no = str(self.model.data(self.model.index(row, 2)).value())
            phone_no = str(self.model.data(self.model.index(row, 3)).value())
        self.paragraph["Member's Name"] = self.name
        self.paragraph["National ID"] = self.national_id
        self.paragraph["Membership Number"] = membr_no
        self.paragraph["Phone Number"] = phone_no
        self.paragraph["Official Email"] = self.email

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
        df = pd.read_csv('payment.csv',
                         names=["NAME", "NATIONAL ID", "DATE", "AMOUNT", "TRANSACTION CODE", "PAYMENT MODE"])
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
