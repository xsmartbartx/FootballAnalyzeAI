from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np

@dataclass
class PlayerMetrics:
    """Metrics collected for each player"""
    player_id: str
    team_id: str
    position_history: List[Tuple[float, float]] = field(default_factory=list)
    distance_covered: float = 0.0
    average_speed: float = 0.0
    max_speed: float = 0.0
    possession_time: float = 0.0
    passes_attempted: int = 0
    passes_completed: int = 0
    shots_attempted: int = 0
    shots_on_target: int = 0

@dataclass
class TeamMetrics:
    """Metrics collected for each team"""
    team_id: str
    possession: float = 0.0
    shots: int = 0
    shots_on_target: int = 0
    passes_completed: int = 0
    pass_accuracy: float = 0.0
    distance_covered: float = 0.0

class MetricsCollector:
    """Collects and analyzes match metrics"""
    
    def __init__(self):
        self.player_metrics: Dict[str, PlayerMetrics] = {}
        self.team_metrics: Dict[str, TeamMetrics] = {}
        self.ball_possession_history: List[str] = []
        self.last_timestamp: Optional[datetime] = None
        
    def update_player_position(
        self,
        player_id: str,
        team_id: str,
        position: Tuple[float, float],
        timestamp: datetime
    ) -> None:
        """Update player position and calculate movement metrics"""
        if player_id not in self.player_metrics:
            self.player_metrics[player_id] = PlayerMetrics(player_id, team_id)
            
        metrics = self.player_metrics[player_id]
        metrics.position_history.append(position)
        
        if len(metrics.position_history) > 1:
            # Calculate distance covered
            prev_pos = metrics.position_history[-2]
            distance = np.sqrt(
                (position[0] - prev_pos[0])**2 +
                (position[1] - prev_pos[1])**2
            )
            metrics.distance_covered += distance
            
            # Calculate speed
            if self.last_timestamp:
                time_diff = (timestamp - self.last_timestamp).total_seconds()
                if time_diff > 0:
                    speed = distance / time_diff
                    metrics.average_speed = (
                        (metrics.average_speed * (len(metrics.position_history) - 2) + speed) /
                        (len(metrics.position_history) - 1)
                    )
                    metrics.max_speed = max(metrics.max_speed, speed)
        
        self.last_timestamp = timestamp
        
    def update_ball_possession(
        self,
        ball_position: Tuple[float, float],
        player_positions: List[Dict],
        timestamp: datetime
    ) -> None:
        """Update ball possession based on proximity"""
        closest_player = None
        min_distance = float('inf')
        
        for player in player_positions:
            if player['class'] in ['player', 'goalkeeper']:
                player_pos = player['position']
                distance = np.sqrt(
                    (ball_position[0] - player_pos[0])**2 +
                    (ball_position[1] - player_pos[1])**2
                )
                
                if distance < min_distance:
                    min_distance = distance
                    closest_player = player
        
        if closest_player and min_distance < 2.0:  # 2 meters threshold
            player_id = str(closest_player['track_id'])
            self.ball_possession_history.append(player_id)
            
            if player_id in self.player_metrics:
                self.player_metrics[player_id].possession_time += (
                    (timestamp - self.last_timestamp).total_seconds()
                    if self.last_timestamp else 0
                )
    
    def update_team_metrics(self) -> None:
        """Update team-level metrics"""
        team_totals: Dict[str, Dict] = {}
        
        for player_metrics in self.player_metrics.values():
            team_id = player_metrics.team_id
            
            if team_id not in team_totals:
                team_totals[team_id] = {
                    'possession_time': 0.0,
                    'distance': 0.0,
                    'passes_completed': 0,
                    'passes_attempted': 0,
                    'shots': 0,
                    'shots_on_target': 0
                }
            
            totals = team_totals[team_id]
            totals['possession_time'] += player_metrics.possession_time
            totals['distance'] += player_metrics.distance_covered
            totals['passes_completed'] += player_metrics.passes_completed
            totals['passes_attempted'] += player_metrics.passes_attempted
            totals['shots'] += player_metrics.shots_attempted
            totals['shots_on_target'] += player_metrics.shots_on_target
        
        # Calculate team metrics
        total_time = sum(t['possession_time'] for t in team_totals.values())
        
        for team_id, totals in team_totals.items():
            if team_id not in self.team_metrics:
                self.team_metrics[team_id] = TeamMetrics(team_id)
                
            metrics = self.team_metrics[team_id]
            metrics.possession = (
                (totals['possession_time'] / total_time * 100)
                if total_time > 0 else 0
            )
            metrics.distance_covered = totals['distance']
            metrics.passes_completed = totals['passes_completed']
            metrics.pass_accuracy = (
                (totals['passes_completed'] / totals['passes_attempted'] * 100)
                if totals['passes_attempted'] > 0 else 0
            )
            metrics.shots = totals['shots']
            metrics.shots_on_target = totals['shots_on_target'] 