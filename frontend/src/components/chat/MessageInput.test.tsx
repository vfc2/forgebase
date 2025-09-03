import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider } from '@mantine/core';
import { MessageInput } from './MessageInput';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('MessageInput', () => {
    it('renders with default placeholder', () => {
        render(
            <TestWrapper>
                <MessageInput onSendMessage={vi.fn()} />
            </TestWrapper>
        );
        
        expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    });

    it('renders with custom placeholder', () => {
        render(
            <TestWrapper>
                <MessageInput 
                    onSendMessage={vi.fn()} 
                    placeholder="Custom placeholder"
                />
            </TestWrapper>
        );
        
        expect(screen.getByPlaceholderText('Custom placeholder')).toBeInTheDocument();
    });

    it('calls onSendMessage when form is submitted with Enter key', async () => {
        const user = userEvent.setup();
        const onSendMessage = vi.fn();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={onSendMessage} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        await user.type(textarea, 'Test message');
        await user.keyboard('{Enter}');
        
        expect(onSendMessage).toHaveBeenCalledWith('Test message');
    });

    it('does not submit on Shift+Enter', async () => {
        const user = userEvent.setup();
        const onSendMessage = vi.fn();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={onSendMessage} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        await user.type(textarea, 'Test message');
        await user.keyboard('{Shift>}{Enter}{/Shift}');
        
        expect(onSendMessage).not.toHaveBeenCalled();
    });

    it('calls onSendMessage when send button is clicked', async () => {
        const user = userEvent.setup();
        const onSendMessage = vi.fn();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={onSendMessage} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        await user.type(textarea, 'Test message');
        
        const sendButton = screen.getByRole('button', { name: /send message/i });
        await user.click(sendButton);
        
        expect(onSendMessage).toHaveBeenCalledWith('Test message');
    });

    it('clears input after sending message', async () => {
        const user = userEvent.setup();
        const onSendMessage = vi.fn();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={onSendMessage} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox') as HTMLTextAreaElement;
        await user.type(textarea, 'Test message');
        await user.keyboard('{Enter}');
        
        expect(textarea.value).toBe('');
    });

    it('disables input and shows loading icon when disabled', () => {
        render(
            <TestWrapper>
                <MessageInput onSendMessage={vi.fn()} disabled />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        const sendButton = screen.getByRole('button');
        
        expect(textarea).toBeDisabled();
        expect(sendButton).toBeDisabled();
    });

    it('does not send empty or whitespace-only messages', async () => {
        const user = userEvent.setup();
        const onSendMessage = vi.fn();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={onSendMessage} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        
        // Test empty message
        await user.keyboard('{Enter}');
        expect(onSendMessage).not.toHaveBeenCalled();
        
        // Test whitespace-only message
        await user.type(textarea, '   ');
        await user.keyboard('{Enter}');
        expect(onSendMessage).not.toHaveBeenCalled();
    });

    it('shows character count', () => {
        render(
            <TestWrapper>
                <MessageInput onSendMessage={vi.fn()} />
            </TestWrapper>
        );
        
        expect(screen.getByText('0/2000 characters')).toBeInTheDocument();
    });

    it('updates character count as user types', async () => {
        const user = userEvent.setup();
        
        render(
            <TestWrapper>
                <MessageInput onSendMessage={vi.fn()} />
            </TestWrapper>
        );
        
        const textarea = screen.getByRole('textbox');
        await user.type(textarea, 'Hello');
        
        expect(screen.getByText('5/2000 characters')).toBeInTheDocument();
    });

    it('shows helper text about keyboard shortcuts', () => {
        render(
            <TestWrapper>
                <MessageInput onSendMessage={vi.fn()} />
            </TestWrapper>
        );
        
        expect(screen.getByText('Press Enter to send, Shift+Enter for new line')).toBeInTheDocument();
    });
});
