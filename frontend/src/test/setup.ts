import '@testing-library/jest-dom';
import { beforeEach, vi } from 'vitest';

// Mock ResizeObserver for Mantine components
Object.defineProperty(globalThis, 'ResizeObserver', {
    value: vi.fn().mockImplementation(() => ({
        observe: vi.fn(),
        unobserve: vi.fn(),
        disconnect: vi.fn(),
    })),
    writable: true,
});

// Mock scrollIntoView for MessageList component
Object.defineProperty(Element.prototype, 'scrollIntoView', {
    value: vi.fn(),
    writable: true,
});

// Mock environment variables
Object.defineProperty(import.meta, 'env', {
    value: {
        VITE_API_URL: 'http://localhost:8000',
    },
    writable: true,
});

// Mock fetch for tests
globalThis.fetch = vi.fn();

// Mock matchMedia for Mantine
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(), // deprecated
        removeListener: vi.fn(), // deprecated
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
    })),
});

// Mock clipboard API
Object.assign(navigator, {
    clipboard: {
        writeText: vi.fn(),
    },
});

// Clean up mocks between tests
beforeEach(() => {
    vi.clearAllMocks();
});
