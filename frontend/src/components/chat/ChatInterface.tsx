import React from 'react';
import { Box, Group, Title, Button, Alert } from '@mantine/core';
import { IconAlertCircle, IconRefresh } from '@tabler/icons-react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
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
        <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Chat header with reset button */}
            <Group justify="space-between" p="md" style={{ borderBottom: '1px solid var(--mantine-color-gray-3)' }}>
                <Title order={2} size="lg">
                    Conversation
                </Title>
                <Button
                    variant="subtle"
                    size="sm"
                    leftSection={<IconRefresh size={16} />}
                    onClick={resetChat}
                    disabled={isResetting || messages.length === 0}
                    loading={isResetting}
                >
                    {isResetting ? 'Resetting...' : 'Reset Chat'}
                </Button>
            </Group>

            {/* Error display */}
            {error && (
                <Alert
                    icon={<IconAlertCircle size={16} />}
                    color="red"
                    m="md"
                    variant="light"
                >
                    {error instanceof Error ? error.message : 'An error occurred'}
                </Alert>
            )}

            {/* Messages */}
            <MessageList messages={messages} isStreaming={isStreaming} />

            {/* Input */}
            <MessageInput
                onSendMessage={sendMessage}
                disabled={isLoading || isStreaming}
                placeholder={isStreaming ? 'Please wait...' : 'Type your message...'}
            />
        </Box>
    );
};
