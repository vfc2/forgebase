import React, { useEffect, useRef } from 'react';
import { Box, Text, Center, Stack, Paper, Container, Group, ThemeIcon } from '@mantine/core';
import { IconSparkles, IconFileText, IconBulb, IconRocket } from '@tabler/icons-react';
import type { ChatMessage } from '../../types/api';
import { MessageBubble } from './MessageBubble';

interface MessageListProps {
    messages: ChatMessage[];
    isStreaming: boolean;
}

const ExamplePrompts = [
    {
        icon: IconFileText,
        title: "E-commerce Platform",
        description: "Create a PRD for a modern e-commerce platform with payment integration"
    },
    {
        icon: IconRocket,
        title: "Mobile App",
        description: "Design requirements for a social media mobile application"
    },
    {
        icon: IconBulb,
        title: "SaaS Dashboard",
        description: "Develop a comprehensive analytics dashboard for business users"
    }
];

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
            <Box style={{ flex: 1, overflowY: 'auto' }} p="md">
                <Container size="md" py="xl">
                    <Center>
                        <Stack align="center" gap="xl" maw={600}>
                            <Box ta="center">
                                <ThemeIcon
                                    size={80}
                                    radius="xl"
                                    variant="gradient"
                                    gradient={{ from: 'blue', to: 'cyan', deg: 45 }}
                                    mb="md"
                                >
                                    <IconSparkles size={40} />
                                </ThemeIcon>
                                <Text size="xl" fw={600} mb="xs">
                                    Welcome to ForgeBase
                                </Text>
                                <Text size="md" c="dimmed" mb="xl">
                                    I'll help you create comprehensive Product Requirements Documents (PRDs) 
                                    through conversational AI. Just describe your project and let's get started!
                                </Text>
                            </Box>

                            <Stack gap="md" w="100%">
                                <Text size="sm" fw={500} c="dimmed" ta="center">
                                    Try these examples to get started:
                                </Text>
                                
                                {ExamplePrompts.map((prompt, index) => (
                                    <Paper
                                        key={index}
                                        p="md"
                                        style={{ 
                                            cursor: 'pointer',
                                            backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-6))',
                                            borderColor: 'light-dark(#e8eaed, var(--mantine-color-dark-5))'
                                        }}
                                        withBorder
                                        className="hover-card"
                                    >
                                        <Group gap="md">
                                            <ThemeIcon size="lg" variant="light" color="blue">
                                                <prompt.icon size={20} />
                                            </ThemeIcon>
                                            <Box style={{ flex: 1 }}>
                                                <Text fw={500} size="sm" mb={4}>
                                                    {prompt.title}
                                                </Text>
                                                <Text size="xs" c="dimmed">
                                                    {prompt.description}
                                                </Text>
                                            </Box>
                                        </Group>
                                    </Paper>
                                ))}
                            </Stack>
                        </Stack>
                    </Center>
                </Container>
            </Box>
        );
    }

    return (
        <Box style={{ flex: 1, overflowY: 'auto' }} p="md">
            <Container size="lg">
                {messages.map((message, index) => (
                    <MessageBubble
                        key={message.id}
                        message={message}
                        messageIndex={index}
                        isStreaming={isStreaming && index === messages.length - 1 && message.role === 'assistant'}
                    />
                ))}
                <div ref={messagesEndRef} />
            </Container>
        </Box>
    );
};
