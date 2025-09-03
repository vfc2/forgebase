import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider, AppShell } from '@mantine/core';
import { Sidebar } from './Sidebar';

// Wrapper component for Mantine provider and AppShell context
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>
        <AppShell>
            {children}
        </AppShell>
    </MantineProvider>
);

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
    }
];

describe('Sidebar', () => {
    it('renders the New Conversation button', () => {
        const onNewChat = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewChat={onNewChat} />
            </TestWrapper>
        );
        
        expect(screen.getByText('New Conversation')).toBeInTheDocument();
    });

    it('calls onNewChat when New Conversation button is clicked', async () => {
        const user = userEvent.setup();
        const onNewChat = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewChat={onNewChat} />
            </TestWrapper>
        );
        
        await user.click(screen.getByText('New Conversation'));
        expect(onNewChat).toHaveBeenCalledTimes(1);
    });

    it('displays "No conversations yet" when chat history is empty', () => {
        render(
            <TestWrapper>
                <Sidebar onNewChat={vi.fn()} chatHistory={[]} />
            </TestWrapper>
        );
        
        expect(screen.getByText('No conversations yet')).toBeInTheDocument();
    });

    it('displays chat history when provided', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewChat={vi.fn()} 
                    chatHistory={mockChatHistory}
                />
            </TestWrapper>
        );
        
        expect(screen.getByText('E-commerce Platform PRD')).toBeInTheDocument();
        expect(screen.getByText('Mobile App Requirements')).toBeInTheDocument();
    });

    it('calls onChatSelect when a chat history item is clicked', async () => {
        const user = userEvent.setup();
        const onChatSelect = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar 
                    onNewChat={vi.fn()}
                    chatHistory={mockChatHistory}
                    onChatSelect={onChatSelect}
                />
            </TestWrapper>
        );
        
        await user.click(screen.getByText('E-commerce Platform PRD'));
        expect(onChatSelect).toHaveBeenCalledWith('1');
    });

    it('highlights the current chat', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewChat={vi.fn()}
                    chatHistory={mockChatHistory}
                    currentChatId="1"
                />
            </TestWrapper>
        );
        
        const currentChatButton = screen.getByText('E-commerce Platform PRD').closest('button');
        expect(currentChatButton).toHaveAttribute('data-variant', 'light');
    });

    it('shows clear history button when chat history exists', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewChat={vi.fn()}
                    chatHistory={mockChatHistory}
                    onClearHistory={vi.fn()}
                />
            </TestWrapper>
        );
        
        // The clear history button should be present (tooltip text)
        expect(screen.getByLabelText('Clear History')).toBeInTheDocument();
    });

    it('calls onClearHistory when clear history button is clicked', async () => {
        const user = userEvent.setup();
        const onClearHistory = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar 
                    onNewChat={vi.fn()}
                    chatHistory={mockChatHistory}
                    onClearHistory={onClearHistory}
                />
            </TestWrapper>
        );
        
        await user.click(screen.getByLabelText('Clear History'));
        expect(onClearHistory).toHaveBeenCalledTimes(1);
    });

    it('renders quick action buttons', () => {
        render(
            <TestWrapper>
                <Sidebar onNewChat={vi.fn()} />
            </TestWrapper>
        );
        
        expect(screen.getByText('Tips & Examples')).toBeInTheDocument();
        expect(screen.getByText('Export Chat')).toBeInTheDocument();
        expect(screen.getByText('Preferences')).toBeInTheDocument();
    });
});
