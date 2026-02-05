from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QMessageBox, QGroupBox, QGridLayout, QFormLayout)
from PyQt6.QtCore import pyqtSlot, Qt, QTimer
from PyQt6.QtGui import QFont

from src.ui.camera_widget import CameraWidget
from src.services.camera_service import CameraService
from src.services.detection_service import DetectionService
from src.services.ocr_service import OCRService
from src.services.transaction_service import TransactionService, TransactionType, NoteStatus
from src.database.sqlite_wrapper import db
print("MainWindow imports done.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cash Note Tracking System (CNTS)")
        self.setGeometry(100, 100, 1280, 720)
        self.operator_id = 1 # Default fallback

        # Services
        # DB is now handled by sqlite_wrapper internally
        self.db = None # Kept attribute for safety if other methods ref it (checked: they don't seem to)

        self.camera_service = CameraService()
        self.detection_service = DetectionService()
        self.transaction_service = TransactionService()
        
        # State
        self.is_scanning = False
        self.frame_count = 0
        self.SKIP_FRAMES = 5 # Run detection every 5th frame
        
        self.init_ui()
        
        # Connect Camera
        if self.camera_service:
            self.camera_service.frame_received.connect(self.process_frame)
            self.camera_service.start()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left Panel (Camera)
        left_layout = QVBoxLayout()
        self.camera_widget = CameraWidget()
        left_layout.addWidget(self.camera_widget)
        
        # Camera Controls
        cam_controls = QHBoxLayout()
        self.btn_cash_in = QPushButton("CASH IN")
        self.btn_cash_in.setCheckable(True)
        self.btn_cash_in.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_cash_in.clicked.connect(self.toggle_cash_in)
        
        self.btn_cash_out = QPushButton("CASH OUT")
        self.btn_cash_out.setCheckable(True)
        self.btn_cash_out.setStyleSheet("background-color: #F44336; color: white; padding: 10px; font-weight: bold;")
        self.btn_cash_out.clicked.connect(self.toggle_cash_out)
        
        cam_controls.addWidget(self.btn_cash_in)
        cam_controls.addWidget(self.btn_cash_out)
        left_layout.addLayout(cam_controls)
        
        main_layout.addLayout(left_layout, stretch=2)

        # Right Panel (Dashboard/Logs)
        right_layout = QVBoxLayout()
        
        # Stats Group
        stats_group = QGroupBox("Session Stats")
        stats_layout = QFormLayout() if 'QFormLayout' in locals() else QVBoxLayout() # Fallback
        self.lbl_count = QLabel("0")
        self.lbl_total = QLabel("₹0")
        
        # Just simple layout for stats
        stats_inner_layout = QGridLayout()
        stats_inner_layout.addWidget(QLabel("Notes Scanned:"), 0, 0)
        stats_inner_layout.addWidget(self.lbl_count, 0, 1)
        stats_inner_layout.addWidget(QLabel("Total Value:"), 1, 0)
        stats_inner_layout.addWidget(self.lbl_total, 1, 1)
        stats_group.setLayout(stats_inner_layout)
        
        right_layout.addWidget(stats_group)
        
        # Logs
        self.log_widget = QListWidget()
        right_layout.addWidget(QLabel("Transaction Log"))
        right_layout.addWidget(self.log_widget)
        
        # Commit Button
        self.btn_commit = QPushButton("COMMIT TRANSACTION")
        self.btn_commit.setEnabled(False)
        self.btn_commit.clicked.connect(self.commit_transaction)
        self.btn_commit.setStyleSheet("padding: 10px; font-size: 14px;")
        right_layout.addWidget(self.btn_commit)

        main_layout.addLayout(right_layout, stretch=1)

    @pyqtSlot(object)
    def process_frame(self, frame):
        self.frame_count += 1
        detections = []
        
        if self.is_scanning and (self.frame_count % self.SKIP_FRAMES == 0):
            detections = self.detection_service.detect(frame)
            
            # Process detections logic
            for det in detections:
                # If high confidence and in session
                if det['conf'] > 0.8:
                    x1, y1, x2, y2 = det['box']
                    # Crop logic for OCR (assuming serial is in a specific region, but for MVP we crop the whole note or assume detection is the note)
                    # Ideally, we need another detection for specific serial region or heuristics.
                    # For MVP, let's just assume we try to read text from the whole note box.
                    
                    note_roi = frame[y1:y2, x1:x2]
                    serial = OCRService.extract_serial(note_roi)
                    
                    if len(serial) > 5: # Basic length check
                        # Try to add to transaction
                        denom = int(det['class']) if det['class'].isdigit() else 500 # Default if model gives '500' string
                        
                        result = self.transaction_service.scan_note(serial, denom)
                        if result['success']:
                            self.log_message(f"SUCCESS: {serial} (₹{denom}) - {result['message']}")
                            self.update_stats()
                        elif "already scanned" not in result['message']: 
                            # Don't spam log with "already scanned"
                             pass # self.log_message(f"IGNORED: {result['message']}")

        self.camera_widget.update_frame(frame, detections)

    def toggle_cash_in(self):
        if self.btn_cash_in.isChecked():
            self.btn_cash_out.setChecked(False)
            self.start_session(TransactionType.IN)
            self.btn_cash_in.setText("STOP CASH IN")
        else:
            self.stop_session()
            self.btn_cash_in.setText("CASH IN")

    def toggle_cash_out(self):
        if self.btn_cash_out.isChecked():
            self.btn_cash_in.setChecked(False)
            self.start_session(TransactionType.OUT)
            self.btn_cash_out.setText("STOP CASH OUT")
        else:
            self.stop_session()
            self.btn_cash_out.setText("CASH OUT")

    def start_session(self, t_type):
        self.is_scanning = True
        if self.transaction_service:
            self.transaction_service.start_session(t_type)
        else:
             self.log_message("Transaction Service unavailable (Debug Mode)")

        self.btn_commit.setEnabled(True)
        self.log_widget.clear()
        # self.log_message(f"--- Session Started: {t_type.value} ---")
        self.log_message(f"--- Session Started ---")
        self.update_stats()

    def stop_session(self):
        self.is_scanning = False
        self.btn_commit.setEnabled(False)
        self.log_message("--- Session Stopped ---")

    def commit_transaction(self):
        try:
            summary = self.transaction_service.get_summary()
            if summary['count'] == 0:
                QMessageBox.warning(self, "Warning", "No notes scanned!")
                return
                
            self.transaction_service.commit_transaction(operator_id=self.operator_id)
            QMessageBox.information(self, "Success", "Transaction Saved!")
            
            # Reset UI
            self.stop_session()
            self.btn_cash_in.setChecked(False)
            self.btn_cash_out.setChecked(False)
            self.btn_cash_in.setText("CASH IN")
            self.btn_cash_out.setText("CASH OUT")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to commit: {str(e)}")

    def update_stats(self):
        if self.transaction_service:
            summary = self.transaction_service.get_summary()
            self.lbl_count.setText(str(summary['count']))
            self.lbl_total.setText(f"₹{summary['total']}")

    def log_message(self, msg):
        self.log_widget.addItem(msg)
        self.log_widget.scrollToBottom()

    def closeEvent(self, event):
        if self.camera_service:
            self.camera_service.stop()
        event.accept()
