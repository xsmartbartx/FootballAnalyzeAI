import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
from .dataset_config import DatasetConfig

class DatasetPreparation:
    def __init__(self, config: DatasetConfig):
        self.config = config
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories for dataset organization"""
        self.config.data_root.mkdir(parents=True, exist_ok=True)
        self.config.train_path.mkdir(parents=True, exist_ok=True)
        self.config.val_path.mkdir(parents=True, exist_ok=True)
    
    def process_video(self, video_path: Path, output_path: Path, 
                     frame_interval: int = 30) -> None:
        """
        Extract frames from video for dataset creation
        
        Args:
            video_path: Path to input video
            output_path: Path to save extracted frames
            frame_interval: Extract every nth frame
        """
        cap = cv2.VideoCapture(str(video_path))
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                # Resize frame to configured input size
                aspect_ratio = frame.shape[1] / frame.shape[0]
                new_width = self.config.input_size
                new_height = int(new_width / aspect_ratio)
                frame = cv2.resize(frame, (new_width, new_height))
                
                # Save frame
                frame_path = output_path / f"frame_{frame_count:06d}.jpg"
                cv2.imwrite(str(frame_path), frame)
            
            frame_count += 1
        
        cap.release() 