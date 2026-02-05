from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal
import cv2
import numpy as np

class CameraWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(640, 480)
        self.current_frame = None
        self.detections = []

    def update_frame(self, frame, detections=None):
        """
        Updates the displayed frame.
        frame: numpy array (BGR)
        detections: list of dicts {'box': [x1, y1, x2, y2], 'class': '500', 'conf': 0.95}
        """
        if frame is None:
            return
        
        self.current_frame = frame
        if detections:
            self.detections = detections
        else:
            self.detections = []

        # Draw detections on frame
        display_frame = frame.copy()
        
        # Convert BGR to RGB
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        # Draw boxes
        for det in self.detections:
            x1, y1, x2, y2 = det['box']
            label = f"{det['class']} (Conf: {det['conf']:.2f})"
            
            # Draw rectangle
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(display_frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert to QImage
        h, w, ch = display_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(display_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Display
        self.setPixmap(QPixmap.fromImage(qt_image))
