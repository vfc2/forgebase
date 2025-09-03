import React from 'react';
import { Box, Alert, Container, Text, Center, Stack } from '@mantine/core';
import { IconAlertCircle, IconFolder } from '@tabler/icons-react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '../../hooks/useChat';
import type { ApiError } from '../../types/api';

interface ChatInterfaceProps {
    hasActiveProject: boolean;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ hasActiveProject }) => {
    const {
        messages,
        isStreaming,
        sendMessage,
        isLoading,
        error,
    } = useChat();

    const apiError = error as ApiError | null;

    // Show placeholder when no project is selected
    if (!hasActiveProject) {
        return (
            <Box style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Center>
                    <Stack align="center" gap="md">
                        <IconFolder size={48} color="var(--mantine-color-gray-6)" />
                        <Text size="lg" fw={500} c="var(--mantine-color-gray-7)">
                            No Project Selected
                        </Text>
                        <Text size="sm" c="var(--mantine-color-gray-6)" ta="center">
                            Please select or create a project from the sidebar to start chatting.
                        </Text>
                    </Stack>
                </Center>
            </Box>
        );
    }

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

            {/* Messages - scrollable area */}
            <Box style={{ 
                flex: 1, 
                minHeight: 0,  // Critical for flex items to shrink
                display: 'flex',
                flexDirection: 'column'
            }}>
                <MessageList messages={messages} isStreaming={isStreaming} onExampleClick={sendMessage} />
            </Box>

            {/* Input - fixed at bottom */}
            <MessageInput
                onSendMessage={sendMessage}
                disabled={isLoading || isStreaming}
                placeholder={isStreaming ? 'Please wait...' : 'Describe your project, features, or ask questions about PRDs...'}
            />
        </Box>
    );
};
