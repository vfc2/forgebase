import React from 'react';
import { Group, Avatar, Paper, Text, Box } from '@mantine/core';
import { IconUser, IconRobot } from '@tabler/icons-react';
import type { ChatMessage } from '../../types/api';

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
        <Box mb="md">
            <Group
                align="flex-start"
                gap="sm"
                justify={isUser ? 'flex-end' : 'flex-start'}
                wrap="nowrap"
            >
                {!isUser && (
                    <Avatar color="gray" radius="xl" size="sm">
                        <IconRobot size={16} />
                    </Avatar>
                )}

                <Paper
                    p="sm"
                    radius="md"
                    bg={isUser ? 'blue' : 'gray.0'}
                    c={isUser ? 'white' : 'dark'}
                    maw="80%"
                    withBorder={!isUser}
                >
                    <Text size="sm" style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                        {message.content}
                        {isStreaming && (
                            <Text
                                component="span"
                                display="inline-block"
                                w={2}
                                h={16}
                                ml={2}
                                bg="currentColor"
                                style={{ animation: 'pulse 1s ease-in-out infinite' }}
                            />
                        )}
                    </Text>
                    <Text
                        size="xs"
                        mt={2}
                        opacity={0.7}
                        c={isUser ? 'blue.1' : 'dimmed'}
                    >
                        {message.timestamp.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </Text>
                </Paper>

                {isUser && (
                    <Avatar color="blue" radius="xl" size="sm">
                        <IconUser size={16} />
                    </Avatar>
                )}
            </Group>
        </Box>
    );
};
