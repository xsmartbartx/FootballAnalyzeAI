from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import logging
from datetime import datetime

from database.connection import DatabaseConnection
from database.config import DatabaseConfig
from database.analytics_repository import AnalyticsRepository
from .schemas import (
    MatchReport,
    PlayerStats,
    TeamStats,
    MatchSummary,
    PlayerPosition,
    TrackingData,
    FieldView
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Football Analytics API",
    description="API for accessing football match analytics data",
    version="1.0.0"
)

# Database dependency
def get_db():
    db = DatabaseConnection(DatabaseConfig())
    try:
        session = next(db.get_session())
        yield session
    finally:
        session.close()

@app.get("/matches/{match_id}/reports", response_model=List[MatchReport])
def get_match_reports(
    match_id: str,
    report_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get analytics reports for a match"""
    try:
        repo = AnalyticsRepository(db)
        reports = repo.get_match_reports(match_id, report_type, limit)
        return reports
    except Exception as e:
        logger.error(f"Error getting match reports: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/matches/{match_id}/summary", response_model=MatchSummary)
def get_match_summary(
    match_id: str,
    db: Session = Depends(get_db)
):
    """Get latest match summary"""
    try:
        repo = AnalyticsRepository(db)
        reports = repo.get_match_reports(match_id, report_type='final', limit=1)
        if not reports:
            raise HTTPException(status_code=404, detail="Match summary not found")
        return reports[0].data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting match summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/players/{player_id}/stats", response_model=PlayerStats)
def get_player_stats(
    player_id: str,
    match_id: str,
    db: Session = Depends(get_db)
):
    """Get player statistics for a match"""
    try:
        repo = AnalyticsRepository(db)
        stats = repo.get_player_match_stats(player_id, match_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Player stats not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting player stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/teams/{team_id}/stats", response_model=TeamStats)
def get_team_stats(
    team_id: str,
    match_id: str,
    db: Session = Depends(get_db)
):
    """Get team statistics for a match"""
    try:
        repo = AnalyticsRepository(db)
        stats = repo.get_team_match_stats(team_id, match_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Team stats not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/matches/{match_id}/tracking", response_model=TrackingData)
def get_tracking_data(
    match_id: str,
    frame_number: Optional[int] = None,
    timestamp: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get tracking data for a specific frame or timestamp"""
    try:
        repo = AnalyticsRepository(db)
        tracking_data = repo.get_tracking_data(match_id, frame_number, timestamp)
        if not tracking_data:
            raise HTTPException(status_code=404, detail="Tracking data not found")
        return tracking_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tracking data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/matches/{match_id}/field-view", response_model=FieldView)
def get_field_view(
    match_id: str,
    timestamp: datetime,
    db: Session = Depends(get_db)
):
    """Get field view data for visualization"""
    try:
        repo = AnalyticsRepository(db)
        field_view = repo.get_field_view(match_id, timestamp)
        if not field_view:
            raise HTTPException(status_code=404, detail="Field view data not found")
        return field_view
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting field view: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/matches/{match_id}/heatmaps/{player_id}", response_model=Dict)
def get_player_heatmap(
    match_id: str,
    player_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get player position heatmap data"""
    try:
        repo = AnalyticsRepository(db)
        heatmap = repo.get_player_heatmap(player_id, match_id, start_time, end_time)
        if not heatmap:
            raise HTTPException(status_code=404, detail="Heatmap data not found")
        return heatmap
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting player heatmap: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 