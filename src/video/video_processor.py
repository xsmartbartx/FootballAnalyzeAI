import cv2
import numpy as np
from pathlib import Path
from typing import Generator, Tuple, Optional
from datetime import datetime, timedelta

class VideoProcessor:
    def __init__(self, source: str):
        """
        Initialize video processor
        
        Args:
            source: Path to video file or camera index (0 for webcam)
        """
        self.source = source
        self.cap = None
        self.frame_count = 0
        self.fps = 0
        self.frame_size = (0, 0)
        
    def __enter__(self):
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        
    def start(self):
        """Start video capture"""
        self.cap = cv2.VideoCapture(self.source)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_size = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        
    def stop(self):
        """Release video capture"""
        if self.cap is not None:
            self.cap.release()
            
    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Get next frame from video"""
        if self.cap is None:
            return False, None
            
        ret, frame = self.cap.read()
        if ret:
            self.frame_count += 1
        return ret, frame
        
    def get_timestamp(self) -> datetime:
        """Get timestamp for current frame"""
        seconds = self.frame_count / self.fps
        return datetime.now() - timedelta(seconds=seconds) 