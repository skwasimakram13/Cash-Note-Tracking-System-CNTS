import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from src.core.config import Config

class CameraService(QThread):
    frame_received = pyqtSignal(object) # Emits numpy array

    def __init__(self):
        super().__init__()
        self._running = False
        self.camera_index = Config.CAMERA_INDEX

    def run(self):
        self._running = True
        cap = cv2.VideoCapture(self.camera_index)
        
        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)

        while self._running:
            ret, frame = cap.read()
            if ret:
                self.frame_received.emit(frame)
            else:
                # Handle camera disconnect or error?
                pass
        
        cap.release()

    def stop(self):
        self._running = False
        self.wait()
