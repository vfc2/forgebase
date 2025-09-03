import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import { Paper, Group, Title, Button, Text, Box } from '@mantine/core';
import { IconCopy, IconCheck } from '@tabler/icons-react';

interface MarkdownPreviewProps {
    content?: string;
}

export const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ content }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        if (content) {
            try {
                await navigator.clipboard.writeText(content);
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
            } catch (err) {
                console.error('Failed to copy content:', err);
            }
        }
    };

    if (!content) {
        return (
            <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Paper p="md" style={{ borderBottom: '1px solid var(--mantine-color-gray-3)' }}>
                    <Title order={2} size="lg">
                        Markdown Preview
                    </Title>
                </Paper>
                <Box style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Box ta="center">
                        <Title order={3} size="md" mb="xs" c="dimmed">
                            No content to preview
                        </Title>
                        <Text size="sm" c="dimmed">
                            Markdown content will appear here when available
                        </Text>
                    </Box>
                </Box>
            </Box>
        );
    }

    return (
        <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Header with copy button */}
            <Paper p="md" style={{ borderBottom: '1px solid var(--mantine-color-gray-3)' }}>
                <Group justify="space-between" align="center">
                    <Title order={2} size="lg">
                        Markdown Preview
                    </Title>
                    <Button
                        variant="subtle"
                        size="sm"
                        leftSection={copied ? <IconCheck size={16} /> : <IconCopy size={16} />}
                        onClick={handleCopy}
                        disabled={!content}
                    >
                        {copied ? 'Copied!' : 'Copy'}
                    </Button>
                </Group>
            </Paper>

            {/* Markdown content */}
            <Box style={{ flex: 1, overflowY: 'auto' }} p="md">
                <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-primary-600 prose-code:text-primary-600 prose-pre:bg-gray-50">
                    <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
                        {content}
                    </ReactMarkdown>
                </div>
            </Box>
        </Box>
    );
};
