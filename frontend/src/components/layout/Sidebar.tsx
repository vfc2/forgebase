import React from 'react';
import {
  AppShell,
  Stack,
  Button,
  Text,
  Divider,
  Group,
  ScrollArea,
  ActionIcon,
  Tooltip
} from '@mantine/core';
import {
  IconMessageCircle,
  IconPlus,
  IconTrash,
  IconDownload,
  IconSettings,
  IconBulb
} from '@tabler/icons-react';

interface SidebarProps {
  onNewChat: () => void;
  onClearHistory?: () => void;
  chatHistory?: Array<{ id: string; title: string; timestamp: Date }>;
  onChatSelect?: (chatId: string) => void;
  currentChatId?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  onNewChat,
  onClearHistory,
  chatHistory = [],
  onChatSelect,
  currentChatId
}) => {
  return (
    <AppShell.Navbar p="md">
      <AppShell.Section>
        <Button
          fullWidth
          leftSection={<IconPlus size={16} />}
          onClick={onNewChat}
          size="md"
          gradient={{ from: 'blue', to: 'cyan', deg: 45 }}
          variant="gradient"
        >
          New Conversation
        </Button>
      </AppShell.Section>

      <Divider my="md" />

      <AppShell.Section>
        <Group justify="space-between" mb="sm">
          <Text size="sm" fw={500} c="dimmed">
            Recent Conversations
          </Text>
          {chatHistory.length > 0 && (
            <Tooltip label="Clear History">
              <ActionIcon
                size="sm"
                variant="subtle"
                color="gray"
                onClick={onClearHistory}
              >
                <IconTrash size={14} />
              </ActionIcon>
            </Tooltip>
          )}
        </Group>
      </AppShell.Section>

      <AppShell.Section grow component={ScrollArea}>
        <Stack gap="xs">
          {chatHistory.length === 0 ? (
            <Text size="sm" c="dimmed" ta="center" py="lg">
              No conversations yet
            </Text>
          ) : (
            chatHistory.map((chat) => (
              <Button
                key={chat.id}
                variant={currentChatId === chat.id ? 'light' : 'subtle'}
                color={currentChatId === chat.id ? 'blue' : 'gray'}
                justify="flex-start"
                leftSection={<IconMessageCircle size={16} />}
                onClick={() => onChatSelect?.(chat.id)}
                style={{
                  height: 'auto',
                  padding: '8px 12px'
                }}
              >
                <div style={{ textAlign: 'left', width: '100%' }}>
                  <Text size="sm" fw={500} truncate>
                    {chat.title}
                  </Text>
                  <Text size="xs" c="dimmed">
                    {chat.timestamp.toLocaleDateString()}
                  </Text>
                </div>
              </Button>
            ))
          )}
        </Stack>
      </AppShell.Section>

      <Divider my="md" />

      <AppShell.Section>
        <Stack gap="xs">
          <Button
            variant="subtle"
            color="gray"
            justify="flex-start"
            leftSection={<IconBulb size={16} />}
            size="sm"
          >
            Tips & Examples
          </Button>
          
          <Button
            variant="subtle"
            color="gray"
            justify="flex-start"
            leftSection={<IconDownload size={16} />}
            size="sm"
          >
            Export Chat
          </Button>

          <Button
            variant="subtle"
            color="gray"
            justify="flex-start"
            leftSection={<IconSettings size={16} />}
            size="sm"
          >
            Preferences
          </Button>
        </Stack>
      </AppShell.Section>
    </AppShell.Navbar>
  );
};
