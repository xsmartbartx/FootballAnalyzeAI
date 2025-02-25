export interface Position {
    x: number;
    y: number;
    z?: number;
}

export interface PlayerPosition {
    player_id: string;
    team_id: string;
    position: Position;
    speed?: number;
    direction?: number;
}

export interface FieldViewData {
    match_id: string;
    timestamp: string;
    field_dimensions: {
        width: number;
        height: number;
    };
    homography_matrix?: number[][];
    players: PlayerPosition[];
    ball_position?: Position;
}

export interface HeatmapData {
    data: number[][];
    x_edges: number[];
    y_edges: number[];
}

export interface PlayerStats {
    player_id: string;
    team_id: string;
    statistics: {
        distance_covered: number;
        average_speed: number;
        max_speed: number;
        possession_time: number;
        passes: {
            attempted: number;
            completed: number;
            accuracy: number;
        };
        shots: {
            attempted: number;
            on_target: number;
            accuracy: number;
        };
    };
    heatmap?: HeatmapData;
}

export interface TeamStats {
    team_id: string;
    statistics: {
        possession: number;
        distance_covered: number;
        passes: {
            completed: number;
            accuracy: number;
        };
        shots: {
            total: number;
            on_target: number;
            accuracy: number;
        };
    };
} 