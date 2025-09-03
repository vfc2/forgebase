import React, { useState } from 'react';
import { AppShell } from '@mantine/core';
import { Header } from '../layout/Header';
import { Sidebar } from '../layout/Sidebar';

interface LayoutProps {
    children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    const [sidebarOpened] = useState(false);

    const handleNewChat = () => {
        // TODO: Implement new chat functionality
        console.log('New chat requested');
    };

    const handleClearHistory = () => {
        // TODO: Implement clear history functionality
        console.log('Clear history requested');
    };

    const handleChatSelect = (chatId: string) => {
        // TODO: Implement chat selection functionality
        console.log('Chat selected:', chatId);
    };

    const handleSettingsClick = () => {
        // TODO: Implement settings functionality
        console.log('Settings clicked');
    };

    const handleProfileClick = () => {
        // TODO: Implement profile functionality
        console.log('Profile clicked');
    };

    // Mock chat history data - replace with real data
    const mockChatHistory = [
        {
            id: '1',
            title: 'E-commerce Platform PRD',
            timestamp: new Date(2025, 8, 1)
        },
        {
            id: '2', 
            title: 'Mobile App Requirements',
            timestamp: new Date(2025, 8, 2)
        },
        {
            id: '3',
            title: 'API Documentation Plan',
            timestamp: new Date(2025, 8, 3)
        }
    ];

    return (
        <AppShell
            header={{ height: 70 }}
            navbar={{
                width: 280,
                breakpoint: 'sm',
                collapsed: { mobile: !sidebarOpened }
            }}
            padding="0"
            styles={{
                main: {
                    backgroundColor: 'light-dark(#fcfcfc, var(--mantine-color-dark-7))'
                },
                header: {
                    backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-7))',
                    borderColor: 'light-dark(#e8eaed, var(--mantine-color-dark-5))'
                },
                navbar: {
                    backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-8))',
                    borderColor: 'light-dark(#e8eaed, var(--mantine-color-dark-5))'
                }
            }}
        >
            <Header 
                onSettingsClick={handleSettingsClick}
                onProfileClick={handleProfileClick}
            />
            
            <Sidebar
                onNewChat={handleNewChat}
                onClearHistory={handleClearHistory}
                chatHistory={mockChatHistory}
                onChatSelect={handleChatSelect}
                currentChatId="1"
            />

            <AppShell.Main
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    height: 'calc(100vh - 70px)'
                }}
            >
                {children}
            </AppShell.Main>
        </AppShell>
    );
};
