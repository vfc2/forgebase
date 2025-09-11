import React from 'react';
import { Box, Title, Text, Stack } from '@mantine/core';
import { IconFileText } from '@tabler/icons-react';
import { MarkdownPreview } from '../markdown/MarkdownPreview';
import type { Project } from '../../types/api';

interface PrdPreviewProps {
    project: Project | null;
    isLoading?: boolean;
}

export const PrdPreview: React.FC<PrdPreviewProps> = ({ project, isLoading = false }) => {
    // Loading state
    if (isLoading) {
        return (
            <Box style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Text c="dimmed">Loading PRD...</Text>
            </Box>
        );
    }

    // No project selected
    if (!project) {
        return (
            <Box style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Stack align="center" gap="md">
                    <IconFileText size={48} color="var(--mantine-color-gray-5)" />
                    <Box ta="center">
                        <Title order={3} size="md" mb="xs" c="dimmed">
                            No Project Selected
                        </Title>
                        <Text size="sm" c="dimmed">
                            Select a project to view its PRD
                        </Text>
                    </Box>
                </Stack>
            </Box>
        );
    }

    // Project selected but no PRD content
    if (!project.prd || project.prd.trim() === '') {
        return (
            <Box style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Stack align="center" gap="md">
                    <IconFileText size={48} color="var(--mantine-color-gray-5)" />
                    <Box ta="center">
                        <Title order={3} size="md" mb="xs" c="dimmed">
                            PRD Not Available
                        </Title>
                        <Text size="sm" c="dimmed">
                            Start a conversation to generate the PRD for "{project.name}"
                        </Text>
                    </Box>
                </Stack>
            </Box>
        );
    }

    // Render the PRD content using MarkdownPreview
    return <MarkdownPreview content={project.prd} />;
};
