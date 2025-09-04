import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { PrdPreview } from './PrdPreview';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('PrdPreview', () => {
    const mockProjectId = 'test-project-123';

    it('renders PRD content', () => {
        render(
            <TestWrapper>
                <PrdPreview projectId={mockProjectId} />
            </TestWrapper>
        );

        // Check for key headings from the mock PRD content
        expect(screen.getByText('Product Requirements Document')).toBeInTheDocument();
        expect(screen.getByText('Project Overview')).toBeInTheDocument();
        expect(screen.getByText('Executive Summary')).toBeInTheDocument();
        expect(screen.getByText('User Stories')).toBeInTheDocument();
        expect(screen.getByText('Technical Requirements')).toBeInTheDocument();
    });

    it('renders markdown content properly', () => {
        render(
            <TestWrapper>
                <PrdPreview projectId={mockProjectId} />
            </TestWrapper>
        );

        // Check for specific content sections
        expect(screen.getByText(/innovative e-commerce platform/)).toBeInTheDocument();
        expect(screen.getByText(/As a Customer/)).toBeInTheDocument();
        expect(screen.getByText(/Performance/)).toBeInTheDocument();
        expect(screen.getByText(/Page load times should be under 2 seconds/)).toBeInTheDocument();
    });

    it('has proper scroll container', () => {
        render(
            <TestWrapper>
                <PrdPreview projectId={mockProjectId} />
            </TestWrapper>
        );

        // The component should render without crashing and have proper structure
        const container = screen.getByText('Product Requirements Document').closest('[style*="height: 100%"]');
        expect(container).toBeInTheDocument();
    });
});