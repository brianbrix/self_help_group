import csv
import datetime
import os, platform
from functools import partial

from PyQt5.QtCore import QTimer, QDateTime

try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except Exception as e:
    print(e)

import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView, QMessageBox, QFileDialog, QShortcut, \
    QAbstractItemView, QFrame

import PandasModel
import all_payments
import members_list
import new_member
import new_payment
import print_statement
import statement
import subprocess
import homepage
import pymysql as mdb

operating_system = platform.system()


def ping(target):
    print(subprocess.call(['ping', target]))
    return True if subprocess.call(['ping', target]) == 0 else False


# Client ID:56840225204-2l4pp6r6ohfd7csh761p4mqq6gupbdkb.apps.googleusercontent.com
# Client Secret: SWwST6so3xCzfibL2aU1sZ_k
# try:
#     os.chmod("C:/Users/ALEX/Desktop/slef_help/payment.csv", 0o777)
#     os.chmod("C:/Users/ALEX/Desktop/slef_help/members.csv", 0o777)
# except Exception as e:
#     print(e)


class All_Members(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = members_list.Ui_MainWindow()
        self.ui.closeEvent = self.closeEvent
        self.ui.setupUi(self)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT",
                                               "Are you sure want to quit?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class HomePage(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = homepage.Ui_HomePage()
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
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = print_statement.Ui_PrintStatement()
        self.ui.setupUi(self)


class TheApp:
    def __init__(self):
        self.all_members = All_Members()
        self.add_member = Add_Member()
        self.new_payment = New_Payment()
        self.all_payments = All_Payments()
        self.print_statement = PrintStatement()
        self.home_page = HomePage()
        self.home_page.show()
        self.home_page.ui.stackedWidget.setCurrentIndex(0)
        self.home_page.ui.continue_to_app.clicked.connect(partial(self.home_page.ui.stackedWidget.setCurrentIndex, 1))
        self.home_page.ui.csv_engine.clicked.connect(self.selectDataEngine)
        self.home_page.ui.database_eng.clicked.connect(self.selectDataEngine)
        # self.model=PandasModel.PandasModel()
        self.home_page.ui.addMemberBtn.clicked.connect(self.memberDetails)
        self.home_page.ui.members_list.clicked.connect(self.tableHasBeenClicked)
        self.home_page.ui.remove_member_btn.clicked.connect(self.deleteMember)
        self.home_page.ui.add_payment_btn.clicked.connect(self.paymentDetails)
        self.home_page.ui.view_all_payments.clicked.connect(self.viewAllPayments)
        self.home_page.ui.statement_btn.clicked.connect(self.printStatement)
        self.new_payment.ui.select_date.toggled.connect(self.radioToggled)
        self.print_statement.ui.yearly.toggled.connect(self.printRadioToggled)
        self.print_statement.ui.monthly.toggled.connect(self.printRadioToggled)
        self.print_statement.ui.quaterly.toggled.connect(self.printRadioToggled)
        self.home_page.ui.run_backup.clicked.connect(self.runBackup)
        self.all_payments.ui.all_payments_view.clicked.connect(
            partial(self.all_payments.ui.delete_selected_button.setEnabled, True))
        # self.all_payments.ui.all_payments_view.setEditTriggers(QAbstractItemView.SelectedClicked)
        keyPress = QShortcut(QKeySequence(Qt.Qt.Key_Escape), self.home_page.ui.members_list)
        keyPress2 = QShortcut(QKeySequence(Qt.Qt.Key_Backspace), self.home_page.ui.members_list)
        keyPress.activated.connect(partial(self.home_page.ui.stackedWidget.setCurrentIndex, 0))
        keyPress2.activated.connect(partial(self.home_page.ui.stackedWidget.setCurrentIndex, 0))
        self.all_payments.ui.delete_selected_button.clicked.connect(self.deletePayment)
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                            "October", "November", "December"]
        quarters = ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"]
        years_back = 5
        self.con = None
        year = datetime.datetime.today().year
        YEARS = [str(year - i) for i in range(years_back + 1)]
        self.print_statement.ui.select_month.addItems(months)
        self.print_statement.ui.select_year.addItems(YEARS)
        self.print_statement.ui.select_quarter.addItems(quarters)
        self.name = ""
        self.national_id = ""
        self.email = ""
        self.paragraph = {}
        # for child in self.home_page.ui.frame.children():
        #     if child.objectName() == "turn_db_on":
        #         child.clicked.connect(self.turnOnDb)
        # for child in self.home_page.ui.frame.children():
        #     if child.objectName() == "csv_folder_select":
        #         child.clicked.connect(self.selectCsvFilesFolder)

    def keyPressEvent(self, e):
        print("event", e)
        if e.key() == Qt.Qt.Key_Return or e.key() == Qt.Qt.Key_Enter:
            print(' return')

    def selectDataEngine(self):
        if self.home_page.ui.csv_engine.isChecked():
            self.home_page.ui.label_3.setEnabled(True)
            self.home_page.ui.csv_folder_select.setEnabled(True)
            confirm = QMessageBox.question(self.home_page, "Confirm Engine", "Continue with CSV Files",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.selectCsvFilesFolder()
                os.environ["DATA_ENGINE"] = "CSV_ENGINE"
                self.displayMembers()
        if self.home_page.ui.database_eng.isChecked():
            self.home_page.ui.label_3.setEnabled(False)
            self.home_page.ui.csv_folder_select.setEnabled(False)
            confirm = QMessageBox.question(self.home_page, "Confirm Engine", "Continue with MySQl Database",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.turnOnDb()
                self.displayMembers()

    def turnOnDb(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'self_help_group')
            QMessageBox.about(self.home_page, 'Connection', 'Database Connected Successfully')
            os.environ["DATA_ENGINE"] = "DATABASE_ENGINE"
        except mdb.Error as e:
            print(e)
            QMessageBox.about(self.home_page, 'Connection', 'Failed To Connect Database')

    def selectCsvFilesFolder(self):
        folder = QFileDialog.getExistingDirectory(self.home_page, "Select Directory")
        try:
            payments_file = os.path.join(folder, "payment.csv")
            members_file = os.path.join(folder, "members.csv")
            if not os.path.exists(payments_file):
                open(payments_file, "w")
            if not os.path.exists(members_file):
                open(members_file, "w")
            os.environ["PAYMENTS_FILE"] = str(payments_file)
            os.environ["MEMBERS_FILE"] = str(members_file)
            os.chmod(payments_file, 0o777)
            os.chmod(members_file, 0o777)
            self.home_page.ui.csv_folder_select.setText(str(folder))
        except Exception as e:
            print(e)

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
        confirm = QMessageBox.question(self.all_payments, "Confirm Delete",
                                       "Are you sure you want to delete transaction " + t_code + " of Ksh " + amount + " for " + name + "?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
                try:
                    cur = self.con.cursor()
                    sql = """DELETE FROM payment WHERE NAME=%s AND transactionCode=%s"""
                    cur.execute(sql,(name,t_code))
                    self.con.commit()
                except Exception as e:
                    QMessageBox.critical(self.home_page, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.home_page, "Success", "The payment was deleted successfully",
                                            QMessageBox.Ok)
            else:
                try:
                    with open(os.environ["PAYMENTS_FILE"], 'r') as readFile:
                        reader = csv.reader(readFile)
                        for row in reader:
                            if len(row) > 2:
                                lines.append(row)
                                if row[0] == name and row[4] == t_code:
                                    lines.remove(row)
                    with open(os.environ["PAYMENTS_FILE"], 'w') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerows(lines)
                except Exception as e:
                    QMessageBox.critical(self.home_page, "Error", str(e),
                                             QMessageBox.Ok)
                else:
                    QMessageBox.information(self.home_page, "Success", "The payment was deleted successfully",
                                            QMessageBox.Ok)
        self.viewAllPayments()
        self.all_payments.ui.delete_selected_button.setEnabled(False)
        # self.backupFile("C:/Users/ALEX/Desktop/slef_help/payment.csv","payment.csv")

    def format(self, x):
        return "{:.2f}".format(float(x))

    def printStatement(self):
        temp_path = ""
        if operating_system == 'Windows':
            temp_path = os.path.join(os.path.expanduser(
                '~'), 'Downloads/').replace('\\\\', '\\')
        if operating_system == 'Linux':
            temp_path = os.path.join(
                os.path.expanduser('~'),
                'Downloads/')
        self.printRadioToggled()
        quarterly = False
        self.print_statement.show()
        if self.print_statement.exec_():
            fileName, _ = QFileDialog.getSaveFileName(
                self.all_members, 'Save as... File', temp_path, filter='PDF Files(*.pdf)')
            if fileName:
                df = pd.read_csv(os.environ["PAYMENTS_FILE"],
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
                    if "," in df2["AMOUNT"]:
                        df2["AMOUNT"] = df2["AMOUNT"].str.replace(",", "")
                    totals = ["TOTAL", df2["AMOUNT"].apply(pd.to_numeric).sum(), "", ""]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    df2 = df2.rename(columns={"AMOUNT": "AMOUNT(KSHs)"})
                    # df2["AMOUNT"]= df2["AMOUNT"].apply(self.format)
                    self.paragraph["Period"] = self.month_names[int(month) - 1] + " " + year
                elif self.print_statement.ui.yearly.isChecked():
                    for index, row in df.iterrows():
                        if year in str(row['DATE']):
                            df2 = df2.append(row, ignore_index=True)
                    if "," in df2["AMOUNT"]:
                        df2["AMOUNT"] = df2["AMOUNT"].str.replace(",", "")
                    totals = ["TOTAL", df2["AMOUNT"].apply(pd.to_numeric).sum(), "", ""]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    df2 = df2.rename(columns={"AMOUNT": "AMOUNT(KSHs)"})
                    # df2["AMOUNT"]= df2["AMOUNT"].apply(self.format)
                    self.paragraph["Period"] = "Year " + year
                elif self.print_statement.ui.quaterly.isChecked():
                    monthly = []
                    if selected_quarter == "First Quarter":
                        monthly.append({"Month": "January", "Amount": ""})
                        monthly.append({"Month": "February", "Amount": ""})
                        monthly.append({"Month": "March", "Amount": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if "," in str(row["AMOUNT"]):
                                row["AMOUNT"] = row["AMOUNT"].str.replace(",", "")
                            if year in str(row['DATE']):
                                if "01" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "January":
                                            x["Amount"] = str(first_monthly_sum)
                                if "02" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "February":
                                            x["Amount"] = str(second_monthly_sum)
                                if "03" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "March":
                                            x["Amount"] = str(third_mothly_sum)
                    if selected_quarter == "Second Quarter":
                        monthly.append({"Month": "April", "Amount": ""})
                        monthly.append({"Month": "May", "Amount": ""})
                        monthly.append({"Month": "June", "Amount": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if "," in str(row["AMOUNT"]):
                                row["AMOUNT"] = row["AMOUNT"].str.replace(",", "")
                            if year in str(row['DATE']):
                                if "04" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "April":
                                            x["Amount"] = str(first_monthly_sum)
                                if "05" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "May":
                                            x["Amount"] = str(second_monthly_sum)
                                if "06" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "June":
                                            x["Amount"] = str(third_mothly_sum)
                    if selected_quarter == "Third Quarter":
                        monthly.append({"Month": "July", "Amount": ""})
                        monthly.append({"Month": "August", "Amount": ""})
                        monthly.append({"Month": "September", "Amount": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if "," in str(row["AMOUNT"]):
                                row["AMOUNT"] = row["AMOUNT"].str.replace(",", "")
                            if year in str(row['DATE']):
                                if "07" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "July":
                                            x["Amount"] = str(first_monthly_sum)
                                if "08" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "August":
                                            x["Amount"] = str(second_monthly_sum)
                                if "09" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "September":
                                            x["Amount"] = str(third_mothly_sum)
                    if selected_quarter == "Fourth Quarter":
                        monthly.append({"Month": "October", "Amount": ""})
                        monthly.append({"Month": "November", "Amount": ""})
                        monthly.append({"Month": "December", "Amount": ""})
                        first_monthly_sum = 0
                        second_monthly_sum = 0
                        third_mothly_sum = 0
                        for index, row in df.iterrows():
                            if "," in str(row["AMOUNT"]):
                                row["AMOUNT"] = row["AMOUNT"].str.replace(",", "")
                            if year in str(row['DATE']):
                                if "10" in str(row["DATE"]).split("/")[1]:
                                    first_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "October":
                                            x["Amount"] = str(first_monthly_sum)
                                if "11" in str(row["DATE"]).split("/")[1]:
                                    second_monthly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "November":
                                            x["Amount"] = str(second_monthly_sum)
                                if "12" in str(row["DATE"]).split("/")[1]:
                                    third_mothly_sum += float(row["AMOUNT"])
                                    for x in monthly:
                                        if x["Month"] == "December":
                                            x["Amount"] = str(third_mothly_sum)

                    df2 = pd.DataFrame.from_records(monthly)
                    df2.columns = map(str.upper, df2.columns)
                    if "," in df2["AMOUNT"]:
                        df2["AMOUNT"] = df2["AMOUNT"].str.replace(",", "")
                    totals = ["TOTAL QUARTERLY", df2["AMOUNT"].apply(pd.to_numeric).sum()]
                    a_series = pd.Series(totals, index=df2.columns)
                    df2 = df2.append(a_series, ignore_index=True)
                    df2.replace('', float(0), inplace=True)
                    df2 = df2.rename(columns={"AMOUNT": "AMOUNT(KSHs)"})
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
        if self.add_member.ui.member_name.text() != "" and self.add_member.ui.member_nat_id.text() != "" and self.add_member.ui.member_number.text() != "" and self.add_member.ui.phone_number.text() != "" and self.add_member.ui.member_email.text() != "":
            if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
                try:
                    cur = self.con.cursor()
                    sql = """INSERT INTO members(NAME, idNumber, meberId, phoneNo, memberEmail) VALUES(%s, %s, 
                                   %s, %s, %s) """
                    cur.execute(sql,(self.add_member.ui.member_name.text(), self.add_member.ui.member_nat_id.text(),
                                         self.add_member.ui.member_number.text(), self.add_member.ui.phone_number.text(),
                                         self.add_member.ui.member_email.text()))
                    self.con.commit()
                except Exception as e:
                    QMessageBox.critical(self.add_member,  "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.add_member, "Success", "The new member was added successfully",
                                         QMessageBox.Ok)
            else:
                members_file = os.environ["MEMBERS_FILE"]
                try:
                    with open(members_file, 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([self.add_member.ui.member_name.text(), self.add_member.ui.member_nat_id.text(),
                                         self.add_member.ui.member_number.text(), self.add_member.ui.phone_number.text(),
                                         self.add_member.ui.member_email.text()])
                except Exception as e:
                    QMessageBox.critical(self.add_member, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.add_member, "Success", "The new member was added successfully",
                                            QMessageBox.Ok)
        else:
            QMessageBox.critical(self.add_member, "Field Error", "All fields must be filled to continue",
                                 QMessageBox.Ok)
            self.add_member.show()
        self.displayMembers()

    def displayMembers(self):
        try:
            df = None
            if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
                with self.con:
                    cur = self.con.cursor()
                    cur.execute("SELECT NAME, idNumber, meberId, phoneNo,memberEmail FROM members")
                    rows = list(list(x) for x in cur.fetchall())
                df = pd.DataFrame(rows, columns=["NAME", "NATIONAL ID", "MEMBER NUMBER", "PHONE NUMBER", "EMAIL"])
            else:
                if os.path.exists(os.environ["MEMBERS_FILE"]):
                    df = pd.read_csv(os.environ["MEMBERS_FILE"],
                                     names=["NAME", "NATIONAL ID", "MEMBER NUMBER", "PHONE NUMBER", "EMAIL"])
                    # df["NATIONAL ID"] = df["NATIONAL ID"].astype(int)
                    # df["PHONE NUMBER"] = df["PHONE NUMBER"].astype(int)
            df = df.reset_index()
            df = df.drop(['index'], axis=1)
            df.dropna(inplace=True)
            self.model = PandasModel.PandasModel(df)
            self.home_page.ui.members_list.setModel(self.model)
            self.home_page.ui.members_list.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)
            # self.home_page.ui.members_list.resizeRowsToContents()
            self.home_page.ui.members_list.setSelectionBehavior(
                QTableView.SelectRows)
            self.home_page.ui.members_list.font().setPointSize(42)
            self.home_page.ui.members_list.setSortingEnabled(True)

        except Exception as e:
            print(e)

    def tableHasBeenClicked(self):
        phone_no = ""
        membr_no = ""
        self.home_page.ui.remove_member_btn.setEnabled(True)
        self.home_page.ui.add_payment_btn.setEnabled(True)
        self.home_page.ui.statement_btn.setEnabled(True)
        for index in sorted(self.home_page.ui.members_list.selectionModel().selectedRows()):
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
        confirm = QMessageBox.question(self.home_page, "Confirm delete",
                                       "Are you sure you want to delete: " + self.name + ": " + self.national_id + "?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
                try:
                    cur = self.con.cursor()
                    sql = """DELETE FROM members WHERE idNumber=%s AND memberEmail=%s"""
                    cur.execute(sql,(self.national_id,self.email))
                    self.con.commit()
                except Exception as e:
                    QMessageBox.critical(self.home_page, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.home_page, "Success", "The user was deleted successfully",
                                            QMessageBox.Ok)
            else:
                try:
                    with open(os.environ["MEMBERS_FILE"], 'r') as readFile:
                        reader = csv.reader(readFile)
                        x = 0
                        for row in reader:
                            if len(row) > 2:
                                lines.append(row)
                                if row[1] == str(self.national_id) and row[4] == self.email:
                                    lines.remove(row)
                                x += 1
                    with open(os.environ["MEMBERS_FILE"], 'w') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerows(lines)
                except Exception as e:
                    QMessageBox.critical(self.home_page, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.home_page, "Success", "The user was deleted successfully",
                                            QMessageBox.Ok)
        self.displayMembers()
        # self.backupFile("C:/Users/ALEX/Desktop/slef_help/members.csv","members.csv")

    def paymentDetails(self):
        self.new_payment.ui.amount_paid.clear()
        self.new_payment.ui.transaction_code.clear()
        self.new_payment.ui.payment_mode.clear()
        self.new_payment.ui.pay_date.clear()
        self.new_payment.show()
        self.new_payment.ui.payment_for.setText("New Payment By: " + self.name + "    Date format(m/d/yyyy)")
        if self.new_payment.exec_():
            self.newPayment()

    def runBackup(self):
        file_names_list = ["payment.csv", "members.csv"]
        file_paths_list = [os.environ["PAYMENTS_FILE"], os.environ["MEMBERS_FILE"]]
        for x in range(len(file_names_list)):
            self.backupFile(file_paths_list[x], file_names_list[x])

    def backupFile(self, file_path, file_name):
        try:
            if ping('8.8.8.8'):
                g_login = GoogleAuth()
                g_login.LocalWebserverAuth()
                drive = GoogleDrive(g_login)
                file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
                for file1 in file_list:
                    if file1['title'] == file_name:
                        file1.Delete()
                f = drive.CreateFile({'title': file_name})
                f.SetContentFile(file_path)
                f.Upload()
                QMessageBox.information(self.all_members, "Backup success",
                                        "Successful backup of the file: " + file_path, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.all_members, "Backup Warning",
                                    "Cannot backup the file: " + file_path + "due to internet unaivalabilty. This can "
                                                                             "only be done when connected to the "
                                                                             "internet.",
                                    QMessageBox.Ok)

        except Exception as e:
            print(e)
    #     """
    # reset table IDs
    # SET @num := 0;
    # UPDATE tablename SET id = @num := (@num+1);
    # ALTER TABLE tablename AUTO_INCREMENT = 1;
    #
    # """
    def newPayment(self):
        import datetime
        date = None
        if self.new_payment.ui.date_today.isChecked():
            date = datetime.date.today().strftime("%d/%m/%Y")
        else:
            date = self.new_payment.ui.pay_date.date().toString("dd/MM/yyyy")
        if self.new_payment.ui.amount_paid.text() != "" and self.new_payment.ui.transaction_code.text() != "" and self.new_payment.ui.payment_mode.text() != "":
            if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
                try:
                    cur = self.con.cursor()
                    sql = """INSERT INTO payment(NAME, idNumber, paymentDate, amount, transactionCode, mode) VALUES(%s, %s, 
                    %s, %s, %s, %s) """
                    cur.execute(sql,(self.name, self.national_id, date, self.new_payment.ui.amount_paid.text(),
                                         self.new_payment.ui.transaction_code.text(),
                                         self.new_payment.ui.payment_mode.text()))
                    self.con.commit()
                except Exception as e:
                    QMessageBox.critical(self.new_payment, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.new_payment, "Success", "The payment was added successfully",
                                            QMessageBox.Ok)

            else:
                pay_file = os.environ["PAYMENTS_FILE"]
                try:
                    with open(pay_file, 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([self.name, self.national_id, date, self.new_payment.ui.amount_paid.text(),
                                         self.new_payment.ui.transaction_code.text(),
                                         self.new_payment.ui.payment_mode.text()])
                except Exception as e:
                    QMessageBox.critical(self.new_payment, "Error", str(e),
                                         QMessageBox.Ok)
                else:
                    QMessageBox.information(self.new_payment, "Success", "The payment was added successfully",
                                            QMessageBox.Ok)

        else:
            QMessageBox.critical(self.new_payment, "Field Error", "All fields must be filled to continue",
                                 QMessageBox.Ok)
            self.new_payment.show()
        # self.backupFile("C:/Users/ALEX/Desktop/slef_help/payment.csv","payment.csv")

    def viewAllPayments(self):
        self.all_payments.show()
        df = None
        if os.environ["DATA_ENGINE"] == "DATABASE_ENGINE":
            with self.con:
                cur = self.con.cursor()
                cur.execute("SELECT NAME, idNumber, paymentDate,amount,transactionCode, mode FROM payment")
                rows = list(list(x) for x in cur.fetchall())
            df = pd.DataFrame(rows,
                              columns=["NAME", "NATIONAL ID", "DATE", "AMOUNT", "TRANSACTION CODE", "PAYMENT MODE"])
        else:
            if os.path.exists(os.environ["MEMBERS_FILE"]):
                df = pd.read_csv(os.environ["PAYMENTS_FILE"],
                                 names=["NAME", "NATIONAL ID", "DATE", "AMOUNT", "TRANSACTION CODE", "PAYMENT MODE"])
        df.dropna(inplace=True)
        # df["NATIONAL ID"] = df["NATIONAL ID"].astype(int)
        df = df.reset_index()

        df = df.drop(['index'], axis=1)
        self.model2 = PandasModel.PandasModel(df)
        self.all_payments.ui.all_payments_view.setModel(self.model2)
        self.all_payments.ui.all_payments_view.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        # self.home_page.ui.members_list.resizeRowsToContents()
        self.all_payments.ui.all_payments_view.setSelectionBehavior(
            QTableView.SelectRows)
        self.all_payments.ui.all_payments_view.font().setPointSize(42);
        self.all_payments.ui.all_payments_view.setSortingEnabled(True)


app = QApplication([])
a = TheApp()
app.exec_()
