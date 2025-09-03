import React from 'react';
import {
  AppShell,
  Group,
  Title,
  Badge,
  ActionIcon,
  Menu,
  Text,
  Avatar,
  Tooltip,
  Flex,
  Box
} from '@mantine/core';
import {
  IconSettings,
  IconUser,
  IconLogout,
  IconBrandGithub,
  IconHelp,
  IconSparkles,
  IconCode
} from '@tabler/icons-react';

interface HeaderProps {
  onSettingsClick?: () => void;
  onProfileClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onSettingsClick,
  onProfileClick
}) => {
  return (
    <AppShell.Header p="md">
      <Group justify="space-between" h="100%">
        {/* Left side - Logo and title */}
        <Group gap="lg">
          <Flex align="center" gap="sm">
            <Box
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '8px',
                padding: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <IconCode size={24} color="white" />
            </Box>
            <Box>
              <Title order={2} size="h3" style={{ lineHeight: 1 }}>
                ForgeBase
              </Title>
              <Text size="xs" c="dimmed" style={{ lineHeight: 1 }}>
                AI-Powered PRD Generation
              </Text>
            </Box>
          </Flex>
          
          <Badge
            variant="light"
            color="blue"
            leftSection={<IconSparkles size={12} />}
            size="sm"
          >
            Beta
          </Badge>
        </Group>

        {/* Right side - Actions and user menu */}
        <Group gap="sm">
          <Tooltip label="View on GitHub">
            <ActionIcon
              variant="subtle"
              color="gray"
              size="lg"
              component="a"
              href="https://github.com/your-org/forgebase"
              target="_blank"
            >
              <IconBrandGithub size={20} />
            </ActionIcon>
          </Tooltip>

          <Tooltip label="Help & Documentation">
            <ActionIcon variant="subtle" color="gray" size="lg">
              <IconHelp size={20} />
            </ActionIcon>
          </Tooltip>

          <Menu shadow="md" width={200} position="bottom-end">
            <Menu.Target>
              <ActionIcon variant="subtle" color="gray" size="lg">
                <Avatar size="sm" color="blue">
                  <IconUser size={16} />
                </Avatar>
              </ActionIcon>
            </Menu.Target>

            <Menu.Dropdown>
              <Menu.Label>Account</Menu.Label>
              <Menu.Item
                leftSection={<IconUser size={14} />}
                onClick={onProfileClick}
              >
                Profile
              </Menu.Item>
              <Menu.Item
                leftSection={<IconSettings size={14} />}
                onClick={onSettingsClick}
              >
                Settings
              </Menu.Item>
              
              <Menu.Divider />
              
              <Menu.Item
                leftSection={<IconLogout size={14} />}
                color="red"
              >
                Sign Out
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Group>
      </Group>
    </AppShell.Header>
  );
};
