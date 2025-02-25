import React, { useEffect, useRef } from 'react';
import { FieldViewData, PlayerPosition } from '../types';
import styled from 'styled-components';

interface FieldViewProps {
    data: FieldViewData;
    width: number;
    height: number;
}

const PlayerCircle = styled.div<{ team: string }>`
    position: absolute;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: ${({ theme, team }) => 
        team === 'team1' ? theme.colors.team1 : theme.colors.team2};
    transform: translate(-50%, -50%);
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
        transform: translate(-50%, -50%) scale(1.2);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
`;

const BallCircle = styled.div<{ elevation: number }>`
    position: absolute;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: ${({ theme }) => theme.colors.ball};
    transform: translate(-50%, -50%);
    box-shadow: 0 ${({ elevation }) => elevation * 2}px 
        ${({ elevation }) => elevation * 3}px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
`;

export const FieldView: React.FC<FieldViewProps> = ({ data, width, height }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw field
        drawField(ctx, width, height);
        
        // Draw players
        data.players.forEach(player => {
            drawPlayer(ctx, player, width, height);
        });
        
        // Draw ball if available
        if (data.ball_position) {
            drawBall(ctx, data.ball_position, width, height);
        }
    }, [data, width, height]);
    
    return (
        <canvas
            ref={canvasRef}
            width={width}
            height={height}
            style={{ border: '1px solid #ccc' }}
        />
    );
};

function drawField(ctx: CanvasRenderingContext2D, width: number, height: number) {
    // Draw field outline
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, width, height);
    
    // Draw center line
    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();
    
    // Draw center circle
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, height / 5, 0, Math.PI * 2);
    ctx.stroke();
    
    // Draw penalty areas
    const penaltyAreaWidth = width / 5;
    const penaltyAreaHeight = height / 2.5;
    
    // Left penalty area
    ctx.strokeRect(
        0,
        (height - penaltyAreaHeight) / 2,
        penaltyAreaWidth,
        penaltyAreaHeight
    );
    
    // Right penalty area
    ctx.strokeRect(
        width - penaltyAreaWidth,
        (height - penaltyAreaHeight) / 2,
        penaltyAreaWidth,
        penaltyAreaHeight
    );
}

function drawPlayer(
    ctx: CanvasRenderingContext2D,
    player: PlayerPosition,
    width: number,
    height: number
) {
    const x = (player.position.x / 105) * width;
    const y = (player.position.y / 68) * height;
    
    // Draw player circle
    ctx.beginPath();
    ctx.fillStyle = player.team_id === 'team1' ? '#ff0000' : '#0000ff';
    ctx.arc(x, y, 10, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw player ID
    ctx.fillStyle = '#ffffff';
    ctx.font = '10px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(player.player_id, x, y + 4);
    
    // Draw direction arrow if available
    if (player.direction !== undefined) {
        const angle = (player.direction * Math.PI) / 180;
        const arrowLength = 20;
        
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(
            x + Math.cos(angle) * arrowLength,
            y + Math.sin(angle) * arrowLength
        );
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();
    }
}

function drawBall(
    ctx: CanvasRenderingContext2D,
    position: { x: number; y: number; z?: number },
    width: number,
    height: number
) {
    const x = (position.x / 105) * width;
    const y = (position.y / 68) * height;
    
    // Draw ball circle
    ctx.beginPath();
    ctx.fillStyle = '#ffffff';
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw shadow based on z-position
    if (position.z !== undefined && position.z > 0) {
        ctx.beginPath();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.ellipse(x, y + 5, 6, 3, 0, 0, Math.PI * 2);
        ctx.fill();
    }
} 