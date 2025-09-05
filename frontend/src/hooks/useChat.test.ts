import { renderHook, act } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useChat } from './useChat';
import { apiService } from '../services/api';
import type { Mock } from 'vitest';
import type { ReactNode } from 'react';

vi.mock('../services/api', () => ({
  apiService: {
    streamChat: vi.fn(),
    resetChat: vi.fn().mockResolvedValue(undefined)
  }
}));

// Test wrapper with QueryClient
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
  
  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useChat', () => {
  it('sanity executes test runner', () => {
    expect(1).toBe(1);
  });
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('adds user and streaming assistant messages then accumulates', async () => {
    const streamMock = apiService.streamChat as unknown as Mock;
    streamMock.mockImplementation(async function* () {
      yield 'Hello';
      yield ' world';
    });

    const { result } = renderHook(() => useChat({ projectId: 'p1' }));

    act(() => {
      result.current.sendMessage('Hi');
    });

  // Allow async generator to run
  await Promise.resolve();
  await Promise.resolve();

    // After streaming complete, last assistant message should contain full concatenated text
    const messages = result.current.messages;
    expect(messages.length).toBe(2);
    expect(messages[0].role).toBe('user');
    expect(messages[1].role).toBe('assistant');
    expect(messages[1].content).toBe('Hello world');
  });

  it('ignores a second send while streaming is in progress', async () => {
    (apiService.streamChat as unknown as Mock).mockImplementation(async function* () {
      yield 'Partial';
      await new Promise(r => setTimeout(r, 25));
    });
    const { result } = renderHook(() => useChat({ projectId: 'p1' }));
    act(() => { result.current.sendMessage('First'); });
    act(() => { result.current.sendMessage('Second'); });
    await new Promise(r => setTimeout(r, 5));
    const msgs = result.current.messages;
    expect(msgs.filter(m => m.role === 'user').length).toBe(1);
    expect(msgs.at(-1)?.content).toBe('Partial');
  });

  it('resetChat clears project messages', async () => {
    (apiService.streamChat as unknown as Mock).mockImplementation(async function* () { yield 'Hi'; });
    const { result } = renderHook(() => useChat({ projectId: 'p1' }));
    act(() => { result.current.sendMessage('Go'); });
  await new Promise(r => setTimeout(r, 1));
  expect(result.current.messages.length).toBe(2);
    await act(async () => { result.current.resetChat(); });
    expect(result.current.messages.length).toBe(0);
  });
});