import React from 'react';
import { AppShell, Title, Text } from '@mantine/core';

interface LayoutProps {
    children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <AppShell
            header={{ height: 70 }}
            padding="md"
        >
            <AppShell.Header p="md">
                <Title order={1} size="h2">Forgebase Chat</Title>
                <Text size="sm" c="dimmed">
                    Conversational PRD Generation
                </Text>
            </AppShell.Header>

            <AppShell.Main style={{ display: 'flex', flexDirection: 'column' }}>
                {children}
            </AppShell.Main>
        </AppShell>
    );
};
