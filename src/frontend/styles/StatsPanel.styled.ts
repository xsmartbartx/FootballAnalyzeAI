import styled from 'styled-components';
import { fadeIn, slideIn, pulse } from './animations';

export const StatsPanelContainer = styled.div`
    background-color: ${({ theme }) => theme.colors.secondary};
    border-radius: ${({ theme }) => theme.borderRadius.lg};
    padding: ${({ theme }) => theme.spacing.md};
    box-shadow: ${({ theme }) => theme.shadows.panel};
    animation: ${slideIn} 0.5s ease-out;
    transition: box-shadow 0.3s ease;

    &:hover {
        box-shadow: ${({ theme }) => theme.shadows.card};
    }
`;

export const StatsSection = styled.div`
    margin-bottom: ${({ theme }) => theme.spacing.lg};
    animation: ${fadeIn} 0.5s ease-in;

    &:last-child {
        margin-bottom: 0;
    }
`;

export const SectionTitle = styled.h3`
    color: ${({ theme }) => theme.colors.text};
    margin: 0 0 ${({ theme }) => theme.spacing.md};
    padding-bottom: ${({ theme }) => theme.spacing.xs};
    border-bottom: 1px solid ${({ theme }) => theme.colors.accent};
    transition: color 0.3s ease;

    &:hover {
        color: ${({ theme }) => theme.colors.accent};
    }
`;

export const StatRow = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: ${({ theme }) => theme.spacing.xs} 0;
    color: ${({ theme }) => theme.colors.textSecondary};
    transition: all 0.3s ease;

    &:hover {
        color: ${({ theme }) => theme.colors.text};
        transform: translateX(${({ theme }) => theme.spacing.xs});
    }
`;

export const StatLabel = styled.span`
    font-weight: 500;
`;

export const StatValue = styled.span`
    font-family: monospace;
    transition: all 0.3s ease;

    &:hover {
        animation: ${pulse} 1s ease-in-out;
        color: ${({ theme }) => theme.colors.accent};
    }
`; 