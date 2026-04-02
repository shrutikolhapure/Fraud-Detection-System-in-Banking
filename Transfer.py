# -*- coding: utf-8 -*-

import sys
import sqlite3
import random
import joblib
import logging
from datetime import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from MainProfile import Ui_MainWindow
from config import DB_NAME

from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE")
USER_PHONE_NUMBER = os.getenv("USER_PHONE")


class Ui_TransferWindow(object):

    def setupUi(self, TransferWindow):
        self.transfer = TransferWindow
        TransferWindow.setObjectName("TransferWindow")
        TransferWindow.resize(900, 600)

        TransferWindow.setStyleSheet("""
        QMainWindow {
            background-color: #d6ecff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(TransferWindow)
        TransferWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # =========================
        # CARD UI
        # =========================
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(400)
        self.card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
        }
        """)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # Title
        self.title = QtWidgets.QLabel("💸 Transfer Money")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        card_layout.addWidget(self.title)

        # Input Style
        input_style = """
        QLineEdit {
            padding: 10px;
            font-size: 14pt;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        """

        # Amount
        self.lineEdit_amount = QtWidgets.QLineEdit()
        self.lineEdit_amount.setPlaceholderText("Enter Amount")
        self.lineEdit_amount.setStyleSheet(input_style)
        card_layout.addWidget(self.lineEdit_amount)

        # Sender
        self.lineEdit_sender = QtWidgets.QLineEdit()
        self.lineEdit_sender.setPlaceholderText("Sender Username")
        self.lineEdit_sender.setStyleSheet(input_style)
        card_layout.addWidget(self.lineEdit_sender)

        # Receiver
        self.lineEdit_receiver = QtWidgets.QLineEdit()
        self.lineEdit_receiver.setPlaceholderText("Receiver Username")
        self.lineEdit_receiver.setStyleSheet(input_style)
        card_layout.addWidget(self.lineEdit_receiver)

        # Button Style
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

        # Transfer Button
        self.btn_transfer = QtWidgets.QPushButton("TRANSFER")
        self.btn_transfer.setStyleSheet(button_style)
        card_layout.addWidget(self.btn_transfer)

        # Cancel Button
        self.btn_cancel = QtWidgets.QPushButton("CANCEL")
        self.btn_cancel.setStyleSheet(button_style)
        card_layout.addWidget(self.btn_cancel)

        main_layout.addWidget(self.card)

        # Connect buttons
        self.btn_transfer.clicked.connect(self.SendTransfer)
        self.btn_cancel.clicked.connect(self.CancleTxf)

    # =========================
    # MESSAGE
    # =========================
    def message(self, title, msg):
        m = QMessageBox()
        m.setWindowTitle(title)
        m.setText(msg)
        m.exec_()

    # =========================
    # SMS
    # =========================
    def send_sms(self, text):
        try:
            from twilio.rest import Client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            client.messages.create(
                body=text,
                from_=TWILIO_PHONE_NUMBER,
                to=USER_PHONE_NUMBER
            )
        except Exception as e:
            logging.error(f"SMS Error: {e}")

    # =========================
    # FRAUD CHECK
    # =========================
    def check_fraud(self, data):
        try:
            model = joblib.load("ml/model.pkl")
            prediction = model.predict([data])[0]
            return prediction == 1
        except:
            return False

    # =========================
    # TRANSFER LOGIC
    # =========================
    def SendTransfer(self):

        sender = self.lineEdit_sender.text().strip()
        receiver = self.lineEdit_receiver.text().strip()
        amount_text = self.lineEdit_amount.text().strip()

        if not sender or not receiver or not amount_text:
            self.message("Error", "All fields required")
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

            if amount > 50000:
                self.message("Limit Error", "Max transfer is ₹50000")
                return

        except:
            self.message("Error", "Invalid amount")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        try:
            conn.execute("BEGIN")

            cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME=?", (sender,))
            s = cur.fetchone()

            if not s:
                self.message("Error", "Sender not found")
                return

            sender_bal = s[0] or 0

            if sender_bal < amount:
                self.message("Error", "Insufficient balance")
                return

            cur.execute("SELECT BAL FROM NEWBANK WHERE USERNAME=?", (receiver,))
            r = cur.fetchone()

            if not r:
                self.message("Error", "Receiver not found")
                return

            receiver_bal = r[0] or 0

            new_sender = sender_bal - amount
            new_receiver = receiver_bal + amount

            cur.execute("UPDATE NEWBANK SET BAL=? WHERE USERNAME=?", (new_sender, sender))
            cur.execute("UPDATE NEWBANK SET BAL=? WHERE USERNAME=?", (new_receiver, receiver))

            is_fraud = self.check_fraud([
                amount,
                sender_bal,
                new_sender,
                receiver_bal,
                new_receiver
            ])

            txn_id = "TXN" + str(random.randint(100000, 999999))
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            cur.execute("""
            INSERT INTO NEWT (
                TXN_ID, SENDER, RECEIVER, TTYPE, AMOUNT,
                SENDEROLDBAL, SENDERNEWBAL,
                RECOLDBAL, RECNEWBAL,
                DATE_TIME, STATUS, FRAUD_FLAG
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                txn_id,
                sender,
                receiver,
                "TRANSFER",
                amount,
                sender_bal,
                new_sender,
                receiver_bal,
                new_receiver,
                time,
                "SUCCESS",
                "YES" if is_fraud else "NO"
            ))

            conn.commit()

            # SMS
            if is_fraud:
                self.send_sms(f"⚠ Fraud Alert: ₹{amount}")
            else:
                self.send_sms(f"₹{amount} transferred successfully")

            self.message("Success", f"Transaction ID: {txn_id}")

            # Clear fields
            self.lineEdit_sender.clear()
            self.lineEdit_receiver.clear()
            self.lineEdit_amount.clear()

        except Exception as e:
            conn.rollback()
            logging.error(str(e))
            self.message("Error", "Transaction failed")

        finally:
            conn.close()

    # =========================
    # CANCEL
    # =========================
    def CancleTxf(self):
        self.transfer.close()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_TransferWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())