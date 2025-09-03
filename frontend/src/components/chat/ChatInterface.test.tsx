import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider } from '@mantine/core';
import { ChatInterface } from './ChatInterface';

// Mock the useChat hook
vi.mock('../../hooks/useChat', () => ({
    useChat: vi.fn()
}));

// Import the mocked hook
import { useChat } from '../../hooks/useChat';
const mockUseChat = vi.mocked(useChat);

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('ChatInterface', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Default mock implementation
        mockUseChat.mockReturnValue({
            messages: [],
            isStreaming: false,
            sendMessage: vi.fn(),
            resetChat: vi.fn(),
            isLoading: false,
            error: null,
            isResetting: false,
        });
    });

    it('renders the chat interface components', () => {
        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        // Should render MessageList and MessageInput components
        expect(screen.getByRole('textbox')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
    });

    it('shows empty state when no messages', () => {
        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        expect(screen.getByText('Welcome to forgebase')).toBeInTheDocument();
    });

    it('displays messages when they exist', () => {
        // Mock useChat hook with messages
        mockUseChat.mockReturnValue({
            messages: [
                {
                    id: '1',
                    content: 'Hello, world!',
                    role: 'user' as const,
                    timestamp: new Date()
                },
                {
                    id: '2',
                    content: 'Hello! How can I help you?',
                    role: 'assistant' as const,
                    timestamp: new Date()
                }
            ],
            isStreaming: false,
            sendMessage: vi.fn(),
            resetChat: vi.fn(),
            isLoading: false,
            error: null,
            isResetting: false,
        });

        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        expect(screen.getByText('Hello, world!')).toBeInTheDocument();
        expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });

    it('calls sendMessage when user submits a message', async () => {
        const user = userEvent.setup();
        const mockSendMessage = vi.fn();
        
        // Mock useChat hook
        mockUseChat.mockReturnValue({
            messages: [],
            isStreaming: false,
            sendMessage: mockSendMessage,
            resetChat: vi.fn(),
            isLoading: false,
            error: null,
            isResetting: false,
        });

        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        await user.type(textarea, 'Test message');
        await user.keyboard('{Enter}');
        
        expect(mockSendMessage).toHaveBeenCalledWith('Test message');
    });

    it('disables input when loading', () => {
        // Mock useChat hook with loading state
        mockUseChat.mockReturnValue({
            messages: [],
            isStreaming: false,
            sendMessage: vi.fn(),
            resetChat: vi.fn(),
            isLoading: true,
            error: null,
            isResetting: false,
        });

        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        const sendButton = screen.getByRole('button', { name: /sending message/i });
        
        expect(textarea).toBeDisabled();
        expect(sendButton).toBeDisabled();
    });

    it('provides proper accessibility attributes', () => {
        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        // Check for proper ARIA labels and roles
        const textarea = screen.getByRole('textbox');
        expect(textarea).toHaveAttribute('placeholder', 'Describe your project, features, or ask questions about PRDs...');
        
        const sendButton = screen.getByRole('button', { name: /send message/i });
        expect(sendButton).toBeInTheDocument();
    });

    it('maintains focus management properly', async () => {
        const user = userEvent.setup();
        
        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        
        // Focus should be manageable
        await user.click(textarea);
        expect(textarea).toHaveFocus();
    });

    it('handles keyboard navigation correctly', async () => {
        const user = userEvent.setup();
        
        // Mock useChat hook with non-loading state
        mockUseChat.mockReturnValue({
            messages: [],
            isStreaming: false,
            sendMessage: vi.fn(),
            resetChat: vi.fn(),
            isLoading: false,
            error: null,
            isResetting: false,
        });
        
        render(
            <TestWrapper>
                <ChatInterface />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        
        // Tab navigation should work
        await user.tab();
        expect(textarea).toHaveFocus();
        
        // Type some text to enable the send button
        await user.type(textarea, 'Test message');
        
        const sendButton = screen.getByRole('button', { name: /send message/i });
        await user.tab();
        expect(sendButton).toHaveFocus();
    });
});
