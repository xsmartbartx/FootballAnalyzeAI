import numpy as np
from typing import List, Dict, Optional
from filterpy.kalman import KalmanFilter
from scipy.optimize import linear_sum_assignment

class Track:
    """Track class for a single object"""
    def __init__(self, bbox: np.ndarray, class_name: str, track_id: int):
        self.id = track_id
        self.bbox = bbox
        self.class_name = class_name
        self.hits = 1
        self.no_losses = 0
        self.prediction = None
        
        # Initialize Kalman filter
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ])
        
        # Initialize state
        self.kf.x[:4] = self._convert_bbox_to_z(bbox)
        self.kf.P[4:, 4:] *= 1000.
        self.kf.P *= 10.
        self.kf.Q[4:, 4:] *= 0.01
        
    def _convert_bbox_to_z(self, bbox: np.ndarray) -> np.ndarray:
        """Convert bounding box to measurement vector"""
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = bbox[0] + w/2.
        y = bbox[1] + h/2.
        return np.array([x, y, w, h]).reshape((4, 1))
        
    def _convert_x_to_bbox(self, x: np.ndarray) -> np.ndarray:
        """Convert state vector to bounding box"""
        w = x[2]
        h = x[3]
        x_center = x[0]
        y_center = x[1]
        return np.array([
            x_center - w/2.,
            y_center - h/2.,
            x_center + w/2.,
            y_center + h/2.
        ]).reshape((4,))
        
    def predict(self) -> np.ndarray:
        """Predict next state"""
        if self.kf.x[6] + self.kf.x[2] <= 0:
            self.kf.x[6] *= 0.0
            
        self.prediction = self.kf.predict()
        return self._convert_x_to_bbox(self.prediction[:4])
        
    def update(self, bbox: np.ndarray) -> None:
        """Update state with new measurement"""
        self.hits += 1
        self.no_losses = 0
        self.kf.update(self._convert_bbox_to_z(bbox))

class SORTTracker:
    """SORT (Simple Online and Realtime Tracking) implementation"""
    
    def __init__(
        self,
        max_age: int = 1,
        min_hits: int = 3,
        iou_threshold: float = 0.3
    ):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.tracks: List[Track] = []
        self.frame_count = 0
        self.track_id_count = 0
        
    def _calculate_iou(self, bbox1: np.ndarray, bbox2: np.ndarray) -> float:
        """Calculate Intersection over Union between two boxes"""
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])
        
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        area2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
        
    def update(self, detections: List[Dict]) -> List[Dict]:
        """Update tracks with new detections"""
        self.frame_count += 1
        
        # Convert detections to numpy array
        if not detections:
            return []
            
        detection_bboxes = np.array([d['bbox'] for d in detections])
        detection_classes = [d['class'] for d in detections]
        
        # Get predictions from existing tracks
        track_predictions = []
        for track in self.tracks:
            track_predictions.append(track.predict())
        
        if not track_predictions:
            # No existing tracks, create new ones for all detections
            for bbox, class_name in zip(detection_bboxes, detection_classes):
                self.tracks.append(Track(bbox, class_name, self.track_id_count))
                self.track_id_count += 1
            return detections
            
        track_predictions = np.array(track_predictions)
        
        # Calculate IoU between predictions and detections
        iou_matrix = np.zeros((len(track_predictions), len(detection_bboxes)))
        for i, track_pred in enumerate(track_predictions):
            for j, det_bbox in enumerate(detection_bboxes):
                iou_matrix[i, j] = self._calculate_iou(track_pred, det_bbox)
        
        # Hungarian algorithm for matching
        matched_indices = linear_sum_assignment(-iou_matrix)
        matched_indices = np.asarray(matched_indices).T
        
        unmatched_detections = []
        for d in range(len(detection_bboxes)):
            if d not in matched_indices[:, 1]:
                unmatched_detections.append(d)
                
        unmatched_tracks = []
        for t in range(len(self.tracks)):
            if t not in matched_indices[:, 0]:
                unmatched_tracks.append(t)
        
        # Filter out matched with low IoU
        matches = []
        for m in matched_indices:
            if iou_matrix[m[0], m[1]] < self.iou_threshold:
                unmatched_detections.append(m[1])
                unmatched_tracks.append(m[0])
            else:
                matches.append(m)
        
        # Update matched tracks
        for track_idx, det_idx in matches:
            self.tracks[track_idx].update(detection_bboxes[det_idx])
        
        # Create new tracks for unmatched detections
        for det_idx in unmatched_detections:
            self.tracks.append(
                Track(
                    detection_bboxes[det_idx],
                    detection_classes[det_idx],
                    self.track_id_count
                )
            )
            self.track_id_count += 1
        
        # Update track states and remove dead tracks
        ret = []
        i = len(self.tracks)
        for track in reversed(self.tracks):
            if track.no_losses > self.max_age:
                self.tracks.pop(i-1)
            elif track.hits >= self.min_hits:
                bbox = track.prediction[:4]
                ret.append({
                    'track_id': track.id,
                    'class': track.class_name,
                    'bbox': bbox.tolist(),
                    'confidence': detections[0].get('confidence', 1.0)  # Use first detection's confidence
                })
            i -= 1
            
        return ret 