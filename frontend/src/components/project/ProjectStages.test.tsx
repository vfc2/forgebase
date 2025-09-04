import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { ProjectStages } from './ProjectStages';

// Mock the child components
vi.mock('../chat/ChatInterface', () => ({
    ChatInterface: ({ projectId }: { projectId: string }) => (
        <div data-testid="chat-interface">Chat Interface for {projectId}</div>
    )
}));

vi.mock('./PrdPreview', () => ({
    PrdPreview: ({ projectId }: { projectId: string }) => (
        <div data-testid="prd-preview">PRD Preview for {projectId}</div>
    )
}));

vi.mock('./BacklogView', () => ({
    BacklogView: ({ projectId }: { projectId: string }) => (
        <div data-testid="backlog-view">Backlog View for {projectId}</div>
    )
}));

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('ProjectStages', () => {
    const mockProjectId = 'test-project-123';

    it('renders all three tabs', () => {
        render(
            <TestWrapper>
                <ProjectStages projectId={mockProjectId} />
            </TestWrapper>
        );

        // Check that all tabs are present
        expect(screen.getByRole('tab', { name: /chat/i })).toBeInTheDocument();
        expect(screen.getByRole('tab', { name: /prd/i })).toBeInTheDocument();
        expect(screen.getByRole('tab', { name: /backlog/i })).toBeInTheDocument();
    });

    it('starts with chat tab active by default', () => {
        render(
            <TestWrapper>
                <ProjectStages projectId={mockProjectId} />
            </TestWrapper>
        );

        // Chat tab should be selected by default
        const chatTab = screen.getByRole('tab', { name: /chat/i });
        expect(chatTab).toHaveAttribute('aria-selected', 'true');

        // Chat interface should be visible
        expect(screen.getByTestId('chat-interface')).toBeInTheDocument();
        expect(screen.getByText(`Chat Interface for ${mockProjectId}`)).toBeInTheDocument();
    });

    it('switches to PRD tab when clicked', () => {
        render(
            <TestWrapper>
                <ProjectStages projectId={mockProjectId} />
            </TestWrapper>
        );

        // Click on PRD tab
        const prdTab = screen.getByRole('tab', { name: /prd/i });
        fireEvent.click(prdTab);

        // PRD tab should be selected
        expect(prdTab).toHaveAttribute('aria-selected', 'true');

        // PRD preview should be visible
        expect(screen.getByTestId('prd-preview')).toBeInTheDocument();
        expect(screen.getByText(`PRD Preview for ${mockProjectId}`)).toBeInTheDocument();

        // Chat interface should not be visible
        expect(screen.queryByTestId('chat-interface')).not.toBeInTheDocument();
    });

    it('switches to Backlog tab when clicked', () => {
        render(
            <TestWrapper>
                <ProjectStages projectId={mockProjectId} />
            </TestWrapper>
        );

        // Click on Backlog tab
        const backlogTab = screen.getByRole('tab', { name: /backlog/i });
        fireEvent.click(backlogTab);

        // Backlog tab should be selected
        expect(backlogTab).toHaveAttribute('aria-selected', 'true');

        // Backlog view should be visible
        expect(screen.getByTestId('backlog-view')).toBeInTheDocument();
        expect(screen.getByText(`Backlog View for ${mockProjectId}`)).toBeInTheDocument();

        // Other components should not be visible
        expect(screen.queryByTestId('chat-interface')).not.toBeInTheDocument();
        expect(screen.queryByTestId('prd-preview')).not.toBeInTheDocument();
    });

    it('passes correct projectId to all child components', () => {
        render(
            <TestWrapper>
                <ProjectStages projectId={mockProjectId} />
            </TestWrapper>
        );

        // Check Chat tab (default)
        expect(screen.getByText(`Chat Interface for ${mockProjectId}`)).toBeInTheDocument();

        // Switch to PRD tab
        fireEvent.click(screen.getByRole('tab', { name: /prd/i }));
        expect(screen.getByText(`PRD Preview for ${mockProjectId}`)).toBeInTheDocument();

        // Switch to Backlog tab
        fireEvent.click(screen.getByRole('tab', { name: /backlog/i }));
        expect(screen.getByText(`Backlog View for ${mockProjectId}`)).toBeInTheDocument();
    });
});