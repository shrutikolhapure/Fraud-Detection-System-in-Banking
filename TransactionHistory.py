import sys
import sqlite3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from MainProfile import Ui_MainWindow


class Ui_HistoryWindow(object):
    def setupUi(self, HistoryWindow):
        self.historywindow = HistoryWindow
        HistoryWindow.setObjectName("HistoryWindow")
        HistoryWindow.resize(1200, 700)

        HistoryWindow.setStyleSheet("""
        QMainWindow {
            background-color: #d6ecff;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(HistoryWindow)
        HistoryWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # Title
        self.titleLabel = QtWidgets.QLabel("📜 Transaction History")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        """)
        main_layout.addWidget(self.titleLabel)

        # Table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels([
            "Sender",
            "Receiver",
            "Type",
            "Amount",
            "Sender Old Bal",
            "Sender New Bal",
            "Receiver Old Bal",
            "Receiver New Bal"
        ])

        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
                font-size: 11pt;
                gridline-color: #dcdcdc;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
        """)

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        main_layout.addWidget(self.tableWidget)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(20)

        btn_style = """
        QPushButton {
            background-color: white;
            border-radius: 12px;
            padding: 14px;
            font-size: 13pt;
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #dcdcdc;
        }
        QPushButton:hover {
            background-color: #3498db;
            color: white;
            border: none;
        }
        """

        self.pushButton_refresh = QtWidgets.QPushButton("🔄 Refresh")
        self.pushButton_refresh.setStyleSheet(btn_style)
        self.pushButton_refresh.setFixedHeight(50)

        self.pushButton_back = QtWidgets.QPushButton("↩ Back")
        self.pushButton_back.setStyleSheet(btn_style)
        self.pushButton_back.setFixedHeight(50)

        btn_layout.addWidget(self.pushButton_refresh)
        btn_layout.addWidget(self.pushButton_back)

        main_layout.addLayout(btn_layout)

        # Button actions
        self.pushButton_refresh.clicked.connect(self.load_history)
        self.pushButton_back.clicked.connect(self.go_back)

        # Load data automatically
        self.load_history()

    def load_history(self):
        try:
            conn = sqlite3.connect("BankNH.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM NEWT")
            rows = cur.fetchall()

            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            conn.close()

        except Exception as e:
            QMessageBox.warning(self.historywindow, "Error", f"Could not load transaction history:\n{str(e)}")

    def go_back(self):
        self.historywindow.close()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    HistoryWindow = QtWidgets.QMainWindow()
    ui = Ui_HistoryWindow()
    ui.setupUi(HistoryWindow)
    HistoryWindow.showMaximized()
    sys.exit(app.exec_())
