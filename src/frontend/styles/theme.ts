export const theme = {
    colors: {
        primary: '#1a1a1a',
        secondary: '#2d2d2d',
        accent: '#4CAF50',
        text: '#ffffff',
        textSecondary: '#b3b3b3',
        error: '#ff4444',
        team1: '#ff0000',
        team2: '#0000ff',
        ball: '#ffffff'
    },
    spacing: {
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px'
    },
    borderRadius: {
        sm: '4px',
        md: '8px',
        lg: '16px'
    },
    shadows: {
        card: '0 4px 6px rgba(0, 0, 0, 0.1)',
        panel: '0 8px 16px rgba(0, 0, 0, 0.15)'
    }
};

export type Theme = typeof theme; 