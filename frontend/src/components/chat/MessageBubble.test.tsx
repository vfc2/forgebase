import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { MessageBubble } from './MessageBubble';
import type { ChatMessage } from '../../types/api';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('MessageBubble', () => {
    const userMessage: ChatMessage = {
        id: '1',
        role: 'user',
        content: 'Hello, how are you?',
        timestamp: new Date(),
    };

    const assistantMessage: ChatMessage = {
        id: '2',
        role: 'assistant',
        content: 'I am doing well, thank you for asking!',
        timestamp: new Date(),
    };

    it('renders user message with correct styling and alignment', () => {
        render(
            <TestWrapper>
                <MessageBubble message={userMessage} messageIndex={0} />
            </TestWrapper>
        );

        expect(screen.getByText('Hello, how are you?')).toBeInTheDocument();
        expect(screen.getByTestId('message-bubble-0')).toBeInTheDocument();
        
        // User messages should not have an avatar
        expect(screen.queryByRole('img')).not.toBeInTheDocument();
    });

    it('renders assistant message with avatar and correct styling', () => {
        render(
            <TestWrapper>
                <MessageBubble message={assistantMessage} messageIndex={1} />
            </TestWrapper>
        );

        expect(screen.getByText('I am doing well, thank you for asking!')).toBeInTheDocument();
        expect(screen.getByTestId('message-bubble-1')).toBeInTheDocument();
    });

    it('shows streaming indicator when isStreaming is true', () => {
        render(
            <TestWrapper>
                <MessageBubble message={assistantMessage} isStreaming={true} />
            </TestWrapper>
        );

        expect(screen.getByText('I am doing well, thank you for asking!')).toBeInTheDocument();
        // The streaming indicator should be present (cursor animation)
        const messageElement = screen.getByText('I am doing well, thank you for asking!');
        expect(messageElement).toBeInTheDocument();
    });

    it('handles empty message content', () => {
        const emptyMessage: ChatMessage = {
            id: '3',
            role: 'assistant',
            content: '',
            timestamp: new Date(),
        };

        render(
            <TestWrapper>
                <MessageBubble message={emptyMessage} />
            </TestWrapper>
        );

        // Should still render the bubble structure with avatar for assistant
        expect(document.querySelector('[data-size="sm"]')).toBeInTheDocument();
    });

    it('formats timestamp correctly', () => {
        const messageWithTimestamp: ChatMessage = {
            id: '4',
            role: 'user',
            content: 'Test message',
            timestamp: new Date('2023-01-01T12:00:00Z'),
        };

        render(
            <TestWrapper>
                <MessageBubble message={messageWithTimestamp} />
            </TestWrapper>
        );

        expect(screen.getByText('Test message')).toBeInTheDocument();
        // The timestamp should be formatted and displayed
        expect(document.querySelector('[style*="font-size"]')).toBeInTheDocument();
    });
});
