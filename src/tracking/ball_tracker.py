import numpy as np
from typing import List, Dict, Optional, Tuple
from filterpy.kalman import KalmanFilter

class BallTracker:
    """Specialized tracker for ball movement"""
    
    def __init__(
        self,
        max_lost_frames: int = 10,
        min_confidence: float = 0.3,
        max_acceleration: float = 50.0  # meters/s²
    ):
        """
        Initialize ball tracker
        
        Args:
            max_lost_frames: Maximum number of frames to keep predicting without detection
            min_confidence: Minimum confidence for ball detection
            max_acceleration: Maximum expected ball acceleration
        """
        self.max_lost_frames = max_lost_frames
        self.min_confidence = min_confidence
        self.max_acceleration = max_acceleration
        
        # Initialize Kalman filter for 3D tracking (x, y, z positions and velocities)
        self.kf = KalmanFilter(dim_x=9, dim_z=3)
        
        # State transition matrix (position, velocity, acceleration)
        dt = 1.0  # time step
        self.kf.F = np.array([
            [1, 0, 0, dt, 0, 0, 0.5*dt**2, 0, 0],
            [0, 1, 0, 0, dt, 0, 0, 0.5*dt**2, 0],
            [0, 0, 1, 0, 0, dt, 0, 0, 0.5*dt**2],
            [0, 0, 0, 1, 0, 0, dt, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, dt, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, dt],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        
        # Measurement matrix (we only measure position)
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0]
        ])
        
        # Initialize state covariance matrix
        self.kf.P *= 1000.
        
        # Initialize process noise
        self.kf.Q[6:, 6:] *= 0.01  # acceleration noise
        
        # Initialize measurement noise
        self.kf.R *= 1.0
        
        self.lost_frames = 0
        self.initialized = False
        
    def predict(self) -> Optional[np.ndarray]:
        """
        Predict ball position
        
        Returns:
            Predicted (x, y, z) position or None if track is lost
        """
        if not self.initialized:
            return None
            
        prediction = self.kf.predict()
        self.lost_frames += 1
        
        if self.lost_frames > self.max_lost_frames:
            self.initialized = False
            return None
            
        return prediction[:3]
        
    def update(self, detection: Optional[Dict]) -> Optional[np.ndarray]:
        """
        Update tracker with new detection
        
        Args:
            detection: Ball detection dictionary or None if no detection
            
        Returns:
            Updated ball position or None if track is lost
        """
        if detection is None:
            return self.predict()
            
        confidence = detection.get('confidence', 0.0)
        if confidence < self.min_confidence:
            return self.predict()
            
        bbox = detection['bbox']
        x = (bbox[0] + bbox[2]) / 2
        y = (bbox[1] + bbox[3]) / 2
        z = detection.get('z_position', 0.0)  # If available from 3D detection
        
        measurement = np.array([x, y, z])
        
        if not self.initialized:
            self.kf.x[:3] = measurement
            self.initialized = True
        else:
            self.kf.update(measurement)
            
        self.lost_frames = 0
        return self.kf.x[:3]
        
    def get_velocity(self) -> Optional[np.ndarray]:
        """Get current ball velocity"""
        if not self.initialized:
            return None
        return self.kf.x[3:6]
        
    def get_acceleration(self) -> Optional[np.ndarray]:
        """Get current ball acceleration"""
        if not self.initialized:
            return None
        return self.kf.x[6:9] 