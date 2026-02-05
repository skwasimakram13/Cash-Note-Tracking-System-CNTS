import pytesseract
import cv2
import re
from src.core.config import Config
import os

# Set tesseract cmd if on Windows, usually needed
if os.name == 'nt':
    if os.path.exists(Config.TESSERACT_CMD):
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD
    else:
        # Fallback or just warn
        print(f"Warning: Tesseract not found at {Config.TESSERACT_CMD}. OCR might fail if not in PATH.")

class OCRService:
    @staticmethod
    def extract_serial(image_roi):
        """
        Extracts serial number from the region of interest (ROI).
        """
        try:
            # Preprocessing
            gray = cv2.cvtColor(image_roi, cv2.COLOR_BGR2GRAY)
            
            # Adaptive thresholding to handle lighting variations
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 11, 2)
            
            # Simple denoise
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
            # OCR configuration
            # Assuming serial numbers are uppercase alphanumeric. 
            # Page segmentation mode 6 (Assume a single uniform block of text) works well for cropped serials.
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            
            text = pytesseract.image_to_string(denoised, config=custom_config)
            
            # Clean up text
            clean_text = re.sub(r'[^A-Z0-9]', '', text).strip()
            
            return clean_text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
