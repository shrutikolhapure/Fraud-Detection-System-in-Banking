# -*- coding: utf-8 -*-

import sys
import sqlite3
import random
import logging
from datetime import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from MainProfile import Ui_MainWindow
from config import DB_NAME


class Ui_DepositWindow(object):

    def setupUi(self, DepositWindow):
        self.depositWindow = DepositWindow
        DepositWindow.setObjectName("DepositWindow")
        DepositWindow.resize(900, 600)

        DepositWindow.setStyleSheet("""
        QMainWindow {
            background-color: #d6ecff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(DepositWindow)
        DepositWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # =========================
        # CARD UI
        # =========================
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(420)
        self.card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
        }
        """)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # =========================
        # TITLE
        # =========================
        self.titleLabel = QtWidgets.QLabel("💰 Deposit Money")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        card_layout.addWidget(self.titleLabel)

        self.subtitleLabel = QtWidgets.QLabel("Add money to your account securely")
        self.subtitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitleLabel.setStyleSheet("font-size: 13px; color: gray;")
        card_layout.addWidget(self.subtitleLabel)

        # =========================
        # INPUT STYLE
        # =========================
        input_style = """
        QLineEdit {
            padding: 10px;
            font-size: 14pt;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        QComboBox {
            padding: 8px;
            font-size: 12pt;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        """

        # Username
        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setPlaceholderText("Enter Username")
        self.lineEdit_username.setStyleSheet(input_style)
        card_layout.addWidget(self.lineEdit_username)

        # Amount
        self.lineEdit_amount = QtWidgets.QLineEdit()
        self.lineEdit_amount.setPlaceholderText("Enter Amount")
        self.lineEdit_amount.setStyleSheet(input_style)
        card_layout.addWidget(self.lineEdit_amount)

        # Category
        self.comboBox_category = QtWidgets.QComboBox()
        self.comboBox_category.addItems([
            "Choose Category",
            "Cash Deposit",
            "Salary",
            "Cheque",
            "UPI",
            "Other"
        ])
        self.comboBox_category.setStyleSheet(input_style)
        card_layout.addWidget(self.comboBox_category)

        # =========================
        # BUTTON STYLE
        # =========================
        button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            font-size: 14pt;
            padding: 10px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """

        # Deposit button
        self.pushButton_deposit = QtWidgets.QPushButton("DEPOSIT")
        self.pushButton_deposit.setStyleSheet(button_style)
        card_layout.addWidget(self.pushButton_deposit)

        # Cancel button
        self.pushButton_cancel = QtWidgets.QPushButton("CANCEL")
        self.pushButton_cancel.setStyleSheet(button_style)
        card_layout.addWidget(self.pushButton_cancel)

        main_layout.addWidget(self.card)

        # =========================
        # CONNECT
        # =========================
        self.pushButton_deposit.clicked.connect(self.DepositMoney)
        self.pushButton_cancel.clicked.connect(self.CancelDeposit)

    # =========================
    # MESSAGE BOX
    # =========================
    def message(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    # =========================
    # CREATE TABLE
    # =========================
    def create_transaction_table(self, cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS NEWT (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TXN_ID TEXT,
            SENDER TEXT,
            RECEIVER TEXT,
            TTYPE TEXT,
            CATEGORY TEXT,
            AMOUNT REAL,
            SENDEROLDBAL REAL,
            SENDERNEWBAL REAL,
            RECOLDBAL REAL,
            RECNEWBAL REAL,
            DATE_TIME TEXT,
            STATUS TEXT,
            FRAUD_FLAG TEXT
        )
        """)

    # =========================
    # DEPOSIT LOGIC
    # =========================
    def DepositMoney(self):

        username = self.lineEdit_username.text().strip()
        amount_text = self.lineEdit_amount.text().strip()
        category = self.comboBox_category.currentText()

        if not username or not amount_text:
            self.message("Error", "Please fill all fields")
            return

        if category == "Choose Category":
            self.message("Error", "Select category")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError

            if amount > 100000:
                self.message("Limit Error", "Max deposit is ₹100000")
                return

        except:
            self.message("Error", "Invalid amount")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            self.create_transaction_table(cur)

            cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME=?", (username,))
            user = cur.fetchone()

            if not user:
                self.message("Error", "User not found")
                return

            old_balance = user[0] or 0
            new_balance = old_balance + amount

            cur.execute("UPDATE NEWBANK SET BAL=? WHERE USERNAME=?",
                        (new_balance, username))

            txn_id = "DEP" + str(random.randint(100000, 999999))
            date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            cur.execute("""
            INSERT INTO NEWT (
                TXN_ID, SENDER, RECEIVER, TTYPE, CATEGORY, AMOUNT,
                SENDEROLDBAL, SENDERNEWBAL,
                RECOLDBAL, RECNEWBAL,
                DATE_TIME, STATUS, FRAUD_FLAG
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                txn_id,
                username,
                username,
                "DEPOSIT",
                category,
                amount,
                old_balance,
                new_balance,
                old_balance,
                new_balance,
                date_time,
                "SUCCESS",
                "NO"
            ))

            conn.commit()
            conn.close()

            self.message(
                "Success",
                f"₹{amount} deposited successfully\nNew Balance: ₹{new_balance}"
            )

            # Clear fields
            self.lineEdit_username.clear()
            self.lineEdit_amount.clear()
            self.comboBox_category.setCurrentIndex(0)

        except Exception as e:
            logging.error(str(e))
            self.message("Error", "Transaction failed")

    # =========================
    # CANCEL
    # =========================
    def CancelDeposit(self):
        self.depositWindow.close()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_DepositWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())