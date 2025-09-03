import { useState, useCallback, useRef, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api';
import type { ChatMessage } from '../types/api';

interface UseChatProps {
    projectId: string | null;
}

export const useChat = ({ projectId }: UseChatProps) => {
    // Store chat histories for each project
    const [projectChats, setProjectChats] = useState<Record<string, ChatMessage[]>>({});
    const [isStreaming, setIsStreaming] = useState(false);
    const controllerRef = useRef<AbortController | null>(null);
    const queryClient = useQueryClient();

    // Get messages for current project
    const messages = projectId ? (projectChats[projectId] || []) : [];

    const generateId = () => `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const addMessage = useCallback((message: Omit<ChatMessage, 'id'>) => {
        if (!projectId) return null;
        
        const newMessage: ChatMessage = {
            ...message,
            id: generateId(),
        };
        
        setProjectChats(prev => ({
            ...prev,
            [projectId]: [...(prev[projectId] || []), newMessage]
        }));
        
        return newMessage;
    }, [projectId]);

    const updateLastMessage = useCallback((content: string) => {
        if (!projectId) return;
        
        setProjectChats(prev => {
            const currentMessages = prev[projectId] || [];
            if (currentMessages.length === 0) return prev;
            
            const lastMessage = currentMessages[currentMessages.length - 1];
            if (lastMessage.role !== 'assistant') return prev;

            return {
                ...prev,
                [projectId]: [
                    ...currentMessages.slice(0, -1),
                    { ...lastMessage, content }
                ]
            };
        });
    }, [projectId]);

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

            // Cancel any in-flight request before starting a new one
            controllerRef.current?.abort();
            controllerRef.current = new AbortController();
            // Start the streaming chat
            const stream = apiService.streamChat({ message }, controllerRef.current.signal);

            try {
                for await (const chunk of stream) {
                    fullResponse += chunk;
                    updateLastMessage(fullResponse);
                }
            } catch (error) {
                // On abort, do not treat as error; otherwise rethrow
                const isAbortError = typeof error === 'object' && error !== null && 'name' in error && (error as { name?: string }).name === 'AbortError';
                if (!isAbortError) {
                    // keep assistant bubble but don't inject apology text
                    throw error;
                }
            } finally {
                setIsStreaming(false);
                controllerRef.current = null;
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
            if (projectId) {
                setProjectChats(prev => ({
                    ...prev,
                    [projectId]: []
                }));
            }
            queryClient.invalidateQueries({ queryKey: ['chat'] });
        },
    });

    const sendMessage = useCallback((message: string) => {
        if (message.trim() && !isStreaming && projectId) {
            sendMessageMutation.mutate(message.trim());
        }
    }, [sendMessageMutation, isStreaming, projectId]);

    const resetChat = useCallback(() => {
        if (projectId) {
            resetChatMutation.mutate();
        }
    }, [resetChatMutation, projectId]);

    // Abort on unmount
    useEffect(() => {
        return () => controllerRef.current?.abort();
    }, []);

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
