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
            <div className="flex-1 flex items-center justify-center text-gray-500">
                <div className="text-center">
                    <div className="text-lg font-medium mb-2">
                        Welcome to Forgebase Chat
                    </div>
                    <div className="text-sm">
                        Start a conversation to generate PRDs and work plans
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto px-4 py-4">
            <div className="max-w-4xl mx-auto">
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
