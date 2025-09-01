import React, { useEffect, useRef } from 'react';
import type { ChatMessage } from '../../types/api';
import { MessageBubble } from './MessageBubble';

interface MessageListProps {
    messages: ChatMessage[];
    isStreaming: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({
    messages,
    isStreaming
}) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isStreaming]);

    if (messages.length === 0) {
        return (
            <div className="chat-messages" style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#6b7280'
            }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.125rem', fontWeight: '500', marginBottom: '0.5rem' }}>
                        Welcome to Forgebase Chat
                    </div>
                    <div style={{ fontSize: '0.875rem' }}>
                        Start a conversation to generate PRDs and work plans
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-messages" style={{
            flex: 1,
            overflowY: 'auto',
            padding: '1rem'
        }}>
            <div style={{ maxWidth: '64rem', margin: '0 auto' }}>
                {messages.map((message, index) => (
                    <MessageBubble
                        key={message.id}
                        message={message}
                        isStreaming={isStreaming && index === messages.length - 1 && message.role === 'assistant'}
                    />
                ))}
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
};
