import cv2
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class FieldLandmark:
    """Field landmark points for homography calculation"""
    name: str
    image_point: Tuple[int, int]  # Point in image coordinates
    field_point: Tuple[float, float]  # Point in field coordinates (meters)

class FieldDetector:
    """Detects soccer field and calculates homography matrix"""
    
    def __init__(self, field_width: float = 105.0, field_height: float = 68.0):
        """
        Initialize field detector
        
        Args:
            field_width: Width of field in meters
            field_height: Height of field in meters
        """
        self.field_width = field_width
        self.field_height = field_height
        self.homography_matrix = None
        
    def detect_field_lines(self, frame: np.ndarray) -> np.ndarray:
        """
        Detect field lines using image processing
        
        Args:
            frame: Input frame
            
        Returns:
            Binary mask of detected lines
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Apply morphological operations
        kernel = np.ones((3,3), np.uint8)
        lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return lines
        
    def detect_field_corners(self, frame: np.ndarray) -> List[FieldLandmark]:
        """
        Detect field corner points
        
        Args:
            frame: Input frame
            
        Returns:
            List of detected field landmarks
        """
        # Detect lines
        lines = self.detect_field_lines(frame)
        
        # Find corners using Harris corner detector
        corners = cv2.cornerHarris(lines.astype(np.float32), 2, 3, 0.04)
        corners = cv2.dilate(corners, None)
        
        # Get corner coordinates
        corner_points = np.where(corners > 0.01 * corners.max())
        corner_coords = list(zip(corner_points[1], corner_points[0]))  # x, y format
        
        # Filter and match corners to field landmarks
        landmarks = []
        field_corners = [
            ("top_left", (0, 0)),
            ("top_right", (self.field_width, 0)),
            ("bottom_left", (0, self.field_height)),
            ("bottom_right", (self.field_width, self.field_height))
        ]
        
        if len(corner_coords) >= 4:
            # Sort corners by position
            corner_coords.sort(key=lambda p: (p[1], p[0]))  # Sort by y, then x
            
            # Match corners to field positions
            for (name, field_point), image_point in zip(field_corners, corner_coords):
                landmarks.append(FieldLandmark(name, image_point, field_point))
        
        return landmarks
        
    def calculate_homography(self, landmarks: List[FieldLandmark]) -> Optional[np.ndarray]:
        """
        Calculate homography matrix from landmarks
        
        Args:
            landmarks: List of field landmarks
            
        Returns:
            3x3 homography matrix or None if calculation fails
        """
        if len(landmarks) < 4:
            return None
            
        # Extract point correspondences
        src_points = np.float32([lm.image_point for lm in landmarks])
        dst_points = np.float32([lm.field_point for lm in landmarks])
        
        # Calculate homography
        H, status = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)
        
        if status is not None and status.sum() >= 4:
            self.homography_matrix = H
            return H
        return None
        
    def warp_to_field_view(
        self,
        frame: np.ndarray,
        output_size: Tuple[int, int] = (800, 600)
    ) -> Optional[np.ndarray]:
        """
        Transform frame to top-down field view
        
        Args:
            frame: Input frame
            output_size: Size of output image (width, height)
            
        Returns:
            Warped image or None if transformation fails
        """
        if self.homography_matrix is None:
            landmarks = self.detect_field_corners(frame)
            if not self.calculate_homography(landmarks):
                return None
        
        # Apply perspective transformation
        warped = cv2.warpPerspective(
            frame,
            self.homography_matrix,
            output_size
        )
        
        return warped 