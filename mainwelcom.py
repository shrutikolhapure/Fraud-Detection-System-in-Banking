# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from MainLogin import Ui_LoginWindow
from registrationNew import Ui_registrationPage

import sys
import sqlite3
from config import DB_NAME   # ✅ use config


# =========================
# DATABASE INIT (CLEAN)
# =========================
def initialize_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''CREATE TABLE IF NOT EXISTS NEWBANK(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            FIRSTNAME TEXT NOT NULL,
            LASTNAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            PASSWORD BLOB NOT NULL,
            CONFIRM_PASSWORD BLOB NOT NULL,
            PHONE TEXT NOT NULL,
            SEX TEXT,
            ADDRESS TEXT,
            BAL REAL DEFAULT 0
        );''')
        conn.close()
    except Exception as e:
        print("DB Init Error:", e)


# =========================
# UI CLASS
# =========================
class Ui_Page(object):

    def setupUi(self, WelcomePage):
        self.window = WelcomePage
        WelcomePage.setObjectName("WelcomePage")
        WelcomePage.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(WelcomePage)
        self.centralwidget.setObjectName("centralwidget")

        # Background
        self.centralwidget.setStyleSheet("""
        QWidget#centralwidget {
            border-image: url(bank.jpg) 0 0 0 0 stretch stretch;
        }
        """)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Overlay
        self.overlay = QtWidgets.QWidget()
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        main_layout.addWidget(self.overlay)

        self.layout = QtWidgets.QVBoxLayout(self.overlay)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(30)

        # Title
        self.label = QtWidgets.QLabel("Welcome to BOI Bank Limited")
        self.label.setStyleSheet("font: bold 36pt 'Arial'; color: white;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Subtitle
        self.label2 = QtWidgets.QLabel("Do You Have An Existing Account?")
        self.label2.setStyleSheet("font: 24pt 'Arial'; color: white;")
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label2)

        # Button style
        button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            font: bold 16pt 'Arial';
            padding: 12px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #5dade2;
        }
        """

        # Buttons
        self.btn_yes = QtWidgets.QPushButton("YES")
        self.btn_no = QtWidgets.QPushButton("NO")
        self.btn_quit = QtWidgets.QPushButton("QUIT")

        for btn in [self.btn_yes, self.btn_no, self.btn_quit]:
            btn.setStyleSheet(button_style)
            btn.setMinimumSize(250, 60)
            self.layout.addWidget(btn, alignment=QtCore.Qt.AlignCenter)

        WelcomePage.setCentralWidget(self.centralwidget)

        # Connect buttons
        self.btn_yes.clicked.connect(self.open_login)
        self.btn_no.clicked.connect(self.open_register)
        self.btn_quit.clicked.connect(self.quit_app)

    # =========================
    # NAVIGATION
    # =========================
    def open_login(self):
        try:
            self.loginWindow = QtWidgets.QMainWindow()
            self.ui = Ui_LoginWindow()
            self.ui.beginLogin(self.loginWindow)
            self.loginWindow.showMaximized()
            self.window.close()
        except Exception as e:
            print("Login Error:", e)

    def open_register(self):
        try:
            self.regWindow = QtWidgets.QMainWindow()
            self.ui = Ui_registrationPage()
            self.ui.setupUi(self.regWindow)
            self.regWindow.showMaximized()
            self.window.close()
        except Exception as e:
            print("Register Error:", e)

    def quit_app(self):
        QtWidgets.QApplication.quit()


# =========================
# MAIN ENTRY
# =========================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    initialize_database()   # ✅ ensure DB exists

    window = QtWidgets.QMainWindow()
    ui = Ui_Page()
    ui.setupUi(window)

    window.showMaximized()
    sys.exit(app.exec_())