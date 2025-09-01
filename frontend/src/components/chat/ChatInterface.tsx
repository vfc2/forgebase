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
        <div className="h-full flex flex-col">
            {/* Chat header with reset button */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
                <h2 className="text-lg font-medium text-gray-900">
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
                <div className="mx-4 mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <p className="text-sm text-red-800">
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
