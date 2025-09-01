import React from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { Button } from '../ui/Button';
import { useChat } from '../../hooks/useChat';

export const ChatInterface: React.FC = () => {
    const {
        messages,
        isStreaming,
        sendMessage,
        resetChat,
        isLoading,
        error,
        isResetting,
    } = useChat();

    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Chat header with reset button */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.75rem 1rem',
                borderBottom: '1px solid #e5e7eb',
                backgroundColor: 'white'
            }}>
                <h2 style={{
                    fontSize: '1.125rem',
                    fontWeight: '500',
                    color: '#111827',
                    margin: 0
                }}>
                    Conversation
                </h2>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={resetChat}
                    disabled={isResetting || messages.length === 0}
                >
                    {isResetting ? 'Resetting...' : 'Reset Chat'}
                </Button>
            </div>

            {/* Error display */}
            {error && (
                <div style={{
                    margin: '1rem',
                    padding: '0.75rem',
                    backgroundColor: '#fef2f2',
                    border: '1px solid #fecaca',
                    borderRadius: '0.375rem'
                }}>
                    <div style={{ display: 'flex' }}>
                        <div style={{ flexShrink: 0 }}>
                            <svg style={{ height: '1.25rem', width: '1.25rem', color: '#ef4444' }} viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div style={{ marginLeft: '0.75rem' }}>
                            <p style={{ fontSize: '0.875rem', color: '#991b1b', margin: 0 }}>
                                {error instanceof Error ? error.message : 'An error occurred'}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Messages */}
            <MessageList messages={messages} isStreaming={isStreaming} />

            {/* Input */}
            <MessageInput
                onSendMessage={sendMessage}
                disabled={isLoading || isStreaming}
                placeholder={isStreaming ? 'Please wait...' : 'Type your message...'}
            />
        </div>
    );
};
