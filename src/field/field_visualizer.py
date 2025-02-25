import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from .field_detector import FieldLandmark

class FieldVisualizer:
    """Visualizes field view and player positions"""
    
    DEFAULT_COLOR_MAP = {
        'player': (0, 255, 0),    # Green
        'goalkeeper': (255, 0, 0), # Blue
        'referee': (0, 0, 255),    # Red
        'ball': (0, 255, 255)      # Yellow
    }
    
    @staticmethod
    def draw_field_landmarks(
        frame: np.ndarray,
        landmarks: List[FieldLandmark],
        color: Tuple[int, int, int] = (0, 255, 0)
    ) -> np.ndarray:
        """Draw detected field landmarks"""
        vis_frame = frame.copy()
        
        # Draw points
        for landmark in landmarks:
            x, y = landmark.image_point
            cv2.circle(vis_frame, (x, y), 5, color, -1)
            cv2.putText(
                vis_frame,
                landmark.name,
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )
        
        return vis_frame
    
    @staticmethod
    def draw_field_grid(
        field_view: np.ndarray,
        grid_size: float = 5.0,  # Grid size in meters
        color: Tuple[int, int, int] = (128, 128, 128)
    ) -> np.ndarray:
        """Draw grid on field view"""
        vis_field = field_view.copy()
        h, w = vis_field.shape[:2]
        
        # Draw vertical lines
        for x in np.arange(0, w, w * grid_size / 105.0):
            cv2.line(vis_field, (int(x), 0), (int(x), h), color, 1)
            
        # Draw horizontal lines
        for y in np.arange(0, h, h * grid_size / 68.0):
            cv2.line(vis_field, (0, int(y)), (w, int(y)), color, 1)
            
        return vis_field
    
    @staticmethod
    def draw_player_positions(
        field_view: np.ndarray,
        player_positions: List[Dict],
        color_map: Optional[Dict[str, Tuple[int, int, int]]] = None
    ) -> np.ndarray:
        """
        Draw player positions on field view
        
        Args:
            field_view: Input field view image
            player_positions: List of player position dictionaries
            color_map: Optional mapping of class names to BGR colors
        
        Returns:
            Field view with drawn player positions
        """
        if color_map is None:
            color_map = FieldVisualizer.DEFAULT_COLOR_MAP
            
        vis_field = field_view.copy()
        
        for player in player_positions:
            x, y = player['position']
            class_name = player['class']
            track_id = player.get('track_id', '')
            color = color_map.get(class_name, (255, 255, 255))
            
            # Draw player marker
            cv2.circle(vis_field, (int(x), int(y)), 10, color, -1)
            
            # Draw player ID
            if track_id:
                cv2.putText(
                    vis_field,
                    str(track_id),
                    (int(x) + 5, int(y) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1
                )
                
        return vis_field 