import React, { useState } from 'react';
import { Group, Textarea, ActionIcon, Paper, Text, Box } from '@mantine/core';
import { IconSend, IconLoader } from '@tabler/icons-react';

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

    return (
        <Paper withBorder p="md" style={{ borderTop: '1px solid var(--mantine-color-gray-3)' }}>
            <Box maw={800} mx="auto">
                <form onSubmit={handleSubmit}>
                    <Group gap="sm" align="flex-end">
                        <Textarea
                            flex={1}
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={placeholder}
                            disabled={disabled}
                            autosize
                            minRows={1}
                            maxRows={4}
                        />
                        <ActionIcon
                            type="submit"
                            disabled={!message.trim() || disabled}
                            size="lg"
                            variant="filled"
                        >
                            {disabled ? (
                                <IconLoader size={16} className="animate-spin" />
                            ) : (
                                <IconSend size={16} />
                            )}
                        </ActionIcon>
                    </Group>
                </form>
                <Text size="xs" c="dimmed" mt="xs">
                    Press Enter to send, Shift+Enter for new line
                </Text>
            </Box>
        </Paper>
    );
};
