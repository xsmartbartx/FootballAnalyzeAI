import styled from 'styled-components';
import { fadeIn, slideIn, spin } from './animations';

export const DashboardContainer = styled.div`
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: ${({ theme }) => theme.spacing.lg};
    padding: ${({ theme }) => theme.spacing.lg};
    background-color: ${({ theme }) => theme.colors.primary};
    min-height: 100vh;
`;

export const MainView = styled.div`
    background-color: ${({ theme }) => theme.colors.secondary};
    border-radius: ${({ theme }) => theme.borderRadius.lg};
    padding: ${({ theme }) => theme.spacing.md};
    box-shadow: ${({ theme }) => theme.shadows.panel};
    animation: ${fadeIn} 0.5s ease-in;
    transition: transform 0.3s ease;

    &:hover {
        transform: scale(1.01);
    }
`;

export const SidePanel = styled.div`
    display: flex;
    flex-direction: column;
    gap: ${({ theme }) => theme.spacing.md};
    animation: ${slideIn} 0.5s ease-out;
`;

export const ErrorMessage = styled.div`
    color: ${({ theme }) => theme.colors.error};
    padding: ${({ theme }) => theme.spacing.md};
    background-color: rgba(255, 0, 0, 0.1);
    border-radius: ${({ theme }) => theme.borderRadius.md};
    margin: ${({ theme }) => theme.spacing.md};
    animation: ${fadeIn} 0.3s ease-in;
`;

export const LoadingSpinner = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: ${({ theme }) => theme.colors.text};

    &::after {
        content: '';
        width: 40px;
        height: 40px;
        border: 4px solid ${({ theme }) => theme.colors.textSecondary};
        border-top-color: ${({ theme }) => theme.colors.accent};
        border-radius: 50%;
        animation: ${spin} 1s linear infinite;
    }
`; 