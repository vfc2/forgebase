import React, { useState, useRef, useEffect } from 'react';
import { Button } from '../ui/Button';
import { cn } from '../../utils/cn';

interface MessageInputProps {
    onSendMessage: (message: string) => void;
    disabled?: boolean;
    placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
    onSendMessage,
    disabled = false,
    placeholder = 'Type your message...',
}) => {
    const [message, setMessage] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim() && !disabled) {
            onSendMessage(message.trim());
            setMessage('');
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [message]);

    return (
        <div className="border-t border-gray-200 bg-white px-4 py-4">
            <div className="max-w-4xl mx-auto">
                <form onSubmit={handleSubmit} className="flex gap-3 items-end">
                    <div className="flex-1">
                        <textarea
                            ref={textareaRef}
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={placeholder}
                            disabled={disabled}
                            rows={1}
                            className={cn(
                                'w-full resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm',
                                'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                                'disabled:cursor-not-allowed disabled:opacity-50',
                                'max-h-32 min-h-[40px]'
                            )}
                        />
                    </div>
                    <Button
                        type="submit"
                        disabled={!message.trim() || disabled}
                        className="h-10"
                    >
                        {disabled ? (
                            <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24">
                                <circle
                                    className="opacity-25"
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke="currentColor"
                                    strokeWidth="4"
                                    fill="none"
                                />
                                <path
                                    className="opacity-75"
                                    fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                                />
                            </svg>
                        ) : (
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        )}
                    </Button>
                </form>
                <div className="mt-2 text-xs text-gray-500">
                    Press Enter to send, Shift+Enter for new line
                </div>
            </div>
        </div>
    );
};
