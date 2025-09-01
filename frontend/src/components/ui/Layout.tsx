import React from 'react';

interface LayoutProps {
    children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="chat-container">
            {/* Header */}
            <header className="chat-header">
                <h1>Forgebase Chat</h1>
                <div style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.25rem' }}>
                    Conversational PRD Generation
                </div>
            </header>

            {/* Main content */}
            <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {children}
            </main>
        </div>
    );
};
