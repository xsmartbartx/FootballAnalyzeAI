import logging
import cv2
import numpy as np
from pathlib import Path
from typing import Optional
from models.detector import ObjectDetector
from video.video_processor import VideoProcessor
from video.visualizer import Visualizer
from tracking.sort_tracker import SORTTracker
from field.field_detector import FieldDetector
from field.field_visualizer import FieldVisualizer
from tracking.ball_tracker import BallTracker
from analytics.metrics_collector import MetricsCollector
from analytics.report_generator import MatchReport
import json
import os
from database.config import DatabaseConfig
from database.connection import DatabaseConnection
from database.analytics_repository import AnalyticsRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_detection(
    model_path: Path,
    video_source: str,
    match_id: str,
    output_path: Optional[Path] = None,
    show_display: bool = True
):
    """
    Run real-time object detection on video
    
    Args:
        model_path: Path to trained model weights
        video_source: Path to video file or camera index
        match_id: UUID of the match being analyzed
        output_path: Path to save output video (optional)
        show_display: Whether to show real-time display
    """
    try:
        # Initialize database connection
        db_config = DatabaseConfig(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'football_tracking'),
            username=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        db = DatabaseConnection(db_config)
        session = next(db.get_session())
        analytics_repo = AnalyticsRepository(session)
        
        # Initialize detector
        detector = ObjectDetector(model_path)
        
        # Initialize video writer if output path is provided
        writer = None
        
        # Initialize tracker
        tracker = SORTTracker()
        
        # Initialize field detector
        field_detector = FieldDetector()
        
        # Initialize ball tracker
        ball_tracker = BallTracker()
        
        # Initialize analytics
        metrics_collector = MetricsCollector()
        
        with VideoProcessor(video_source) as video:
            if output_path is not None:
                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Initialize video writer with proper codec
                fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
                writer = cv2.VideoWriter(
                    str(output_path),
                    fourcc,
                    video.fps,
                    video.frame_size
                )
                
                if not writer.isOpened():
                    logger.error("Failed to create video writer")
                    return
            
            logger.info("Starting video processing...")
            frame_count = 0
            
            while True:
                ret, frame = video.get_frame()
                if not ret or frame is None:
                    break
                
                try:
                    # Run detection
                    detections = detector.detect(frame)
                    
                    # Separate ball and player detections
                    ball_detection = None
                    player_detections = []
                    
                    for det in detections:
                        if det['class'] == 'ball':
                            ball_detection = det
                        else:
                            player_detections.append(det)
                    
                    # Update tracking
                    tracked_objects = tracker.update(player_detections)
                    ball_position = ball_tracker.update(ball_detection)
                    
                    # Update analytics
                    timestamp = video.get_timestamp()
                    
                    # Update player metrics
                    for obj in tracked_objects:
                        if obj['class'] in ['player', 'goalkeeper']:
                            metrics_collector.update_player_position(
                                str(obj['track_id']),
                                obj.get('team_id', 'unknown'),  # You'll need to add team detection
                                obj['position'],
                                timestamp
                            )
                    
                    # Update ball possession
                    if ball_position is not None:
                        metrics_collector.update_ball_possession(
                            (ball_position[0], ball_position[1]),
                            tracked_objects,
                            timestamp
                        )
                    
                    # Update team metrics
                    metrics_collector.update_team_metrics()
                    
                    # Generate field view
                    field_view = field_detector.warp_to_field_view(frame)
                    if field_view is not None:
                        # Convert tracked objects to field coordinates
                        player_positions = []
                        for obj in tracked_objects:
                            bbox = obj['bbox']
                            foot_point = (bbox[0] + bbox[2]) // 2, bbox[3]  # Bottom center of bbox
                            
                            # Transform to field coordinates
                            field_point = cv2.perspectiveTransform(
                                np.array([[foot_point]], dtype=np.float32),
                                field_detector.homography_matrix
                            )[0][0]
                            
                            player_positions.append({
                                **obj,
                                'position': (int(field_point[0]), int(field_point[1]))
                            })
                        
                        # Add ball position if available
                        if ball_position is not None:
                            field_point = cv2.perspectiveTransform(
                                np.array([[ball_position[:2]]], dtype=np.float32),
                                field_detector.homography_matrix
                            )[0][0]
                            
                            player_positions.append({
                                'class': 'ball',
                                'position': (int(field_point[0]), int(field_point[1])),
                                'z_position': ball_position[2]
                            })
                        
                        # Visualize field view
                        field_vis = FieldVisualizer.draw_field_grid(field_view)
                        field_vis = FieldVisualizer.draw_player_positions(field_vis, player_positions)
                        
                        if show_display:
                            cv2.imshow('Field View', field_vis)
                    
                    # Visualize results
                    vis_frame = Visualizer.draw_tracked_objects(frame, tracked_objects)
                    
                    # Write frame if output path is provided
                    if writer is not None:
                        writer.write(vis_frame)
                    
                    # Show frame if display is enabled
                    if show_display:
                        cv2.imshow('Detection', vis_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    
                    # Generate periodic reports
                    if frame_count % 300 == 0:  # Every 10 seconds at 30 fps
                        report = MatchReport(metrics_collector)
                        match_stats = report.generate_match_report()
                        
                        # Save report to database
                        analytics_repo.save_match_report(
                            match_id=match_id,
                            report_data=match_stats,
                            report_type='periodic'
                        )
                        
                        # Update player and team statistics
                        for player_id, player_stats in match_stats['players'].items():
                            analytics_repo.update_player_stats(
                                player_id=player_id,
                                match_id=match_id,
                                stats=player_stats
                            )
                        
                        for team_id, team_stats in match_stats['teams'].items():
                            analytics_repo.update_team_stats(
                                team_id=team_id,
                                match_id=match_id,
                                stats=team_stats
                            )
                        
                        # Save report to file system as backup
                        report_path = Path("output/reports")
                        report_path.mkdir(parents=True, exist_ok=True)
                        with open(report_path / f"report_{frame_count}.json", 'w') as f:
                            json.dump(match_stats, f, indent=2)
                    
                    frame_count += 1
                    if frame_count % 100 == 0:
                        logger.info(f"Processed {frame_count} frames")
                        
                except Exception as e:
                    logger.error(f"Error processing frame {frame_count}: {str(e)}")
                    continue
        
        logger.info(f"Completed processing {frame_count} frames")
        
        # Save final match report
        final_report = MatchReport(metrics_collector)
        final_stats = final_report.generate_match_report()
        analytics_repo.save_match_report(
            match_id=match_id,
            report_data=final_stats,
            report_type='final'
        )
        
    except Exception as e:
        logger.error(f"Error during video processing: {str(e)}")
        raise
        
    finally:
        # Close database session
        session.close()
        
        # Cleanup
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        # Configure paths
        model_path = Path("models/weights/best.pt")
        video_source = "path/to/your/video.mp4"  # or 0 for webcam
        output_path = Path("output/detection.mp4")
        match_id = "your-match-uuid"  # You'll need to provide this
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model weights not found at {model_path}")
        
        if isinstance(video_source, str) and not Path(video_source).exists():
            if video_source != "0":  # Allow webcam source
                raise FileNotFoundError(f"Video file not found at {video_source}")
        
        run_detection(model_path, video_source, match_id, output_path)
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}") 