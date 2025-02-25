import React, { useState, useEffect, useRef } from 'react';
import { FieldView } from './FieldView';
import { HeatmapView } from './HeatmapView';
import { StatsPanel } from './StatsPanel';
import { ApiService } from '../services/api';
import { FieldViewData, PlayerStats, TeamStats } from '../types';
import {
    DashboardContainer,
    MainView,
    SidePanel,
    ErrorMessage,
    LoadingSpinner
} from '../styles/Dashboard.styled';
import { WebSocketService } from '../services/websocket';

interface DashboardProps {
    matchId: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ matchId }) => {
    const [fieldData, setFieldData] = useState<FieldViewData | null>(null);
    const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
    const [playerStats, setPlayerStats] = useState<PlayerStats | null>(null);
    const [teamStats, setTeamStats] = useState<Record<string, TeamStats>>({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const wsRef = useRef<WebSocketService | null>(null);
    
    useEffect(() => {
        // Initialize WebSocket connection
        const wsUrl = `${process.env.REACT_APP_WS_URL || 'ws://localhost:8000'}/ws/matches/${matchId}`;
        wsRef.current = new WebSocketService(wsUrl);
        wsRef.current.connect();

        // Subscribe to tracking data updates
        wsRef.current.subscribe('tracking_data', (data: FieldViewData) => {
            setFieldData(data);
        });

        // Subscribe to team stats updates
        wsRef.current.subscribe('team_stats', (data: Record<string, TeamStats>) => {
            setTeamStats(data);
        });

        // Subscribe to player stats updates
        wsRef.current.subscribe('player_stats', (data: PlayerStats) => {
            if (data.player_id === selectedPlayer) {
                setPlayerStats(data);
            }
        });

        return () => {
            wsRef.current?.disconnect();
        };
    }, [matchId]);
    
    const handlePlayerClick = (playerId: string) => {
        setSelectedPlayer(playerId);
    };
    
    if (error) {
        return <ErrorMessage>{error}</ErrorMessage>;
    }
    
    if (!fieldData) {
        return <LoadingSpinner>Loading...</LoadingSpinner>;
    }
    
    return (
        <DashboardContainer>
            <MainView>
                <FieldView
                    data={fieldData}
                    width={800}
                    height={600}
                    onPlayerClick={handlePlayerClick}
                />
            </MainView>
            <SidePanel>
                <StatsPanel
                    playerStats={playerStats}
                    teamStats={teamStats}
                    selectedPlayer={selectedPlayer}
                />
                {playerStats?.heatmap && (
                    <HeatmapView
                        data={playerStats.heatmap}
                        width={400}
                        height={300}
                    />
                )}
            </SidePanel>
        </DashboardContainer>
    );
}; 