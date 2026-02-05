import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(DATA_DIR, "cnts.db")
    DB_URL = f"sqlite:///{DB_PATH}"
    
    # Camera Settings
    CAMERA_INDEX = 0
    FRAME_WIDTH = 1920
    FRAME_HEIGHT = 1080
    
    # Detection Settings
    MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt") # Placeholder
    CONFIDENCE_THRESHOLD = 0.5
    
    # OCR Settings
    TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Typical Windows path
