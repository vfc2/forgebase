import React, { useState } from 'react';
import { Group, Textarea, ActionIcon, Paper, Text, Container, Loader } from '@mantine/core';
import { IconSend } from '@tabler/icons-react';

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
    const MAX_LEN = 2000;

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
        <Paper 
            p="md" 
            shadow="sm"
            style={{ 
                borderTop: '1px solid var(--mantine-color-gray-3)',
                backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-7))'
            }}
        >
            <Container size="lg">
                <form onSubmit={handleSubmit}>
                    <Group gap="sm" align="flex-end">
                        <Textarea
                            flex={1}
                            value={message}
                            onChange={(e) => setMessage(e.target.value.slice(0, MAX_LEN))}
                            onKeyDown={handleKeyDown}
                            placeholder={placeholder}
                            disabled={disabled}
                            autosize
                            minRows={1}
                            maxRows={4}
                            maxLength={MAX_LEN}
                            styles={{
                                input: {
                                    border: '1px solid var(--mantine-color-gray-4)',
                                    backgroundColor: 'light-dark(#fcfcfc, var(--mantine-color-dark-6))',
                                    fontSize: '14px',
                                    '&:focus': {
                                        borderColor: 'var(--mantine-color-blue-5)',
                                        boxShadow: '0 0 0 1px var(--mantine-color-blue-5)'
                                    }
                                }
                            }}
                        />
                        <ActionIcon
                            type="submit"
                            disabled={!message.trim() || disabled}
                            size="xl"
                            variant="gradient"
                            gradient={{ from: 'blue', to: 'cyan', deg: 45 }}
                            style={{ minWidth: '42px', minHeight: '42px' }}
                            aria-label={disabled ? 'Sending message' : 'Send message'}
                        >
                            {disabled ? <Loader size="sm" color="white" /> : <IconSend size={18} />}
                        </ActionIcon>
                    </Group>
                </form>
                <Group justify="space-between" mt="xs">
                    <Text size="xs" c="dimmed">
                        Press Enter to send, Shift+Enter for new line
                    </Text>
                    <Text size="xs" c="dimmed">
                        {message.length}/{MAX_LEN} characters
                    </Text>
                </Group>
            </Container>
        </Paper>
    );
};
