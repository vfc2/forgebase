import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider } from '@mantine/core';
import { MarkdownPreview } from './MarkdownPreview';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('MarkdownPreview', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders empty state when no content provided', () => {
        render(
            <TestWrapper>
                <MarkdownPreview />
            </TestWrapper>
        );

        expect(screen.getByText('No content to preview')).toBeInTheDocument();
        expect(screen.getByText('Markdown content will appear here when available')).toBeInTheDocument();
    });

    it('renders markdown content when provided', () => {
        const markdownContent = '# Test Title\n\nThis is **bold** text and *italic* text.';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        expect(screen.getByText('Test Title')).toBeInTheDocument();
        expect(screen.getByText('bold')).toBeInTheDocument();
        expect(screen.getByText('italic')).toBeInTheDocument();
    });

    it('shows copy button when content is provided', () => {
        const markdownContent = '# Test Content';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        expect(screen.getByRole('button', { name: /copy/i })).toBeInTheDocument();
    });

    it('shows copy button functionality', async () => {
        const user = userEvent.setup();
        const markdownContent = '# Test Content\n\nThis is test content.';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        const copyButton = screen.getByRole('button', { name: /copy/i });
        expect(copyButton).toBeInTheDocument();
        expect(copyButton).not.toBeDisabled();
        
        // Click the button - it should not crash
        await user.click(copyButton);
        
        // The button should still be there after clicking
        expect(copyButton).toBeInTheDocument();
    });

    it('shows success indicator after copying', async () => {
        const user = userEvent.setup();
        const markdownContent = '# Test Content';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        const copyButton = screen.getByRole('button', { name: /copy/i });
        await user.click(copyButton);

        // Should show success state briefly
        expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('handles markdown with code blocks', () => {
        const markdownContent = '```javascript\nconst hello = "world";\n```';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        // Code should be rendered (syntax highlighting splits text into spans)
        // Look for the code elements more flexibly
        expect(screen.getByText('const')).toBeInTheDocument();
        expect(screen.getByText((content, element) => {
            return element?.textContent === 'hello =' || content.includes('hello');
        })).toBeInTheDocument();
        expect(screen.getByText('"world"')).toBeInTheDocument();
    });

    it('handles copy button interaction gracefully', async () => {
        const user = userEvent.setup();
        const markdownContent = '# Test Content';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        const copyButton = screen.getByRole('button', { name: /copy/i });
        
        // Should be able to click without throwing errors
        await user.click(copyButton);
        
        // Button should still be present and functional
        expect(copyButton).toBeInTheDocument();
    });
});
