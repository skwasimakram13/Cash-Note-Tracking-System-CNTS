import sys
print("Starting imports...")

try:
    import cv2
    print("OpenCV imported successfully")
except Exception as e:
    print(f"OpenCV failed: {e}")

try:
    import torch
    print("PyTorch imported successfully")
except Exception as e:
    print(f"PyTorch failed: {e}")

try:
    from PyQt6.QtWidgets import QApplication
    print("PyQt6 imported successfully")
except Exception as e:
    print(f"PyQt6 failed: {e}")

try:
    from ultralytics import YOLO
    print("Ultralytics imported successfully")
except Exception as e:
    print(f"Ultralytics failed: {e}")

print("Imports done.")
