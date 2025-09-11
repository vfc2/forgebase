import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { PrdPreview } from './PrdPreview';
import type { Project } from '../../types/api';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('PrdPreview', () => {
    const mockProject: Project = {
        id: 'test-project-123',
        name: 'Test Project',
        prd: '# Product Requirements Document\n\n## Project Overview\n\nThis is a comprehensive Product Requirements Document for our innovative e-commerce platform.\n\n## User Stories\n\n**As a Customer**\n- I want to browse products easily\n\n## Technical Requirements\n\n**Performance**\n- Page load times should be under 2 seconds',
        createdAt: new Date(),
        updatedAt: new Date(),
    };

    it('renders PRD content when project has PRD', () => {
        render(
            <TestWrapper>
                <PrdPreview project={mockProject} />
            </TestWrapper>
        );

        // Check for content rendered by MarkdownPreview
        expect(screen.getByText('Product Requirements Document')).toBeInTheDocument();
        expect(screen.getByText('Project Overview')).toBeInTheDocument();
        expect(screen.getByText(/innovative e-commerce platform/)).toBeInTheDocument();
    });

    it('shows empty state when project has no PRD', () => {
        const projectWithoutPrd = { ...mockProject, prd: '' };
        render(
            <TestWrapper>
                <PrdPreview project={projectWithoutPrd} />
            </TestWrapper>
        );

        expect(screen.getByText('PRD Not Available')).toBeInTheDocument();
        expect(screen.getByText(/Start a conversation to generate the PRD/)).toBeInTheDocument();
    });

    it('shows loading state', () => {
        render(
            <TestWrapper>
                <PrdPreview project={null} isLoading={true} />
            </TestWrapper>
        );

        expect(screen.getByText('Loading PRD...')).toBeInTheDocument();
    });

    it('shows no project selected state', () => {
        render(
            <TestWrapper>
                <PrdPreview project={null} />
            </TestWrapper>
        );

        expect(screen.getByText('No Project Selected')).toBeInTheDocument();
        expect(screen.getByText('Select a project to view its PRD')).toBeInTheDocument();
    });
});