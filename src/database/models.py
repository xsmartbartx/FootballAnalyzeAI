from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    avatar_url = Column(String)
    role = Column(Enum('admin', 'coach', 'analyst', name='user_role'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String)
    stats = Column(JSON)  # Store team statistics as JSON
    logo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    players = relationship("Player", back_populates="team")

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    home_team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    venue = Column(String)
    competition = Column(String)
    status = Column(Enum('scheduled', 'live', 'completed', name='match_status'), nullable=False)
    video_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    reports = relationship("AnalyticsReport", back_populates="match")

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)
    jersey_number = Column(Integer)
    name = Column(String, nullable=False)
    position = Column(String)
    stats = Column(JSON)  # Store player statistics as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="players")

class TrackingSession(Base):
    __tablename__ = 'tracking_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(Enum('processing', 'completed', 'failed', name='tracking_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PlayerTrackingData(Base):
    __tablename__ = 'player_tracking_data'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_session_id = Column(UUID(as_uuid=True), ForeignKey('tracking_sessions.id'), nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'), nullable=False)
    frame_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    x_position = Column(Float, nullable=False)
    y_position = Column(Float, nullable=False)
    speed = Column(Float)
    direction = Column(Float)
    confidence_score = Column(Float)

class BallTrackingData(Base):
    __tablename__ = 'ball_tracking_data'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_session_id = Column(UUID(as_uuid=True), ForeignKey('tracking_sessions.id'), nullable=False)
    frame_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    x_position = Column(Float, nullable=False)
    y_position = Column(Float, nullable=False)
    z_position = Column(Float)
    speed = Column(Float)
    trajectory = Column(JSONB)
    confidence_score = Column(Float)

class MatchEvent(Base):
    __tablename__ = 'match_events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id'), nullable=False)
    event_type = Column(Enum('goal', 'pass', 'shot', 'foul', 'offside', name='event_type'), nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'))
    timestamp = Column(DateTime, nullable=False)
    coordinates = Column(Geography('POINT'))
    metadata = Column(JSONB)

class AnalyticsReport(Base):
    __tablename__ = 'analytics_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id'), nullable=False)
    report_type = Column(String, nullable=False)
    data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="reports") 