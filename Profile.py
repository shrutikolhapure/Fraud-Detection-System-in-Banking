from PyQt5 import QtWidgets, QtCore
import sqlite3
from config import DB_NAME


class ProfileWindow(QtWidgets.QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.setWindowTitle("👤 User Profile")
        self.resize(500, 400)

        self.setStyleSheet("background-color: #d6ecff;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # ================= CARD =================
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(350)
        self.card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
        }
        """)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("👤 Profile Details")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        card_layout.addWidget(title)

        # Labels
        self.label_username = QtWidgets.QLabel()
        self.label_name = QtWidgets.QLabel()
        self.label_email = QtWidgets.QLabel()
        self.label_phone = QtWidgets.QLabel()
        self.label_balance = QtWidgets.QLabel()

        for lbl in [
            self.label_username,
            self.label_name,
            self.label_email,
            self.label_phone,
            self.label_balance
        ]:
            lbl.setStyleSheet("font-size:14pt;")
            card_layout.addWidget(lbl)

        layout.addWidget(self.card)

        # Load user data
        self.load_user()

    # ================= LOAD DATA =================
    def load_user(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT * FROM NEWBANK WHERE USERNAME=?", (self.username,))
        user = cur.fetchone()
        conn.close()

        if user:
            self.label_username.setText(f"Username: {user[1]}")
            self.label_name.setText(f"Name: {user[2]} {user[3]}")
            self.label_email.setText(f"Email: {user[4]}")
            self.label_phone.setText(f"Phone: {user[6]}")
            self.label_balance.setText(f"Balance: ₹{user[8]}")
        else:
            self.label_username.setText("User not found")