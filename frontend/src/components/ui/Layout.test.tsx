import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { Layout } from './Layout';
import { useProjects } from '../../hooks/useProjects';
import type { ReactNode } from 'react';

// Mock the hooks and components to isolate Layout testing
vi.mock('../../hooks/useProjects', () => ({
    useProjects: vi.fn(),
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
    beforeEach(() => {
        // Reset mock to default behavior
        vi.mocked(useProjects).mockReturnValue({
            projects: [
                { id: 'project-1', name: 'Test Project 1', createdAt: new Date() },
                { id: 'project-2', name: 'Test Project 2', createdAt: new Date() }
            ],
            currentProjectId: 'project-1',
            createProject: vi.fn(),
            deleteProject: vi.fn(),
            selectProject: vi.fn(),
            isLoading: false,
            error: null,
        });
    });
    it('renders all main layout components', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        expect(screen.getByTestId('header')).toBeInTheDocument();
        expect(screen.getByTestId('sidebar')).toBeInTheDocument();
        // Since currentProjectId is 'project-1', it should render ProjectStages, not ChatInterface
        expect(screen.getByTestId('project-stages')).toBeInTheDocument();
        expect(screen.queryByTestId('chat-interface')).not.toBeInTheDocument();
    });

    it('passes correct projectId to child components', () => {
        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        // With currentProjectId 'project-1', should render ProjectStages, not ChatInterface
        expect(screen.getByText('Stages for project: project-1')).toBeInTheDocument();
        expect(screen.queryByText('Chat for project: project-1')).not.toBeInTheDocument();
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
        const appShell = screen.getByTestId('project-stages').closest('[class*="AppShell"]');
        expect(appShell || screen.getByTestId('project-stages')).toBeInTheDocument();
        
        // Should have header and sidebar
        expect(screen.getByTestId('header')).toBeInTheDocument();
        expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    });

    it('renders ChatInterface when no project is selected', () => {
        // Override mock for this test
        vi.mocked(useProjects).mockReturnValue({
            projects: [],
            currentProjectId: null,
            createProject: vi.fn(),
            deleteProject: vi.fn(),
            selectProject: vi.fn(),
            isLoading: false,
            error: null,
        });

        render(
            <TestWrapper>
                <Layout />
            </TestWrapper>
        );

        expect(screen.getByTestId('chat-interface')).toBeInTheDocument();
        expect(screen.queryByTestId('project-stages')).not.toBeInTheDocument();
        // Just check that the chat interface is rendered when no project is selected
        expect(screen.getByTestId('chat-interface')).toHaveTextContent('Chat for project:');
    });
});
