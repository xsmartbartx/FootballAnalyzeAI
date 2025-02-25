import cv2
import numpy as np
from typing import List, Dict, Tuple

class Visualizer:
    """Handles visualization of detections on video frames"""
    
    @staticmethod
    def draw_detections(
        frame: np.ndarray,
        detections: List[Dict],
        color_map: Dict[str, Tuple[int, int, int]] = None
    ) -> np.ndarray:
        """
        Draw detection boxes and labels on frame
        
        Args:
            frame: Input frame
            detections: List of detection dictionaries
            color_map: Dictionary mapping class names to BGR colors
        
        Returns:
            Frame with drawn detections
        """
        if color_map is None:
            color_map = {
                'player': (0, 255, 0),    # Green
                'goalkeeper': (255, 0, 0), # Blue
                'referee': (0, 0, 255),    # Red
                'ball': (0, 255, 255)      # Yellow
            }
            
        vis_frame = frame.copy()
        
        for det in detections:
            bbox = det['bbox']
            class_name = det['class']
            conf = det['confidence']
            color = color_map.get(class_name, (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(
                vis_frame,
                (bbox[0], bbox[1]),
                (bbox[2], bbox[3]),
                color,
                2
            )
            
            # Draw label
            label = f"{class_name} {conf:.2f}"
            (label_w, label_h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                1
            )
            
            cv2.rectangle(
                vis_frame,
                (bbox[0], bbox[1] - label_h - 10),
                (bbox[0] + label_w, bbox[1]),
                color,
                -1
            )
            
            cv2.putText(
                vis_frame,
                label,
                (bbox[0], bbox[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            
        return vis_frame 

    @staticmethod
    def draw_tracked_objects(
        frame: np.ndarray,
        tracked_objects: List[Dict],
        color_map: Dict[str, Tuple[int, int, int]] = None
    ) -> np.ndarray:
        """
        Draw tracked objects with their IDs on frame
        
        Args:
            frame: Input frame
            tracked_objects: List of tracked object dictionaries
            color_map: Dictionary mapping class names to BGR colors
        
        Returns:
            Frame with drawn tracked objects
        """
        if color_map is None:
            color_map = {
                'player': (0, 255, 0),    # Green
                'goalkeeper': (255, 0, 0), # Blue
                'referee': (0, 0, 255),    # Red
                'ball': (0, 255, 255)      # Yellow
            }
            
        vis_frame = frame.copy()
        
        for obj in tracked_objects:
            bbox = obj['bbox']
            class_name = obj['class']
            track_id = obj['track_id']
            color = color_map.get(class_name, (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(
                vis_frame,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[2]), int(bbox[3])),
                color,
                2
            )
            
            # Draw label with track ID
            label = f"{class_name} #{track_id}"
            (label_w, label_h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                1
            )
            
            cv2.rectangle(
                vis_frame,
                (int(bbox[0]), int(bbox[1]) - label_h - 10),
                (int(bbox[0]) + label_w, int(bbox[1])),
                color,
                -1
            )
            
            cv2.putText(
                vis_frame,
                label,
                (int(bbox[0]), int(bbox[1]) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            
        return vis_frame 