from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .models import AnalyticsReport, Match, Player, Team, PlayerTrackingData, BallTrackingData
import json
import numpy as np

class AnalyticsRepository:
    """Repository for managing analytics data in the database"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save_match_report(
        self,
        match_id: str,
        report_data: Dict,
        report_type: str = 'full_match'
    ) -> AnalyticsReport:
        """
        Save match analytics report to database
        
        Args:
            match_id: UUID of the match
            report_data: Report data as dictionary
            report_type: Type of report (e.g., 'full_match', 'player_stats', etc.)
            
        Returns:
            Created AnalyticsReport instance
        """
        report = AnalyticsReport(
            match_id=match_id,
            report_type=report_type,
            data=report_data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.session.add(report)
        self.session.commit()
        return report
    
    def update_player_stats(
        self,
        player_id: str,
        match_id: str,
        stats: Dict
    ) -> None:
        """
        Update player statistics in the database
        
        Args:
            player_id: UUID of the player
            match_id: UUID of the match
            stats: Player statistics dictionary
        """
        player = self.session.query(Player).filter_by(id=player_id).first()
        if not player:
            return
            
        # Update player statistics
        player.stats = {
            **(player.stats or {}),
            match_id: stats
        }
        
        self.session.commit()
    
    def update_team_stats(
        self,
        team_id: str,
        match_id: str,
        stats: Dict
    ) -> None:
        """
        Update team statistics in the database
        
        Args:
            team_id: UUID of the team
            match_id: UUID of the match
            stats: Team statistics dictionary
        """
        team = self.session.query(Team).filter_by(id=team_id).first()
        if not team:
            return
            
        # Update team statistics
        team.stats = {
            **(team.stats or {}),
            match_id: stats
        }
        
        self.session.commit()
    
    def get_match_reports(
        self,
        match_id: str,
        report_type: Optional[str] = None,
        limit: int = 10
    ) -> List[AnalyticsReport]:
        """
        Get analytics reports for a match
        
        Args:
            match_id: UUID of the match
            report_type: Optional type of report to filter
            limit: Maximum number of reports to return
            
        Returns:
            List of AnalyticsReport instances
        """
        query = self.session.query(AnalyticsReport).filter_by(match_id=match_id)
        
        if report_type:
            query = query.filter_by(report_type=report_type)
            
        return query.order_by(desc(AnalyticsReport.created_at)).limit(limit).all()
    
    def get_player_match_stats(
        self,
        player_id: str,
        match_id: str
    ) -> Optional[Dict]:
        """Get player statistics for a specific match"""
        player = self.session.query(Player).filter_by(id=player_id).first()
        if not player or not player.stats:
            return None
            
        return player.stats.get(match_id)
    
    def get_team_match_stats(
        self,
        team_id: str,
        match_id: str
    ) -> Optional[Dict]:
        """Get team statistics for a specific match"""
        team = self.session.query(Team).filter_by(id=team_id).first()
        if not team or not team.stats:
            return None
            
        return team.stats.get(match_id)
    
    def get_tracking_data(
        self,
        match_id: str,
        frame_number: Optional[int] = None,
        timestamp: Optional[datetime] = None
    ) -> Optional[Dict]:
        """Get tracking data for a specific frame or timestamp"""
        query = self.session.query(PlayerTrackingData).filter_by(match_id=match_id)
        
        if frame_number is not None:
            query = query.filter_by(frame_number=frame_number)
        elif timestamp is not None:
            query = query.filter_by(timestamp=timestamp)
        else:
            # Get latest frame if no specific time is provided
            query = query.order_by(desc(PlayerTrackingData.frame_number))
            
        tracking_data = query.first()
        if not tracking_data:
            return None
            
        # Get corresponding ball position
        ball_data = self.session.query(BallTrackingData).filter_by(
            match_id=match_id,
            frame_number=tracking_data.frame_number
        ).first()
        
        return {
            "match_id": match_id,
            "frame_number": tracking_data.frame_number,
            "timestamp": tracking_data.timestamp,
            "players": [
                {
                    "player_id": data.player_id,
                    "team_id": data.team_id,
                    "position": {
                        "x": data.x_position,
                        "y": data.y_position
                    },
                    "speed": data.speed,
                    "direction": data.direction
                }
                for data in tracking_data
            ],
            "ball_position": {
                "x": ball_data.x_position,
                "y": ball_data.y_position,
                "z": ball_data.z_position
            } if ball_data else None
        }
    
    def get_field_view(
        self,
        match_id: str,
        timestamp: datetime
    ) -> Optional[Dict]:
        """Get field view data for visualization"""
        tracking_data = self.get_tracking_data(match_id, timestamp=timestamp)
        if not tracking_data:
            return None
            
        # Get field dimensions from match settings
        match = self.session.query(Match).filter_by(id=match_id).first()
        if not match:
            return None
            
        return {
            "match_id": match_id,
            "timestamp": timestamp,
            "field_dimensions": {
                "width": 105.0,  # Standard football field dimensions
                "height": 68.0
            },
            "players": tracking_data["players"],
            "ball_position": tracking_data["ball_position"]
        }
    
    def get_player_heatmap(
        self,
        player_id: str,
        match_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Optional[Dict]:
        """Get player position heatmap data"""
        query = self.session.query(PlayerTrackingData).filter_by(
            match_id=match_id,
            player_id=player_id
        )
        
        if start_time:
            query = query.filter(PlayerTrackingData.timestamp >= start_time)
        if end_time:
            query = query.filter(PlayerTrackingData.timestamp <= end_time)
            
        positions = [
            (data.x_position, data.y_position)
            for data in query.all()
        ]
        
        if not positions:
            return None
            
        # Create 2D histogram
        pos_array = np.array(positions)
        heatmap, xedges, yedges = np.histogram2d(
            pos_array[:, 0],
            pos_array[:, 1],
            bins=(20, 20),
            range=[[0, 105], [0, 68]]
        )
        
        return {
            "data": heatmap.tolist(),
            "x_edges": xedges.tolist(),
            "y_edges": yedges.tolist()
        } 