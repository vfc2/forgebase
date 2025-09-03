import React, { useState } from 'react';
import {
  AppShell,
  Stack,
  Button,
  Text,
  Divider,
  Group,
  ScrollArea,
  ActionIcon,
  Tooltip,
  Modal,
  TextInput,
  Menu,
  rem
} from '@mantine/core';
import {
  IconFolder,
  IconPlus,
  IconTrash,
  IconDownload,
  IconSettings,
  IconBulb,
  IconDots
} from '@tabler/icons-react';
import type { Project } from '../../types/api';

interface SidebarProps {
  onNewProject: (name: string) => void;
  onClearProjects?: () => void;
  projects?: Project[];
  onProjectSelect?: (projectId: string) => void;
  onProjectDelete?: (projectId: string) => void;
  currentProjectId?: string | null;
}

export const Sidebar: React.FC<SidebarProps> = ({
  onNewProject,
  onClearProjects,
  projects = [],
  onProjectSelect,
  onProjectDelete,
  currentProjectId
}) => {
  const [isNewProjectModalOpen, setIsNewProjectModalOpen] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [deleteConfirmProjectId, setDeleteConfirmProjectId] = useState<string | null>(null);

  const handleCreateProject = () => {
    if (projectName.trim()) {
      onNewProject(projectName);
      setProjectName('');
      setIsNewProjectModalOpen(false);
    }
  };

  const handleDeleteProject = (projectId: string) => {
    onProjectDelete?.(projectId);
    setDeleteConfirmProjectId(null);
  };

  const confirmDelete = (projectId: string) => {
    setDeleteConfirmProjectId(projectId);
  };
  return (
    <>
      <AppShell.Navbar p="md">
        <AppShell.Section>
          <Button
            fullWidth
            leftSection={<IconPlus size={16} />}
            onClick={() => setIsNewProjectModalOpen(true)}
            size="md"
            gradient={{ from: 'blue', to: 'cyan', deg: 45 }}
            variant="gradient"
          >
            New Project
          </Button>
        </AppShell.Section>

        <Divider my="md" />

        <AppShell.Section>
          <Group justify="space-between" mb="sm">
            <Text size="sm" fw={500} c="var(--mantine-color-text)">
              Recent Projects
            </Text>
            {projects.length > 0 && (
              <Tooltip label="Clear Projects">
                <ActionIcon
                  size="sm"
                  variant="subtle"
                  color="gray"
                  onClick={onClearProjects}
                  aria-label="Clear Projects"
                >
                  <IconTrash size={14} />
                </ActionIcon>
              </Tooltip>
            )}
          </Group>
        </AppShell.Section>

        <AppShell.Section grow component={ScrollArea}>
          <Stack gap="xs">
            {projects.length === 0 ? (
              <Text size="sm" c="var(--mantine-color-text)" ta="center" py="lg">
                No projects yet
              </Text>
            ) : (
              projects.map((project) => (
                <Group key={project.id} gap="xs" wrap="nowrap">
                  <Button
                    variant={currentProjectId === project.id ? 'light' : 'subtle'}
                    color={currentProjectId === project.id ? 'blue' : 'gray'}
                    justify="flex-start"
                    leftSection={<IconFolder size={16} />}
                    onClick={() => onProjectSelect?.(project.id)}
                    style={{
                      height: 'auto',
                      padding: '8px 12px',
                      flex: 1
                    }}
                  >
                    <div style={{ textAlign: 'left', width: '100%' }}>
                      <Text size="sm" fw={500} truncate>
                        {project.name}
                      </Text>
                      <Text size="xs" c="var(--mantine-color-text)">
                        {project.createdAt.toLocaleDateString()}
                      </Text>
                    </div>
                  </Button>
                  <Menu shadow="md" width={200}>
                    <Menu.Target>
                      <ActionIcon
                        size="sm"
                        variant="subtle"
                        color="gray"
                        aria-label={`Project options for ${project.name}`}
                      >
                        <IconDots size={16} />
                      </ActionIcon>
                    </Menu.Target>
                    <Menu.Dropdown>
                      <Menu.Item
                        color="red"
                        leftSection={<IconTrash style={{ width: rem(14), height: rem(14) }} />}
                        onClick={() => confirmDelete(project.id)}
                      >
                        Delete Project
                      </Menu.Item>
                    </Menu.Dropdown>
                  </Menu>
                </Group>
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
              Export Project
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

      {/* New Project Modal */}
      <Modal
        opened={isNewProjectModalOpen}
        onClose={() => {
          setIsNewProjectModalOpen(false);
          setProjectName('');
        }}
        title="Create New Project"
        centered
      >
        <Stack gap="md">
          <TextInput
            label="Project Name"
            placeholder="Enter project name..."
            value={projectName}
            onChange={(event) => setProjectName(event.currentTarget.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                handleCreateProject();
              }
            }}
            data-autofocus
          />
          <Group justify="flex-end" gap="sm">
            <Button
              variant="subtle"
              onClick={() => {
                setIsNewProjectModalOpen(false);
                setProjectName('');
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateProject}
              disabled={!projectName.trim()}
            >
              Create Project
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        opened={deleteConfirmProjectId !== null}
        onClose={() => setDeleteConfirmProjectId(null)}
        title="Delete Project"
        centered
      >
        <Stack gap="md">
          <Text>
            Are you sure you want to delete this project? This action cannot be undone.
          </Text>
          <Group justify="flex-end" gap="sm">
            <Button
              variant="subtle"
              onClick={() => setDeleteConfirmProjectId(null)}
            >
              Cancel
            </Button>
            <Button
              color="red"
              onClick={() => deleteConfirmProjectId && handleDeleteProject(deleteConfirmProjectId)}
            >
              Delete
            </Button>
          </Group>
        </Stack>
      </Modal>
    </>
  );
};
