# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import sqlite3
import random
from MainLogin import Ui_LoginWindow
import bcrypt
from PyQt5.QtWidgets import QMessageBox

dbb = sqlite3.connect('BankNH.db')
c = dbb.cursor()


class Ui_registrationPage(object):
    def setupUi(self, registrationPage):
        self.register = registrationPage
        registrationPage.setObjectName("registrationPage")
        registrationPage.resize(900, 700)

        # 🎨 Background
        registrationPage.setStyleSheet("""
        QMainWindow {
            background-color: #d6ecff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(registrationPage)
        self.centralwidget.setObjectName("centralwidget")

        # 📦 Main Layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 🧊 Card
        card = QtWidgets.QFrame()
        card.setMaximumWidth(700)
        card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 20px;
        }
        """)

        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(35, 35, 35, 35)

        # 📝 Title
        self.label_10 = QtWidgets.QLabel("📝 Create Account")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        """)
        card_layout.addWidget(self.label_10)

        # 🎨 Input Style
        input_style = """
        QLineEdit {
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            font-size: 12pt;
            background-color: white;
        }
        QLineEdit:focus {
            border: 2px solid #3498db;
        }
        """

        label_style = """
        QLabel {
            font-size: 11pt;
            font-weight: bold;
            color: #2c3e50;
        }
        """

        combo_style = """
        QComboBox {
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            font-size: 12pt;
            background-color: white;
        }
        QComboBox:focus {
            border: 2px solid #3498db;
        }
        """

        button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border-radius: 12px;
            padding: 12px;
            font-size: 13pt;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """

        # 📋 Form Layout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)

        # Username
        self.label_username = QtWidgets.QLabel("Username")
        self.label_username.setStyleSheet(label_style)
        self.lineEdit_Username = QtWidgets.QLineEdit()
        self.lineEdit_Username.setPlaceholderText("Enter username")
        self.lineEdit_Username.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_username, self.lineEdit_Username)

        # First Name
        self.label_fname = QtWidgets.QLabel("First Name")
        self.label_fname.setStyleSheet(label_style)
        self.lineEdit_Firstname = QtWidgets.QLineEdit()
        self.lineEdit_Firstname.setPlaceholderText("Enter first name")
        self.lineEdit_Firstname.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_fname, self.lineEdit_Firstname)

        # Last Name
        self.label_Lname = QtWidgets.QLabel("Last Name")
        self.label_Lname.setStyleSheet(label_style)
        self.lineEdit_Lastname = QtWidgets.QLineEdit()
        self.lineEdit_Lastname.setPlaceholderText("Enter last name")
        self.lineEdit_Lastname.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_Lname, self.lineEdit_Lastname)

        # Email
        self.label_email = QtWidgets.QLabel("Email")
        self.label_email.setStyleSheet(label_style)
        self.lineEdit_email = QtWidgets.QLineEdit()
        self.lineEdit_email.setPlaceholderText("Enter email")
        self.lineEdit_email.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_email, self.lineEdit_email)

        # Password
        self.label_password = QtWidgets.QLabel("Password")
        self.label_password.setStyleSheet(label_style)
        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setPlaceholderText("Enter password")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_password, self.lineEdit_password)

        # Confirm Password
        self.label_password_confirm = QtWidgets.QLabel("Confirm Password")
        self.label_password_confirm.setStyleSheet(label_style)
        self.lineEdit_confirmPassword = QtWidgets.QLineEdit()
        self.lineEdit_confirmPassword.setPlaceholderText("Confirm password")
        self.lineEdit_confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirmPassword.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_password_confirm, self.lineEdit_confirmPassword)

        # Phone
        self.label_phone = QtWidgets.QLabel("Phone")
        self.label_phone.setStyleSheet(label_style)
        self.lineEdit_phone = QtWidgets.QLineEdit()
        self.lineEdit_phone.setPlaceholderText("Enter phone number")
        self.lineEdit_phone.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_phone, self.lineEdit_phone)

        # Gender
        self.label_sex = QtWidgets.QLabel("Gender")
        self.label_sex.setStyleSheet(label_style)
        self.comboBox_sex = QtWidgets.QComboBox()
        self.comboBox_sex.addItems(["Male", "Female", "Other"])
        self.comboBox_sex.setStyleSheet(combo_style)
        self.formLayout.addRow(self.label_sex, self.comboBox_sex)

        # Address
        self.label_address = QtWidgets.QLabel("Address")
        self.label_address.setStyleSheet(label_style)
        self.lineEdit_address = QtWidgets.QLineEdit()
        self.lineEdit_address.setPlaceholderText("Enter address")
        self.lineEdit_address.setStyleSheet(input_style)
        self.formLayout.addRow(self.label_address, self.lineEdit_address)

        card_layout.addLayout(self.formLayout)

        # Buttons
        self.pushButton_Register = QtWidgets.QPushButton("REGISTER")
        self.pushButton_Register.setStyleSheet(button_style)
        card_layout.addWidget(self.pushButton_Register)

        self.pushButton_reglogin = QtWidgets.QPushButton("LOGIN")
        self.pushButton_reglogin.setStyleSheet(button_style)
        card_layout.addWidget(self.pushButton_reglogin)

        main_layout.addWidget(card)

        registrationPage.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(registrationPage)
        self.statusbar.setObjectName("statusbar")
        registrationPage.setStatusBar(self.statusbar)

        # Connect Buttons
        self.pushButton_Register.clicked.connect(self.CreateDB)
        self.pushButton_reglogin.clicked.connect(self.login)

    # =========================
    # GENERAL MESSAGE
    # =========================
    def general_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    # =========================
    # GENERATE UNIQUE ACCOUNT NUMBER
    # =========================
    def generate_account_number(self):
        while True:
            account_no = str(random.randint(100000000000, 999999999999))
            c.execute("SELECT * FROM NEWBANK WHERE ACCOUNT_NO = ?", (account_no,))
            existing = c.fetchone()
            if not existing:
                return account_no

    # =========================
    # CREATE TABLE
    # =========================
    def CreateDB(self):
        c.execute('''
        CREATE TABLE IF NOT EXISTS NEWBANK(
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           USERNAME TEXT NOT NULL UNIQUE,
           FIRSTNAME TEXT NOT NULL,
           LASTNAME TEXT NOT NULL,
           EMAIL TEXT NOT NULL,
           PASSWORD TEXT NOT NULL,
           CONFIRM TEXT NOT NULL,
           PHONE TEXT NOT NULL,
           SEX TEXT,
           ADDRESS TEXT NOT NULL,
           BAL REAL DEFAULT 0,
           ACCOUNT_NO TEXT UNIQUE
        );
        ''')
        dbb.commit()
        self.insertdb()

    # =========================
    # INSERT USER DATA
    # =========================
    def insertdb(self):
        username = self.lineEdit_Username.text().strip()
        firstname = self.lineEdit_Firstname.text().strip()
        lastname = self.lineEdit_Lastname.text().strip()
        email = self.lineEdit_email.text().strip()
        password = self.lineEdit_password.text().strip()
        confirmPass = self.lineEdit_confirmPassword.text().strip()
        phone = self.lineEdit_phone.text().strip()
        sex = self.comboBox_sex.currentText()
        address = self.lineEdit_address.text().strip()

        # Validation
        if not username or not firstname or not lastname or not email or not password or not confirmPass or not phone or not address:
            self.general_message("Missing Fields", "Please fill all fields.")
            return

        if '@' not in email:
            self.general_message('Invalid Email', 'Please check your email again.')
            return

        if password != confirmPass:
            self.general_message('Password Error', 'Passwords do not match.')
            return
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if len(phone) != 10 or not phone.isdigit():
            self.general_message('Invalid Number', 'Please enter a valid 10-digit phone number.')
            return

        # Check duplicate username
        c.execute("SELECT * FROM NEWBANK WHERE USERNAME = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            self.general_message("Username Exists", "This username already exists. Please choose another one.")
            return

        # Generate account number
        account_no = self.generate_account_number()

        # Insert data
        c.execute("""
        INSERT INTO NEWBANK(
            USERNAME, FIRSTNAME, LASTNAME, EMAIL,
            PASSWORD, CONFIRM_PASSWORD, PHONE, SEX, ADDRESS,
            BAL, ACCOUNT_NO
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,(
            username,
            firstname,
            lastname,
            email,
            hashed_password,
            hashed_password,
            phone,
            sex,
            address,
            1000.0,
            account_no
        ))

        dbb.commit()

        self.general_message(
            "Success",
            f"Registration successful!\n\nYour Account Number is:\n{account_no}"
        )

        # Clear fields
        self.lineEdit_Username.clear()
        self.lineEdit_Firstname.clear()
        self.lineEdit_Lastname.clear()
        self.lineEdit_email.clear()
        self.lineEdit_password.clear()
        self.lineEdit_confirmPassword.clear()
        self.lineEdit_phone.clear()
        self.lineEdit_address.clear()
        self.comboBox_sex.setCurrentIndex(0)

        self.login()

    # =========================
    # GO TO LOGIN
    # =========================
    def login(self):
        self.register.close()
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_LoginWindow()
        self.ui.beginLogin(self.LoginWindow)
        self.LoginWindow.showMaximized()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    registrationPage = QtWidgets.QMainWindow()
    ui = Ui_registrationPage()
    ui.setupUi(registrationPage)
    registrationPage.showMaximized()
    sys.exit(app.exec_())
