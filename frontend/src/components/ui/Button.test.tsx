import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider } from '@mantine/core';
import { Button } from '../ui/Button';

// Wrapper component for Mantine provider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>{children}</MantineProvider>
);

describe('Button', () => {
    it('renders children correctly', () => {
        render(
            <TestWrapper>
                <Button>Click me</Button>
            </TestWrapper>
        );
        expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
    });

    it('handles click events', async () => {
        const user = userEvent.setup();
        const handleClick = vi.fn();

        render(
            <TestWrapper>
                <Button onClick={handleClick}>Click me</Button>
            </TestWrapper>
        );

        await user.click(screen.getByRole('button'));
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('renders with primary variant by default', () => {
        render(
            <TestWrapper>
                <Button>Primary Button</Button>
            </TestWrapper>
        );
        const button = screen.getByRole('button');
        expect(button).toBeInTheDocument();
    });

    it('renders with secondary variant', () => {
        render(
            <TestWrapper>
                <Button variant="secondary">Secondary Button</Button>
            </TestWrapper>
        );
        const button = screen.getByRole('button');
        expect(button).toBeInTheDocument();
    });

    it('renders with ghost variant', () => {
        render(
            <TestWrapper>
                <Button variant="ghost">Ghost Button</Button>
            </TestWrapper>
        );
        const button = screen.getByRole('button');
        expect(button).toBeInTheDocument();
    });

    it('is disabled when disabled prop is true', () => {
        render(
            <TestWrapper>
                <Button disabled>Disabled Button</Button>
            </TestWrapper>
        );
        const button = screen.getByRole('button');
        expect(button).toBeDisabled();
    });

    it('accepts additional props', () => {
        render(
            <TestWrapper>
                <Button data-testid="custom-button">Custom Button</Button>
            </TestWrapper>
        );
        const button = screen.getByTestId('custom-button');
        expect(button).toBeInTheDocument();
    });
});
