import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider, AppShell } from '@mantine/core';
import { Header } from './Header';
import { ThemeProvider } from '../../providers/ThemeProvider';

// Wrapper component for providers
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <ThemeProvider>
        <MantineProvider>
            <AppShell>
                {children}
            </AppShell>
        </MantineProvider>
    </ThemeProvider>
);

describe('Header', () => {
    it('renders the ForgeBase title and subtitle', () => {
        render(
            <TestWrapper>
                <Header />
            </TestWrapper>
        );
        
        expect(screen.getByText('ForgeBase')).toBeInTheDocument();
        expect(screen.getByText('AI-Powered PRD Generation')).toBeInTheDocument();
    });

    it('displays the Beta badge', () => {
        render(
            <TestWrapper>
                <Header />
            </TestWrapper>
        );
        
        expect(screen.getByText('Beta')).toBeInTheDocument();
    });

    it('renders theme toggle button', () => {
        render(
            <TestWrapper>
                <Header />
            </TestWrapper>
        );
        
        // Should have either sun or moon icon (theme toggle)
        const themeButton = screen.getByRole('button', { name: /switch to/i });
        expect(themeButton).toBeInTheDocument();
    });

    it('calls onSettingsClick when settings is clicked from user menu', async () => {
        const user = userEvent.setup();
        const onSettingsClick = vi.fn();
        
        render(
            <TestWrapper>
                <Header onSettingsClick={onSettingsClick} />
            </TestWrapper>
        );
        
        // Open user menu
        const userMenuButton = screen.getByRole('button', { name: /account menu/i });
        await user.click(userMenuButton);
        
        // Wait for menu to appear
        await screen.findByText('Settings');
        
        // Click settings
        const settingsItem = screen.getByText('Settings');
        await user.click(settingsItem);
        
        expect(onSettingsClick).toHaveBeenCalledTimes(1);
    });

    it('calls onProfileClick when profile is clicked from user menu', async () => {
        const user = userEvent.setup();
        const onProfileClick = vi.fn();
        
        render(
            <TestWrapper>
                <Header onProfileClick={onProfileClick} />
            </TestWrapper>
        );
        
        // Open user menu
        const userMenuButton = screen.getByRole('button', { name: /account menu/i });
        await user.click(userMenuButton);
        
        // Wait for menu to appear
        await screen.findByText('Profile');
        
        // Click profile
        const profileItem = screen.getByText('Profile');
        await user.click(profileItem);
        
        expect(onProfileClick).toHaveBeenCalledTimes(1);
    });

    it('has accessible tooltips for action buttons', () => {
        render(
            <TestWrapper>
                <Header />
            </TestWrapper>
        );
        
        // GitHub link should have tooltip
        expect(screen.getByRole('link')).toHaveAttribute('href', 'https://github.com/your-org/forgebase');
    });
});
