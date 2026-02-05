import cv2
import os
import time
from datetime import datetime

# Configuration
SAVE_DIR = "datasets/raw_images"
CLASS_NAME = "500_Note"

def create_dirs():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"Created directory: {SAVE_DIR}")

def capture_images():
    create_dirs()
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Try CAP_DSHOW for Windows if default fails
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
        
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("--- Data Collection Tool ---")
    print(f"Class: {CLASS_NAME}")
    print("Controls:")
    print("  [Space] - Save Image")
    print("  [Q]     - Quit")
    
    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame.")
            break

        # Display
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Saved: {count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Data Collector', display_frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == 32: # Space
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{CLASS_NAME}_{timestamp}_{count}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            cv2.imwrite(filepath, frame)
            count += 1
            print(f"Saved: {filepath}")
            # Visual feedback
            cv2.rectangle(display_frame, (0,0), (frame.shape[1], frame.shape[0]), (0, 255, 0), 10)
            cv2.imshow('Data Collector', display_frame)
            cv2.waitKey(100) # Pause briefly

    cap.release()
    cv2.destroyAllWindows()
    print(f"Collection finished. Total images saved: {count}")
    print(f"Location: {os.path.abspath(SAVE_DIR)}")

if __name__ == "__main__":
    capture_images()
