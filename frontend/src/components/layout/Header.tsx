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
  IconSun,
  IconMoon
} from '@tabler/icons-react';
import { useTheme } from '../../hooks/useTheme';

interface HeaderProps {
  onSettingsClick?: () => void;
  onProfileClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onSettingsClick,
  onProfileClick
}) => {
  const { colorScheme, toggleColorScheme } = useTheme();

  return (
    <AppShell.Header p="md">
      <Group justify="space-between" h="100%">
        {/* Left side - Logo and title */}
        <Group gap="lg">
          <Flex align="center" gap="sm">
            {/* Microsoft Logo */}
            <Box
              style={{
                width: 32,
                height: 32,
                display: 'flex',
                flexWrap: 'wrap',
                gap: 2,
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Box style={{ width: 14, height: 14, backgroundColor: '#F25022', borderRadius: 1 }} />
              <Box style={{ width: 14, height: 14, backgroundColor: '#7FBA00', borderRadius: 1 }} />
              <Box style={{ width: 14, height: 14, backgroundColor: '#00A4EF', borderRadius: 1 }} />
              <Box style={{ width: 14, height: 14, backgroundColor: '#FFB900', borderRadius: 1 }} />
            </Box>
            <Box>
              <Title order={2} size="h3" style={{ lineHeight: 1 }}>
                forgebase
              </Title>
              <Text size="xs" c="var(--mantine-color-text)" style={{ lineHeight: 2 }}>
                Microsoft Hackaton 2025
              </Text>
            </Box>
          </Flex>

          <Badge
            variant="light"
            color="blue"
            leftSection={<IconSparkles size={12} />}
            size="sm"
          >
            Alpha
          </Badge>
        </Group>

        {/* Right side - Actions and user menu */}
        <Group gap="sm">
          <Tooltip label={colorScheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
            <ActionIcon
              variant="subtle"
              color="gray"
              size="lg"
              onClick={toggleColorScheme}
              aria-label={colorScheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {colorScheme === 'dark' ? <IconSun size={20} /> : <IconMoon size={20} />}
            </ActionIcon>
          </Tooltip>

          <Tooltip label="View on GitHub">
            <ActionIcon
              variant="subtle"
              color="gray"
              size="lg"
              component="a"
              href="https://github.com/vfc2/forgebase"
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
              <ActionIcon variant="subtle" color="gray" size="lg" aria-label="Account menu">
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
