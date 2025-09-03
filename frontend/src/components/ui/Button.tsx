import React from 'react';
import { Button as MantineButton } from '@mantine/core';
import type { ButtonProps as MantineButtonProps } from '@mantine/core';

export interface ButtonProps extends Omit<MantineButtonProps, 'variant' | 'size'> {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    children: React.ReactNode;
    onClick?: React.MouseEventHandler<HTMLButtonElement>;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'md',
    children,
    ...props
}) => {
    // Map our custom variants to Mantine variants
    const mantineVariant = {
        primary: 'filled',
        secondary: 'outline',
        ghost: 'subtle',
    }[variant] as MantineButtonProps['variant'];

    // Map our sizes to Mantine sizes
    const mantineSize = {
        sm: 'sm',
        md: 'md',
        lg: 'lg',
    }[size] as MantineButtonProps['size'];

    return (
        <MantineButton
            variant={mantineVariant}
            size={mantineSize}
            {...props}
        >
            {children}
        </MantineButton>
    );
};
