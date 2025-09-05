import { describe, it, expect, beforeEach, vi } from 'vitest';
import { apiService } from '../services/api';

// Mock fetch globally
const mockFetch = vi.fn();
globalThis.fetch = mockFetch as unknown as typeof fetch;

describe('ApiService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('healthCheck', () => {
        it('makes a GET request to /health', async () => {
            const mockResponse = { status: 'ok' };
            mockFetch.mockResolvedValueOnce({
                ok: true,
                status: 200,
                json: async () => mockResponse,
            });
            const result = await apiService.healthCheck();
            expect(result).toEqual(mockResponse);
            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/health',
                expect.objectContaining({ headers: expect.any(Object) })
            );
        });
    });

    describe('resetChat', () => {
        it('makes a POST request to /api/chat/reset', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                status: 204,
                json: async () => ({}),
            });
            await apiService.resetChat();
            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/api/chat/reset',
                expect.objectContaining({ method: 'POST' })
            );
        });
    });

    describe('streamChat', () => {
        it('streams chat responses correctly', async () => {
            const mockRequest = { message: 'Hello' };
            const mockChunks = ['Hello', 'World']; // Remove empty space chunk

            // Mock ReadableStream
            const mockStream = new ReadableStream({
                start(controller) {
                    // Don't include empty/space chunks
                    controller.enqueue(new TextEncoder().encode(`data: Hello\n`));
                    controller.enqueue(new TextEncoder().encode(`data: World\n`));
                    controller.enqueue(new TextEncoder().encode('data: [DONE]\n'));
                    controller.close();
                },
            });

            mockFetch.mockResolvedValueOnce({
                ok: true,
                status: 200,
                body: mockStream,
            });

            const chunks: string[] = [];
            for await (const chunk of apiService.streamChat(mockRequest)) {
                chunks.push(chunk);
            }

            expect(chunks).toEqual(mockChunks);
            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/api/chat/stream',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(mockRequest),
                }
            );
        });

        it('handles streaming errors gracefully', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 500,
                json: async () => ({ detail: 'Server error' }),
            });

            const mockRequest = { message: 'Hello' };

            await expect(async () => {
                const iterator = apiService.streamChat(mockRequest);
                await iterator.next();
            }).rejects.toMatchObject({ detail: 'Server error', status: 500 });
        });
    });
});
