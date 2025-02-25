from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class Position(BaseModel):
    x: float
    y: float
    z: Optional[float] = None

class PlayerStats(BaseModel):
    player_id: str
    team_id: str
    statistics: Dict = Field(
        ...,
        example={
            "distance_covered": 10.5,
            "average_speed": 15.2,
            "max_speed": 25.4,
            "possession_time": 120.5,
            "passes": {
                "attempted": 50,
                "completed": 45,
                "accuracy": 90.0
            },
            "shots": {
                "attempted": 5,
                "on_target": 3,
                "accuracy": 60.0
            }
        }
    )
    heatmap: Optional[Dict] = None

class TeamStats(BaseModel):
    team_id: str
    statistics: Dict = Field(
        ...,
        example={
            "possession": 55.5,
            "distance_covered": 110.5,
            "passes": {
                "completed": 450,
                "accuracy": 85.5
            },
            "shots": {
                "total": 15,
                "on_target": 8,
                "accuracy": 53.3
            }
        }
    )

class MatchReport(BaseModel):
    id: str
    match_id: str
    report_type: str
    data: Dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PlayerPosition(BaseModel):
    player_id: str
    team_id: str
    position: Position
    speed: Optional[float] = None
    direction: Optional[float] = None

class MatchSummary(BaseModel):
    match_id: str
    timestamp: datetime
    teams: Dict[str, TeamStats]
    players: Dict[str, PlayerStats]

class TrackingData(BaseModel):
    match_id: str
    frame_number: int
    timestamp: datetime
    players: List[PlayerPosition]
    ball_position: Optional[Position] = None

class FieldView(BaseModel):
    match_id: str
    timestamp: datetime
    field_dimensions: Dict[str, float] = Field(
        ...,
        example={
            "width": 105.0,
            "height": 68.0
        }
    )
    homography_matrix: Optional[List[List[float]]] = None
    players: List[PlayerPosition]
    ball_position: Optional[Position] = None
    
    class Config:
        schema_extra = {
            "example": {
                "match_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": "2024-03-20T15:30:00",
                "field_dimensions": {
                    "width": 105.0,
                    "height": 68.0
                },
                "homography_matrix": [
                    [1.2, 0.1, -50.0],
                    [0.0, 1.5, -30.0],
                    [0.0, 0.0, 1.0]
                ],
                "players": [
                    {
                        "player_id": "player1",
                        "team_id": "team1",
                        "position": {
                            "x": 23.5,
                            "y": 45.2,
                            "z": 0.0
                        },
                        "speed": 12.3,
                        "direction": 45.0
                    }
                ],
                "ball_position": {
                    "x": 52.5,
                    "y": 34.0,
                    "z": 1.2
                }
            }
        } 