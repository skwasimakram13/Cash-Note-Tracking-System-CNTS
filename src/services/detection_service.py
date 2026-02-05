from src.core.config import Config
import os
import cv2

class DetectionService:
    def __init__(self):
        self.model = None
        self.yolo_available = False
        
        # Lazy import to prevent hangs/crashes at module level
        try:
            from ultralytics import YOLO
            self.yolo_available = True
        except ImportError as e:
            print(f"Warning: Could not import YOLO (Ultralytics). Detection will be disabled. Error: {e}")
        except Exception as e:
             # Catching OSError (DLL) or other init errors
            print(f"Warning: Error importing YOLO (Torch). Detection will be disabled. Error: {e}")

        if self.yolo_available:
            if os.path.exists(Config.MODEL_PATH):
                try:
                    self.model = YOLO(Config.MODEL_PATH)
                except Exception as e:
                    print(f"Failed to load YOLO model: {e}")
            else:
                print(f"YOLO Model not found at {Config.MODEL_PATH}. Detection will be disabled/simulated.")
        else:
             print("YOLO is unavailable in this environment.")

    def detect(self, frame):
        """
        Detects notes in the frame.
        Returns a list of detections: [{'box': [x1, y1, x2, y2], 'class': '500', 'conf': 0.95}, ...]
        """
        if not self.model:
            # Fallback / Simulation for testing UI if model fails
            # In a real app we might just return empty, but for demo let's return nothing or a mock if requested
            return []

        results = self.model(frame, verbose=False) # Run inference
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                conf = float(box.conf)
                if conf < Config.CONFIDENCE_THRESHOLD:
                    continue
                
                cls_id = int(box.cls)
                class_name = self.model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                detections.append({
                    'box': [x1, y1, x2, y2],
                    'class': class_name,
                    'conf': conf
                })
        
        return detections
