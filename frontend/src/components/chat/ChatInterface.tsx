import React from 'react';
import { Box, Alert, Container } from '@mantine/core';
import { IconAlertCircle } from '@tabler/icons-react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '../../hooks/useChat';

export const ChatInterface: React.FC = () => {
    const {
        messages,
        isStreaming,
        sendMessage,
        isLoading,
        error,
    } = useChat();

    return (
        <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Error display */}
            {error && (
                <Container size="lg" px="md" pt="md">
                    <Alert
                        icon={<IconAlertCircle size={16} />}
                        color="red"
                        variant="light"
                    >
                        {error instanceof Error ? error.message : 'An error occurred'}
                    </Alert>
                </Container>
            )}

            {/* Messages */}
            <Box style={{ flex: 1, overflow: 'hidden' }}>
                <MessageList messages={messages} isStreaming={isStreaming} />
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
