import React from 'react';
import type { ChatMessage } from '../../types/api';
import { cn } from '../../utils/cn';

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
        <div className={cn(
            'flex w-full mb-4',
            isUser ? 'justify-end' : 'justify-start'
        )}>
            <div className={cn(
                'flex max-w-[80%] gap-3',
                isUser ? 'flex-row-reverse' : 'flex-row'
            )}>
                {/* Avatar */}
                <div className={cn(
                    'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                    isUser
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-300 text-gray-700'
                )}>
                    {isUser ? 'U' : 'A'}
                </div>

                {/* Message content */}
                <div className={cn(
                    'rounded-lg px-4 py-2 text-sm',
                    isUser
                        ? 'bg-primary-600 text-white'
                        : 'bg-white border border-gray-200 text-gray-900'
                )}>
                    <div className="whitespace-pre-wrap break-words">
                        {message.content}
                        {isStreaming && (
                            <span className="inline-block w-2 h-4 ml-1 bg-current animate-pulse" />
                        )}
                    </div>
                    <div className={cn(
                        'text-xs mt-1 opacity-70',
                        isUser ? 'text-primary-100' : 'text-gray-500'
                    )}>
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
