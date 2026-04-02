# -*- coding: utf-8 -*-

import sqlite3
import bcrypt

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from MainProfile import Ui_MainWindow


class Ui_LoginWindow(object):

    def beginLogin(self, LoginWindow):
        self.login = LoginWindow
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(900, 600)

        # 🌈 Background Style
        LoginWindow.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #2c3e50,
                stop:1 #4ca1af
            );
        }
        """)

        self.centralwidget = QtWidgets.QWidget(LoginWindow)

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Card UI
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(400)
        self.card.setStyleSheet("""
        QFrame {
          background-color: rgba(255, 255, 255, 60);
          border-radius: 20px;
          border: 1px solid rgba(255,255,255,120);
        }
        """)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # Title
        self.title = QtWidgets.QLabel("LOGIN")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: black;
        """)
        card_layout.addWidget(self.title)

        # Username
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Enter Username")
        self.lineEdit.setStyleSheet("""
        QLineEdit {
            padding: 12px;
            border-radius: 10px;
            background: rgba(255,255,255,180);
            font-size: 14pt;
        }
        """)
        card_layout.addWidget(self.lineEdit)

        # Password
        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setPlaceholderText("Enter Password")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setStyleSheet("""
        QLineEdit {
            padding: 12px;
            border-radius: 10px;
            background: rgba(255,255,255,180);
            font-size: 14pt;
        }
        """)
        card_layout.addWidget(self.lineEdit_2)

        # Buttons
        button_style = """
        QPushButton {
            background-color: rgba(255,255,255,80);
            color: black;
            font-size: 14pt;
            padding: 12px;
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: rgba(255,255,255,120);
        }
        """

        self.pushButton_Login = QtWidgets.QPushButton("LOGIN")
        self.pushButton_Login.setStyleSheet(button_style)

        self.pushButton_Sign_up = QtWidgets.QPushButton("BACK TO SIGN-UP")
        self.pushButton_Sign_up.setStyleSheet(button_style)

        card_layout.addWidget(self.pushButton_Login)
        card_layout.addWidget(self.pushButton_Sign_up)

        main_layout.addWidget(self.card)
        LoginWindow.setCentralWidget(self.centralwidget)

        # Connect buttons
        self.pushButton_Login.clicked.connect(self.loginLogin)
        self.pushButton_Sign_up.clicked.connect(self.reg)

    # =========================
    # MESSAGE BOX
    # =========================
    def general_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    # =========================
    # OPEN DASHBOARD
    # =========================
    def profile(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()

    # =========================
    # LOGIN FUNCTION (FIXED)
    # =========================
    def loginLogin(self):

        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        # Validate input
        if not username or not password:
            self.general_message("Error", "Please enter username and password")
            return

        try:
            conn = sqlite3.connect('BankNH.db')
            cur = conn.cursor()

            # Get stored hashed password
            cur.execute("SELECT PASSWORD FROM NEWBANK WHERE USERNAME = ?", (username,))
            result = cur.fetchone()

            if result:
                stored_password = result[0]

                # Compare password using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    conn.close()
                    self.login.close()
                    self.profile()
                    return

            conn.close()
            self.general_message("Login Failed", "Invalid Username or Password")

        except Exception as e:
            print("Login Error:", e)
            self.general_message("Error", "Something went wrong")

    # =========================
    # GO TO REGISTRATION
    # =========================
    def reg(self):
        self.login.close()
        from registrationNew import Ui_registrationPage

        self.registrationPage = QtWidgets.QMainWindow()
        self.ui = Ui_registrationPage()
        self.ui.setupUi(self.registrationPage)
        self.registrationPage.showMaximized()


# =========================
# RUN FILE DIRECTLY
# =========================
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()

    ui = Ui_LoginWindow()
    ui.beginLogin(LoginWindow)

    LoginWindow.showMaximized()
    sys.exit(app.exec_())