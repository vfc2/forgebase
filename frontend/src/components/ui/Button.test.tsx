import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { Button } from '../ui/Button';

describe('Button', () => {
    it('renders children correctly', () => {
        render(<Button>Click me</Button>);
        expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
    });

    it('handles click events', async () => {
        const user = userEvent.setup();
        const handleClick = vi.fn();

        render(<Button onClick={handleClick}>Click me</Button>);

        await user.click(screen.getByRole('button'));
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('applies primary variant styles by default', () => {
        render(<Button>Primary Button</Button>);
        const button = screen.getByRole('button');
        expect(button).toHaveClass('bg-primary-600');
    });

    it('applies secondary variant styles', () => {
        render(<Button variant="secondary">Secondary Button</Button>);
        const button = screen.getByRole('button');
        expect(button).toHaveClass('bg-gray-100');
    });

    it('applies ghost variant styles', () => {
        render(<Button variant="ghost">Ghost Button</Button>);
        const button = screen.getByRole('button');
        expect(button).toHaveClass('text-gray-700');
    });

    it('is disabled when disabled prop is true', () => {
        render(<Button disabled>Disabled Button</Button>);
        const button = screen.getByRole('button');
        expect(button).toBeDisabled();
        expect(button).toHaveClass('disabled:opacity-50');
    });

    it('applies custom className', () => {
        render(<Button className="custom-class">Custom Button</Button>);
        const button = screen.getByRole('button');
        expect(button).toHaveClass('custom-class');
    });
});
