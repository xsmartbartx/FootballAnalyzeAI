import React from 'react';
import { PlayerStats, TeamStats } from '../types';
import {
    StatsPanelContainer,
    StatsSection,
    SectionTitle,
    StatRow,
    StatLabel,
    StatValue
} from '../styles/StatsPanel.styled';

interface StatsPanelProps {
    playerStats: PlayerStats | null;
    teamStats: Record<string, TeamStats>;
    selectedPlayer: string | null;
}

export const StatsPanel: React.FC<StatsPanelProps> = ({
    playerStats,
    teamStats,
    selectedPlayer
}) => {
    return (
        <StatsPanelContainer>
            {Object.entries(teamStats).map(([teamId, stats]) => (
                <StatsSection key={teamId}>
                    <SectionTitle>Team {teamId}</SectionTitle>
                    <StatRow>
                        <StatLabel>Possession</StatLabel>
                        <StatValue>{stats.statistics.possession.toFixed(1)}%</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Distance</StatLabel>
                        <StatValue>{stats.statistics.distance_covered.toFixed(1)} km</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Pass Accuracy</StatLabel>
                        <StatValue>{stats.statistics.passes.accuracy.toFixed(1)}%</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Shots on Target</StatLabel>
                        <StatValue>
                            {stats.statistics.shots.on_target} / {stats.statistics.shots.total}
                        </StatValue>
                    </StatRow>
                </StatsSection>
            ))}
            
            {playerStats && (
                <StatsSection>
                    <SectionTitle>Player Stats</SectionTitle>
                    <StatRow>
                        <StatLabel>Distance</StatLabel>
                        <StatValue>
                            {playerStats.statistics.distance_covered.toFixed(1)} km
                        </StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Avg Speed</StatLabel>
                        <StatValue>{playerStats.statistics.average_speed.toFixed(1)} km/h</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Max Speed</StatLabel>
                        <StatValue>{playerStats.statistics.max_speed.toFixed(1)} km/h</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Pass Accuracy</StatLabel>
                        <StatValue>{playerStats.statistics.passes.accuracy.toFixed(1)}%</StatValue>
                    </StatRow>
                    <StatRow>
                        <StatLabel>Shot Accuracy</StatLabel>
                        <StatValue>{playerStats.statistics.shots.accuracy.toFixed(1)}%</StatValue>
                    </StatRow>
                </StatsSection>
            )}
        </StatsPanelContainer>
    );
}; 