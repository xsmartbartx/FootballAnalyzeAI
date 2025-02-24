import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

class AnnotationHandler:
    """Handles creation and storage of image annotations"""
    
    def __init__(self, annotation_dir: Path):
        self.annotation_dir = annotation_dir
        self.annotation_dir.mkdir(parents=True, exist_ok=True)
    
    def save_annotation(self, image_name: str, objects: List[Dict]) -> None:
        """
        Save annotation for an image
        
        Args:
            image_name: Name of the image file
            objects: List of detected objects with their coordinates and class
                    Format: [{'class': str, 'bbox': [x1, y1, x2, y2], 'confidence': float}]
        """
        annotation_path = self.annotation_dir / f"{image_name.split('.')[0]}.json"
        
        annotation_data = {
            'image_name': image_name,
            'objects': objects
        }
        
        with open(annotation_path, 'w') as f:
            json.dump(annotation_data, f, indent=4)
    
    def load_annotation(self, image_name: str) -> Dict:
        """Load annotation for an image if it exists"""
        annotation_path = self.annotation_dir / f"{image_name.split('.')[0]}.json"
        
        if annotation_path.exists():
            with open(annotation_path, 'r') as f:
                return json.load(f)
        return {'image_name': image_name, 'objects': []} 