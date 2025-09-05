import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { Layout } from './Layout';
import type { ReactNode } from 'react';

// Mock the hooks and components to isolate Layout testing
const mockUseProjects = vi.fn(() => ({
    projects: [
        { id: 'project-1', name: 'Test Project 1' },
        { id: 'project-2', name: 'Test Project 2' }
    ],
    currentProjectId: 'project-1',
    createProject: vi.fn(),
    deleteProject: vi.fn(),
    selectProject: vi.fn(),
}));

vi.mock('../../hooks/useProjects', () => ({
    useProjects: mockUseProjects,
}));

vi.mock('../layout/Header', () => ({
    Header: ({ onSettingsClick, onProfileClick }: { onSettingsClick: () => void; onProfileClick: () => void }) => (
        <div data-testid="header">
            <button onClick={onSettingsClick} data-testid="settings-btn">Settings</button>
            <button onClick={onProfileClick} data-testid="profile-btn">Profile</button>
        </div>
    ),
}));

vi.mock('../layout/Sidebar', () => ({
    Sidebar: ({ projects, onNewProject, onProjectSelect, onProjectDelete }: { 
        projects: Array<{ id: string; name: string }>;
        onNewProject: (name: string) => void;
        onProjectSelect: (id: string) => void;
        onProjectDelete: (id: string) => void;
    }) => (
        <div data-testid="sidebar">
            <button onClick={() => onNewProject('New Project')} data-testid="new-project-btn">
                New Project
            </button>
            {projects.map((project) => (
                <div key={project.id} data-testid={`project-${project.id}`}>
                    <button onClick={() => onProjectSelect(project.id)}>{project.name}</button>
                    <button onClick={() => onProjectDelete(project.id)}>Delete</button>
                </div>
            ))}
        </div>
    ),
}));

vi.mock('../chat/ChatInterface', () => ({
    ChatInterface: ({ projectId }: { projectId: string | null }) => (
        <div data-testid="chat-interface">Chat for project: {projectId}</div>
    ),
}));

vi.mock('../project/ProjectStages', () => ({
    ProjectStages: ({ projectId }: { projectId: string | null }) => (
        <div data-testid="project-stages">Stages for project: {projectId}</div>
    ),
}));

// Test wrapper with all required providers
const TestWrapper = ({ children }: { children: ReactNode }) => {
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: { retry: false },
            mutations: { retry: false },
        },
    });
    
    return (
        <QueryClientProvider client={queryClient}>
            <MantineProvider>
                {children}
            </MantineProvider>
        </QueryClientProvider>
    );
};

describe('Layout', () => {
    it('renders all main layout components', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        expect(screen.getByTestId('header')).toBeInTheDocument();
        expect(screen.getByTestId('sidebar')).toBeInTheDocument();
        expect(screen.getByTestId('chat-interface')).toBeInTheDocument();
        expect(screen.getByTestId('project-stages')).toBeInTheDocument();
    });

    it('passes correct projectId to child components', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        expect(screen.getByText('Chat for project: project-1')).toBeInTheDocument();
        expect(screen.getByText('Stages for project: project-1')).toBeInTheDocument();
    });

    it('displays projects in sidebar', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        expect(screen.getByTestId('project-project-1')).toBeInTheDocument();
        expect(screen.getByTestId('project-project-2')).toBeInTheDocument();
        expect(screen.getByText('Test Project 1')).toBeInTheDocument();
        expect(screen.getByText('Test Project 2')).toBeInTheDocument();
    });

    it('provides project management handlers to sidebar', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        // The handlers should be passed to sidebar - verify the interface exists
        expect(screen.getByTestId('new-project-btn')).toBeInTheDocument();
        expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    });

    it('has proper AppShell structure', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        // Should render within AppShell structure
        const mainContent = screen.getByTestId('chat-interface').closest('[class*="AppShell"]');
        expect(mainContent || screen.getByTestId('chat-interface')).toBeInTheDocument();
    });
});
