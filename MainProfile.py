# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem
import sqlite3
import bcrypt
from config import DB_NAME


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.resize(1000, 700)

        MainWindow.setStyleSheet("""
        QMainWindow {
            background-color: #eaf4ff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # ================= TITLE =================
        self.title = QtWidgets.QLabel("🏦 BOI Banking Dashboard")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 38px;
            font-weight: bold;
            color: #2c3e50;
        """)
        main_layout.addWidget(self.title)

        # ================= STATS =================
        self.statsLabel = QtWidgets.QLabel()
        self.statsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statsLabel.setStyleSheet("font-size:15px; color:#555;")
        main_layout.addWidget(self.statsLabel)

        self.load_stats()

        # ================= CARD =================
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(420)
        self.card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 18px;
            padding: 25px;
        }
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setYOffset(6)
        self.card.setGraphicsEffect(shadow)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(18)

        # ================= BUTTON STYLE =================
        button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            font-size: 15pt;
            padding: 12px;
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """

        self.btn_balance = QtWidgets.QPushButton("💰 Check Balance")
        self.btn_transfer = QtWidgets.QPushButton("🔁 Transfer")
        self.btn_deposit = QtWidgets.QPushButton("💵 Deposit")
        self.btn_history = QtWidgets.QPushButton("📜 History")
        self.btn_logout = QtWidgets.QPushButton("🚪 Logout")

        for btn in [
            self.btn_balance,
            self.btn_transfer,
            self.btn_deposit,
            self.btn_history,
            self.btn_logout
        ]:
            btn.setStyleSheet(button_style)
            btn.setMinimumHeight(50)
            card_layout.addWidget(btn)

        main_layout.addWidget(self.card)

        # ================= CONNECTIONS =================
        self.btn_balance.clicked.connect(self.CheckBal)
        self.btn_transfer.clicked.connect(self.Transfer)
        self.btn_deposit.clicked.connect(self.Deposit)
        self.btn_history.clicked.connect(self.TransactionHistory)
        self.btn_logout.clicked.connect(self.Logout)

    # ================= ANALYTICS =================
    def load_stats(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM NEWT")
        total = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM NEWT WHERE FRAUD_FLAG='YES'")
        fraud = cur.fetchone()[0]

        cur.execute("SELECT BAL FROM NEWBANK LIMIT 1")
        bal = cur.fetchone()
        balance = bal[0] if bal else 0

        conn.close()

        self.statsLabel.setText(
            f"💰 Balance: ₹{balance}   |   📊 Transactions: {total}   |   🚨 Fraud: {fraud}"
        )

    # ================= CHECK BALANCE =================
    def CheckBal(self):
        password, ok = QInputDialog.getText(
            self.mainwindow, "Check Balance", "Enter Password:", QtWidgets.QLineEdit.Password
        )

        if ok and password:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()

            cur.execute("SELECT PASSWORD, BAL FROM NEWBANK")
            users = cur.fetchall()

            for stored_password, balance in users:
                if bcrypt.checkpw(password.encode(), stored_password):
                    QMessageBox.information(
                        self.mainwindow, "Balance", f"₹{balance:.2f}"
                    )
                    conn.close()
                    return

            conn.close()
            QMessageBox.warning(self.mainwindow, "Error", "Invalid password")

    # ================= NAVIGATION =================
    def Transfer(self):
        from Transfer import Ui_TransferWindow
        self.transfer = QtWidgets.QMainWindow()
        self.ui = Ui_TransferWindow()
        self.ui.setupUi(self.transfer)
        self.transfer.show()

    def Deposit(self):
        from Deposit import Ui_DepositWindow
        self.deposit = QtWidgets.QMainWindow()
        self.ui = Ui_DepositWindow()
        self.ui.setupUi(self.deposit)
        self.deposit.show()

    # ================= TRANSACTION HISTORY =================
    def TransactionHistory(self):
        self.historyWindow = QtWidgets.QDialog(self.mainwindow)
        self.historyWindow.setWindowTitle("Transaction History")
        self.historyWindow.resize(1100, 600)

        layout = QtWidgets.QVBoxLayout(self.historyWindow)

        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("🔍 Search...")
        layout.addWidget(self.searchBox)

        self.filterBox = QtWidgets.QComboBox()
        self.filterBox.addItems(["All", "DEPOSIT", "TRANSFER"])
        layout.addWidget(self.filterBox)

        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        self.exportBtn = QtWidgets.QPushButton("📄 Export PDF")
        layout.addWidget(self.exportBtn)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM NEWT ORDER BY ID DESC")
        self.all_rows = cur.fetchall()
        conn.close()

        self.load_table(self.all_rows)

        self.searchBox.textChanged.connect(self.apply_filter)
        self.filterBox.currentTextChanged.connect(self.apply_filter)
        self.exportBtn.clicked.connect(self.export_pdf)

        self.historyWindow.exec_()

    # ================= LOAD TABLE =================
    def load_table(self, rows):
        if not rows:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No data found"))
            return

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))

        headers = [
            "ID","TXN_ID","SENDER","RECEIVER","TYPE","CATEGORY",
            "AMOUNT","S_OLD","S_NEW","R_OLD","R_NEW","DATE","STATUS","FRAUD"
        ]
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))

                if j == 13 and str(val).upper() == "YES":
                    item.setBackground(QtGui.QColor("red"))
                    item.setForeground(QtGui.QColor("white"))

                self.table.setItem(i, j, item)

    # ================= FILTER =================
    def apply_filter(self):
        keyword = self.searchBox.text().strip().lower()
        filter_type = self.filterBox.currentText().strip().lower()

        filtered = []

        for row in self.all_rows:
            sender = str(row[2]).lower()
            receiver = str(row[3]).lower()
            ttype = str(row[4]).strip().lower()

            if keyword in sender or keyword in receiver:
                if filter_type == "all" or ttype == filter_type:
                    filtered.append(row)

        self.load_table(filtered)

    # ================= PDF =================
    def export_pdf(self):
        from reportlab.platypus import SimpleDocTemplate, Table

        pdf = SimpleDocTemplate("statement.pdf")
        data = [list(row[:7]) for row in self.all_rows]

        table = Table(data)
        pdf.build([table])

        QMessageBox.information(self.mainwindow, "Done", "PDF Created")

    # ================= LOGOUT =================
    def Logout(self):
        self.mainwindow.close()