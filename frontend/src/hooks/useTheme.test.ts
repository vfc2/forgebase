import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { ThemeProvider } from '../providers/ThemeProvider';
import { useTheme } from './useTheme';
import React from 'react';

// Mock localStorage
const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
};

// Mock matchMedia
const matchMediaMock = vi.fn();

Object.defineProperty(window, 'localStorage', {
    value: localStorageMock
});

Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: matchMediaMock,
});

const wrapper = ({ children }: { children: React.ReactNode }) => 
    React.createElement(ThemeProvider, null, children);

describe('useTheme', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        matchMediaMock.mockReturnValue({
            matches: false,
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
        });
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('throws error when used outside ThemeProvider', () => {
        expect(() => {
            renderHook(() => useTheme());
        }).toThrow('useTheme must be used within a ThemeProvider');
    });

    it('initializes with light theme by default when no saved preference and system prefers light', () => {
        localStorageMock.getItem.mockReturnValue(null);
        matchMediaMock.mockReturnValue({
            matches: false, // System prefers light
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
        });

        const { result } = renderHook(() => useTheme(), { wrapper });
        
        expect(result.current.colorScheme).toBe('light');
    });

    it('initializes with dark theme when system prefers dark and no saved preference', () => {
        localStorageMock.getItem.mockReturnValue(null);
        matchMediaMock.mockReturnValue({
            matches: true, // System prefers dark
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
        });

        const { result } = renderHook(() => useTheme(), { wrapper });
        
        expect(result.current.colorScheme).toBe('dark');
    });

    it('uses saved preference when available', () => {
        localStorageMock.getItem.mockReturnValue('dark');
        matchMediaMock.mockReturnValue({
            matches: false, // System prefers light, but saved preference should take priority
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
        });

        const { result } = renderHook(() => useTheme(), { wrapper });
        
        expect(result.current.colorScheme).toBe('dark');
    });

    it('toggles between light and dark themes', () => {
        localStorageMock.getItem.mockReturnValue('light');
        matchMediaMock.mockReturnValue({
            matches: false,
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
        });

        const { result } = renderHook(() => useTheme(), { wrapper });
        
        expect(result.current.colorScheme).toBe('light');
        
        act(() => {
            result.current.toggleColorScheme();
        });
        
        expect(result.current.colorScheme).toBe('dark');
        expect(localStorageMock.setItem).toHaveBeenCalledWith('mantine-color-scheme', 'dark');
        
        act(() => {
            result.current.toggleColorScheme();
        });
        
        expect(result.current.colorScheme).toBe('light');
        expect(localStorageMock.setItem).toHaveBeenCalledWith('mantine-color-scheme', 'light');
    });

    it('sets up system theme change listeners', () => {
        const addEventListener = vi.fn();
        const removeEventListener = vi.fn();
        
        matchMediaMock.mockReturnValue({
            matches: false,
            addEventListener,
            removeEventListener,
        });

        const { unmount } = renderHook(() => useTheme(), { wrapper });
        
        expect(addEventListener).toHaveBeenCalledWith('change', expect.any(Function));
        
        unmount();
        
        expect(removeEventListener).toHaveBeenCalledWith('change', expect.any(Function));
    });
});
