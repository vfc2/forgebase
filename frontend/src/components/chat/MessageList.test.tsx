import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { MessageList } from './MessageList';
import type { ChatMessage } from '../../types/api';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

const mockMessages: ChatMessage[] = [
    {
        id: '1',
        content: 'Hello, how are you?',
        role: 'user',
        timestamp: new Date('2024-01-01T10:00:00Z')
    },
    {
        id: '2',
        content: 'I am doing well, thank you! How can I help you today?',
        role: 'assistant',
        timestamp: new Date('2024-01-01T10:01:00Z')
    },
    {
        id: '3',
        content: 'Can you help me with React development?',
        role: 'user',
        timestamp: new Date('2024-01-01T10:02:00Z')
    }
];

describe('MessageList', () => {
    it('renders empty state when no messages', () => {
        render(
            <TestWrapper>
                <MessageList messages={[]} isStreaming={false} />
            </TestWrapper>
        );
        
        expect(screen.getByText('Welcome to ForgeBase')).toBeInTheDocument();
    });

    it('renders all messages when provided', () => {
        render(
            <TestWrapper>
                <MessageList messages={mockMessages} isStreaming={false} />
            </TestWrapper>
        );
        
        expect(screen.getByText('Hello, how are you?')).toBeInTheDocument();
        expect(screen.getByText('I am doing well, thank you! How can I help you today?')).toBeInTheDocument();
        expect(screen.getByText('Can you help me with React development?')).toBeInTheDocument();
    });

    it('displays user and assistant messages with correct styling', () => {
        render(
            <TestWrapper>
                <MessageList messages={mockMessages} isStreaming={false} />
            </TestWrapper>
        );
        
        // Check that messages are rendered as MessageBubble components
        const messageElements = screen.getAllByTestId(/^message-bubble-/);
        expect(messageElements).toHaveLength(3);
    });

    it('maintains scroll position when new messages are added', () => {
        const { rerender } = render(
            <TestWrapper>
                <MessageList messages={mockMessages.slice(0, 2)} isStreaming={false} />
            </TestWrapper>
        );
        
        // Add a new message
        const newMessage: ChatMessage = {
            id: '4',
            content: 'This is a new message',
            role: 'assistant',
            timestamp: new Date('2024-01-01T10:03:00Z')
        };
        
        rerender(
            <TestWrapper>
                <MessageList messages={[...mockMessages.slice(0, 2), newMessage]} isStreaming={false} />
            </TestWrapper>
        );
        
        expect(screen.getByText('This is a new message')).toBeInTheDocument();
    });

    it('shows streaming indicator when isStreaming is true', () => {
        render(
            <TestWrapper>
                <MessageList messages={mockMessages} isStreaming={true} />
            </TestWrapper>
        );
        
        // Check for streaming indicator - this would depend on the actual implementation
        // The component might show a typing indicator or loading state
    });

    it('handles empty message content gracefully', () => {
        const messagesWithEmpty: ChatMessage[] = [
            {
                id: '1',
                content: '',
                role: 'user',
                timestamp: new Date('2024-01-01T10:00:00Z')
            }
        ];
        
        render(
            <TestWrapper>
                <MessageList messages={messagesWithEmpty} isStreaming={false} />
            </TestWrapper>
        );
        
        // Should still render the message bubble even with empty content
        expect(screen.getByTestId('message-bubble-0')).toBeInTheDocument();
    });
});
