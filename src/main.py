import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Pre-import SQLAlchemy to prevent DLL conflicts with PyQt6
try:
    import sqlalchemy.orm
except ImportError:
    pass

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 1. Show Login
    login = LoginWindow()
    if login.exec() == 1: # QDialog.Accepted
        print(f"Login successful: Operator {login.operator_name}")
        
        # 2. Show Main Window
        try:
            window = MainWindow()
            # Pass operator info if needed, or store in global context
            window.setWindowTitle(f"CNTS - Operator: {login.operator_name}")
            window.operator_id = login.operator_id
            window.show()
        except Exception as e:
            print(f"Error creating MainWindow: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
        sys.exit(app.exec())
    else:
        print("Login cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    print("Starting main module...")
    main()
