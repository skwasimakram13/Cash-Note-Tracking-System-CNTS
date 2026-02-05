from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox)
from PyQt6.QtCore import Qt
from src.database.sqlite_wrapper import db

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CNTS Login")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        
        self.operator_id = None
        self.operator_name = None
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Operator Login ID:"))
        self.txt_login = QLineEdit()
        self.txt_login.setPlaceholderText("Enter Login ID (e.g. admin)")
        layout.addWidget(self.txt_login)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.attempt_login)
        self.btn_login.setDefault(True) # Enter key triggers click
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)

    def attempt_login(self):
        login_id = self.txt_login.text().strip()
        
        if not login_id:
            QMessageBox.warning(self, "Error", "Please enter a login ID")
            return

        conn = db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM operators WHERE login_id = ?", (login_id,))
            row = cursor.fetchone()
            
            if row:
                self.operator_id = row[0]
                self.operator_name = row[1]
                self.accept() # Close dialog with QDialog.Accepted
            else:
                QMessageBox.warning(self, "Error", "Invalid Login ID")
        finally:
            conn.close()
