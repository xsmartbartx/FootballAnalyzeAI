from typing import Dict, List, Tuple
import json
from datetime import datetime
from .metrics_collector import MetricsCollector, PlayerMetrics, TeamMetrics
import numpy as np

class MatchReport:
    """Generates match analysis reports"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        
    def generate_player_report(self, player_id: str) -> Dict:
        """Generate detailed report for a player"""
        if player_id not in self.metrics.player_metrics:
            return {}
            
        metrics = self.metrics.player_metrics[player_id]
        return {
            'player_id': player_id,
            'team_id': metrics.team_id,
            'statistics': {
                'distance_covered': round(metrics.distance_covered, 2),
                'average_speed': round(metrics.average_speed, 2),
                'max_speed': round(metrics.max_speed, 2),
                'possession_time': round(metrics.possession_time, 2),
                'passes': {
                    'attempted': metrics.passes_attempted,
                    'completed': metrics.passes_completed,
                    'accuracy': round(
                        metrics.passes_completed / metrics.passes_attempted * 100
                        if metrics.passes_attempted > 0 else 0,
                        2
                    )
                },
                'shots': {
                    'attempted': metrics.shots_attempted,
                    'on_target': metrics.shots_on_target,
                    'accuracy': round(
                        metrics.shots_on_target / metrics.shots_attempted * 100
                        if metrics.shots_attempted > 0 else 0,
                        2
                    )
                }
            },
            'heatmap': self._generate_heatmap(metrics.position_history)
        }
    
    def generate_team_report(self, team_id: str) -> Dict:
        """Generate detailed report for a team"""
        if team_id not in self.metrics.team_metrics:
            return {}
            
        metrics = self.metrics.team_metrics[team_id]
        return {
            'team_id': team_id,
            'statistics': {
                'possession': round(metrics.possession, 2),
                'distance_covered': round(metrics.distance_covered, 2),
                'passes': {
                    'completed': metrics.passes_completed,
                    'accuracy': round(metrics.pass_accuracy, 2)
                },
                'shots': {
                    'total': metrics.shots,
                    'on_target': metrics.shots_on_target,
                    'accuracy': round(
                        metrics.shots_on_target / metrics.shots * 100
                        if metrics.shots > 0 else 0,
                        2
                    )
                }
            }
        }
    
    def generate_match_report(self) -> Dict:
        """Generate comprehensive match report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'teams': {
                team_id: self.generate_team_report(team_id)
                for team_id in self.metrics.team_metrics
            },
            'players': {
                player_id: self.generate_player_report(player_id)
                for player_id in self.metrics.player_metrics
            }
        }
    
    def _generate_heatmap(self, positions: List[Tuple[float, float]]) -> Dict:
        """Generate position heatmap data"""
        if not positions:
            return {}
            
        # Convert positions to numpy array for easier processing
        pos_array = np.array(positions)
        
        # Create 2D histogram
        heatmap, xedges, yedges = np.histogram2d(
            pos_array[:, 0],
            pos_array[:, 1],
            bins=(20, 20),
            range=[[0, 105], [0, 68]]
        )
        
        return {
            'data': heatmap.tolist(),
            'x_edges': xedges.tolist(),
            'y_edges': yedges.tolist()
        } 