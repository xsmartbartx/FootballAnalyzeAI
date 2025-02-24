import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from ..data.dataset_config import DatasetConfig
from ..data.annotation_handler import AnnotationHandler

class LabelingTool:
    def __init__(self, config: DatasetConfig, annotation_handler: AnnotationHandler):
        self.config = config
        self.annotation_handler = annotation_handler
        self.current_class = 0
        self.drawing = False
        self.start_point = None
        self.end_point = None
        
    def draw_bbox(self, event, x, y, flags, param):
        """Mouse callback function for drawing bounding boxes"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.end_point = (x, y)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_point = (x, y)
            
            # Add bbox to current image annotations
            if self.start_point and self.end_point:
                x1, y1 = min(self.start_point[0], self.end_point[0]), min(self.start_point[1], self.end_point[1])
                x2, y2 = max(self.start_point[0], self.end_point[0]), max(self.start_point[1], self.end_point[1])
                
                self.current_objects.append({
                    'class': self.config.classes[self.current_class],
                    'bbox': [x1, y1, x2, y2],
                    'confidence': 1.0
                })
    
    def label_image(self, image_path: Path) -> None:
        """Label a single image"""
        image = cv2.imread(str(image_path))
        window_name = 'Labeling Tool'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.draw_bbox)
        
        # Load existing annotations if any
        self.current_objects = self.annotation_handler.load_annotation(
            image_path.name
        ).get('objects', [])
        
        while True:
            img_copy = image.copy()
            
            # Draw existing boxes
            for obj in self.current_objects:
                bbox = obj['bbox']
                cv2.rectangle(img_copy, 
                            (bbox[0], bbox[1]), 
                            (bbox[2], bbox[3]),
                            (0, 255, 0), 2)
                cv2.putText(img_copy, 
                          obj['class'],
                          (bbox[0], bbox[1] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX,
                          0.5, (0, 255, 0), 2)
            
            # Draw current box
            if self.drawing and self.start_point and self.end_point:
                cv2.rectangle(img_copy,
                            self.start_point,
                            self.end_point,
                            (255, 0, 0), 2)
            
            # Show current class
            cv2.putText(img_copy,
                      f"Current class: {self.config.classes[self.current_class]}",
                      (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      1, (0, 0, 255), 2)
            
            cv2.imshow(window_name, img_copy)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit
                break
            elif key == ord('s'):  # Save
                self.annotation_handler.save_annotation(image_path.name, self.current_objects)
                print(f"Saved annotations for {image_path.name}")
            elif key == ord('c'):  # Change class
                self.current_class = (self.current_class + 1) % len(self.config.classes)
            elif key == ord('z'):  # Undo last bbox
                if self.current_objects:
                    self.current_objects.pop()
        
        cv2.destroyAllWindows() 