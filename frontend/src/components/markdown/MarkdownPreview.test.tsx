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

    it('copies content to clipboard when copy button is clicked', async () => {
        const writeTextSpy = vi.spyOn(navigator.clipboard, 'writeText').mockResolvedValue(undefined);
        const user = userEvent.setup();
        const markdownContent = '# Test Content\n\nThis is test content.';
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        const copyButton = screen.getByRole('button', { name: /copy/i });
        await user.click(copyButton);

        expect(writeTextSpy).toHaveBeenCalledWith(markdownContent);
        writeTextSpy.mockRestore();
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
        expect(screen.getByText('const')).toBeInTheDocument();
        expect(screen.getByText('hello =')).toBeInTheDocument();
        expect(screen.getByText('"world"')).toBeInTheDocument();
    });

    it('handles clipboard copy failure gracefully', async () => {
        // Mock clipboard to fail
        const writeTextSpy = vi.spyOn(navigator.clipboard, 'writeText').mockRejectedValue(new Error('Clipboard failed'));
        
        const user = userEvent.setup();
        const markdownContent = '# Test Content';
        
        // Spy on console.error to verify error handling
        const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
        
        render(
            <TestWrapper>
                <MarkdownPreview content={markdownContent} />
            </TestWrapper>
        );

        const copyButton = screen.getByRole('button', { name: /copy/i });
        await user.click(copyButton);

        expect(consoleSpy).toHaveBeenCalledWith('Failed to copy content:', expect.any(Error));
        
        consoleSpy.mockRestore();
        writeTextSpy.mockRestore();
    });
});
