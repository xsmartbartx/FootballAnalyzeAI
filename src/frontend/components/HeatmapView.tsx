import React, { useEffect, useRef } from 'react';
import { HeatmapData } from '../types';

interface HeatmapViewProps {
    data: HeatmapData;
    width: number;
    height: number;
}

export const HeatmapView: React.FC<HeatmapViewProps> = ({ data, width, height }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw heatmap
        const maxValue = Math.max(...data.data.flat());
        const cellWidth = width / data.data[0].length;
        const cellHeight = height / data.data.length;
        
        data.data.forEach((row, i) => {
            row.forEach((value, j) => {
                const intensity = value / maxValue;
                ctx.fillStyle = getHeatmapColor(intensity);
                ctx.fillRect(
                    j * cellWidth,
                    i * cellHeight,
                    cellWidth,
                    cellHeight
                );
            });
        });
        
        // Draw field overlay
        drawFieldOverlay(ctx, width, height);
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

function getHeatmapColor(intensity: number): string {
    // Convert intensity to RGB color
    const r = Math.floor(255 * Math.min(1, intensity * 2));
    const g = Math.floor(255 * Math.min(1, intensity * 2));
    const b = Math.floor(255 * (1 - intensity));
    
    return `rgba(${r}, ${g}, ${b}, 0.7)`;
}

function drawFieldOverlay(ctx: CanvasRenderingContext2D, width: number, height: number) {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.lineWidth = 1;
    
    // Draw field outline
    ctx.strokeRect(0, 0, width, height);
    
    // Draw center line and circle
    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, height / 5, 0, Math.PI * 2);
    ctx.stroke();
} 