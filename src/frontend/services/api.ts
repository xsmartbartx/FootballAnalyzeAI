import axios from 'axios';
import { FieldViewData, PlayerStats, TeamStats, HeatmapData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export class ApiService {
    static async getFieldView(matchId: string, timestamp: string): Promise<FieldViewData> {
        const response = await axios.get(
            `${API_BASE_URL}/matches/${matchId}/field-view`,
            { params: { timestamp } }
        );
        return response.data;
    }
    
    static async getPlayerStats(playerId: string, matchId: string): Promise<PlayerStats> {
        const response = await axios.get(
            `${API_BASE_URL}/players/${playerId}/stats`,
            { params: { match_id: matchId } }
        );
        return response.data;
    }
    
    static async getTeamStats(teamId: string, matchId: string): Promise<TeamStats> {
        const response = await axios.get(
            `${API_BASE_URL}/teams/${teamId}/stats`,
            { params: { match_id: matchId } }
        );
        return response.data;
    }
    
    static async getPlayerHeatmap(
        playerId: string,
        matchId: string,
        startTime?: string,
        endTime?: string
    ): Promise<HeatmapData> {
        const response = await axios.get(
            `${API_BASE_URL}/matches/${matchId}/heatmaps/${playerId}`,
            { params: { start_time: startTime, end_time: endTime } }
        );
        return response.data;
    }
} 