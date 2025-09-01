import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api';
import type { ChatMessage } from '../types/api';

export const useChat = () => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isStreaming, setIsStreaming] = useState(false);
    const queryClient = useQueryClient();

    const generateId = () => `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const addMessage = useCallback((message: Omit<ChatMessage, 'id'>) => {
        const newMessage: ChatMessage = {
            ...message,
            id: generateId(),
        };
        setMessages(prev => [...prev, newMessage]);
        return newMessage;
    }, []);

    const updateLastMessage = useCallback((content: string) => {
        setMessages(prev => {
            if (prev.length === 0) return prev;
            const lastMessage = prev[prev.length - 1];
            if (lastMessage.role !== 'assistant') return prev;

            return [
                ...prev.slice(0, -1),
                { ...lastMessage, content }
            ];
        });
    }, []);

    const sendMessageMutation = useMutation({
        mutationFn: async (message: string) => {
            // Add user message immediately
            addMessage({
                content: message,
                role: 'user',
                timestamp: new Date(),
            });

            // Wait a brief moment to ensure user message is rendered
            await new Promise(resolve => setTimeout(resolve, 50));

            // Add empty assistant message that will be updated
            addMessage({
                content: '',
                role: 'assistant',
                timestamp: new Date(),
            });

            setIsStreaming(true);
            let fullResponse = '';

            // Start the streaming chat
            const stream = apiService.streamChat({ message });

            try {
                for await (const chunk of stream) {
                    fullResponse += chunk;
                    updateLastMessage(fullResponse);
                }
            } catch (error) {
                // Update the assistant message with error
                updateLastMessage('Sorry, I encountered an error processing your message.');
                throw error;
            } finally {
                setIsStreaming(false);
            }

            return fullResponse;
        },
        onError: (error) => {
            console.error('Chat error:', error);
            setIsStreaming(false);
        },
    });

    const resetChatMutation = useMutation({
        mutationFn: apiService.resetChat,
        onSuccess: () => {
            setMessages([]);
            queryClient.invalidateQueries({ queryKey: ['chat'] });
        },
    });

    const sendMessage = useCallback((message: string) => {
        if (message.trim() && !isStreaming) {
            sendMessageMutation.mutate(message.trim());
        }
    }, [sendMessageMutation, isStreaming]);

    const resetChat = useCallback(() => {
        resetChatMutation.mutate();
    }, [resetChatMutation]);

    return {
        messages,
        isStreaming,
        sendMessage,
        resetChat,
        isLoading: sendMessageMutation.isPending,
        error: sendMessageMutation.error,
        isResetting: resetChatMutation.isPending,
    };
};
