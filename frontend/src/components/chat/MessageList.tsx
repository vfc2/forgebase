import React, { useEffect, useRef } from 'react';
import { Box, Text, Center, Stack } from '@mantine/core';
import type { ChatMessage } from '../../types/api';
import { MessageBubble } from './MessageBubble';

interface MessageListProps {
    messages: ChatMessage[];
    isStreaming: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({
    messages,
    isStreaming
}) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isStreaming]);

    if (messages.length === 0) {
        return (
            <Center style={{ flex: 1 }}>
                <Stack align="center" gap="xs">
                    <Text size="lg" fw={500} c="dimmed">
                        Welcome to Forgebase Chat
                    </Text>
                    <Text size="sm" c="dimmed">
                        Start a conversation to generate PRDs and work plans
                    </Text>
                </Stack>
            </Center>
        );
    }

    return (
        <Box style={{ flex: 1, overflowY: 'auto' }} p="md">
            <Box maw={800} mx="auto">
                {messages.map((message, index) => (
                    <MessageBubble
                        key={message.id}
                        message={message}
                        isStreaming={isStreaming && index === messages.length - 1 && message.role === 'assistant'}
                    />
                ))}
                <div ref={messagesEndRef} />
            </Box>
        </Box>
    );
};
