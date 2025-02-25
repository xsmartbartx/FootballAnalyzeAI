from pathlib import Path
import numpy as np
import torch
from ultralytics import YOLO
from typing import List, Dict, Tuple

class ObjectDetector:
    def __init__(self, model_path: Path):
        """
        Initialize object detector with trained model
        
        Args:
            model_path: Path to trained YOLOv8 model weights
        """
        self.model = YOLO(str(model_path))
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def detect(self, frame: np.ndarray, conf_threshold: float = 0.25) -> List[Dict]:
        """
        Detect objects in a single frame
        
        Args:
            frame: Input image as numpy array (BGR)
            conf_threshold: Confidence threshold for detections
            
        Returns:
            List of detections with class, confidence and coordinates
        """
        results = self.model(frame, conf=conf_threshold)[0]
        detections = []
        
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            
            detections.append({
                'class': class_name,
                'confidence': confidence,
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
            
        return detections 