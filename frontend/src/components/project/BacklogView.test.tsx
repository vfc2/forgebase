import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { BacklogView } from './BacklogView';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('BacklogView', () => {
    const mockProjectId = 'test-project-123';

    it('renders placeholder content', () => {
        render(
            <TestWrapper>
                <BacklogView projectId={mockProjectId} />
            </TestWrapper>
        );

        expect(screen.getByText('Backlog Coming Soon')).toBeInTheDocument();
        expect(screen.getByText(/The backlog view will help you track and prioritize/)).toBeInTheDocument();
    });

    it('has proper layout structure', () => {
        render(
            <TestWrapper>
                <BacklogView projectId={mockProjectId} />
            </TestWrapper>
        );

        // Check for the main content
        const heading = screen.getByText('Backlog Coming Soon');
        expect(heading).toBeInTheDocument();
        
        // Check for the icon (List icon should be present)
        const container = heading.closest('[style*="height: 100%"]');
        expect(container).toBeInTheDocument();
    });
});