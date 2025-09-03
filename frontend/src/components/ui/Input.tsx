import React from 'react';
import { TextInput } from '@mantine/core';
import type { TextInputProps } from '@mantine/core';

interface InputProps extends Omit<TextInputProps, 'error'> {
    error?: string;
}

export const Input: React.FC<InputProps> = ({
    error,
    ...props
}) => {
    return (
        <TextInput
            error={error}
            {...props}
        />
    );
};
