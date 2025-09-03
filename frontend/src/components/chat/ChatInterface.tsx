import React from 'react';
import { Box, Alert, Container } from '@mantine/core';
import { IconAlertCircle } from '@tabler/icons-react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '../../hooks/useChat';
import type { ApiError } from '../../types/api';

export const ChatInterface: React.FC = () => {
    const {
        messages,
        isStreaming,
        sendMessage,
        isLoading,
        error,
    } = useChat();

    const apiError = error as ApiError | null;

    return (
        <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Error display */}
            {apiError && (
                <Container size="lg" px="md" pt="md">
                    <Alert
                        icon={<IconAlertCircle size={16} />}
                        color="red"
                        variant="light"
                    >
                        {apiError.detail || 'An error occurred'}
                    </Alert>
                </Container>
            )}

            {/* Messages */}
            <Box style={{ flex: 1, overflow: 'hidden' }}>
                <MessageList messages={messages} isStreaming={isStreaming} onExampleClick={sendMessage} />
            </Box>

            {/* Input */}
            <MessageInput
                onSendMessage={sendMessage}
                disabled={isLoading || isStreaming}
                placeholder={isStreaming ? 'Please wait...' : 'Describe your project, features, or ask questions about PRDs...'}
            />
        </Box>
    );
};
