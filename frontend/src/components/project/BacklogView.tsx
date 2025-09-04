import React from 'react';
import { Box, Container, Center, Stack, Text, ThemeIcon } from '@mantine/core';
import { IconList } from '@tabler/icons-react';

interface BacklogViewProps {
    projectId: string;
}

export const BacklogView: React.FC<BacklogViewProps> = () => {
    return (
        <Box style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Container size="sm">
                <Center>
                    <Stack align="center" gap="md">
                        <ThemeIcon
                            size={80}
                            radius="xl"
                            variant="gradient"
                            gradient={{ from: 'orange', to: 'red', deg: 45 }}
                        >
                            <IconList size={40} />
                        </ThemeIcon>
                        <Text size="xl" fw={600} ta="center">
                            Backlog Coming Soon
                        </Text>
                        <Text size="md" c="dimmed" ta="center" maw={400}>
                            The backlog view will help you track and prioritize features, 
                            user stories, and development tasks for your project.
                        </Text>
                    </Stack>
                </Center>
            </Container>
        </Box>
    );
};
