import React from 'react';
import type { ChatMessage } from '../../types/api';

interface MessageBubbleProps {
    message: ChatMessage;
    isStreaming?: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
    message,
    isStreaming = false
}) => {
    const isUser = message.role === 'user';

    return (
        <div className="message-bubble" style={{
            width: '100%',
            marginBottom: '1rem',
            display: 'flex',
            justifyContent: isUser ? 'flex-end' : 'flex-start'
        }}>
            <div style={{
                display: 'flex',
                maxWidth: '80%',
                gap: '0.75rem',
                flexDirection: isUser ? 'row-reverse' : 'row'
            }}>
                {/* Avatar */}
                <div style={{
                    flexShrink: 0,
                    width: '2rem',
                    height: '2rem',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.875rem',
                    fontWeight: '500',
                    backgroundColor: isUser ? '#3b82f6' : '#e5e7eb',
                    color: isUser ? 'white' : '#374151'
                }}>
                    {isUser ? 'U' : 'A'}
                </div>

                {/* Message content */}
                <div style={{
                    borderRadius: '0.5rem',
                    padding: '0.75rem 1rem',
                    fontSize: '0.875rem',
                    backgroundColor: isUser ? '#3b82f6' : 'white',
                    color: isUser ? 'white' : '#111827',
                    border: isUser ? 'none' : '1px solid #d1d5db'
                }}>
                    <div style={{
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word',
                        lineHeight: '1.5'
                    }}>
                        {message.content}
                        {isStreaming && (
                            <span style={{
                                display: 'inline-block',
                                width: '0.5rem',
                                height: '1rem',
                                marginLeft: '0.25rem',
                                backgroundColor: 'currentColor',
                                animation: 'pulse 1s ease-in-out infinite'
                            }} />
                        )}
                    </div>
                    <div style={{
                        fontSize: '0.75rem',
                        marginTop: '0.25rem',
                        opacity: 0.7,
                        color: isUser ? '#dbeafe' : '#6b7280'
                    }}>
                        {message.timestamp.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
};
