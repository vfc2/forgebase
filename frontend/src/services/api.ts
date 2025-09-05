import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type { ChatRequest, ApiError } from '../types/api';
import { extractSseChunks, unescapeSseData } from '../utils/chat';

class ApiService {
    private client: AxiosInstance;
    private baseURL: string;

    constructor() {
        // Use environment variable with a sensible default for development
        this.baseURL = import.meta.env.VITE_API_URL || `http://localhost:${import.meta.env.VITE_API_PORT || '8000'}`;

        this.client = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000, // 30 seconds
        });

        this.setupInterceptors();
    }

    private setupInterceptors() {
        const isDev = import.meta.env.MODE === 'development';
        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                if (isDev) console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                if (isDev) console.error('API Request Error:', error);
                return Promise.reject(error);
            }
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                if (isDev) console.log(`API Response: ${response.status} ${response.config.url}`);
                return response;
            },
            (error) => {
                if (isDev) console.error('API Response Error:', error.response?.data || error.message);
                return Promise.reject(this.handleError(error));
            }
        );
    }

    private handleError(error: unknown): ApiError {
        if (axios.isAxiosError(error)) {
            if (error.response) {
                return {
                    detail: error.response.data?.detail || 'Server error occurred',
                    status: error.response.status,
                };
            } else if (error.request) {
                return {
                    detail: 'Network error - unable to reach server',
                    status: 0,
                };
            }
        }

        return {
            detail: error instanceof Error ? error.message : 'Unknown error occurred',
        };
    }

    async healthCheck(): Promise<{ status: string }> {
        const response = await this.client.get('/health');
        return response.data;
    }

    async resetChat(): Promise<void> {
        await this.client.post('/api/chat/reset');
    }

    // Streaming chat using fetch API (since axios doesn't handle SSE well)
    async *streamChat(request: ChatRequest, signal?: AbortSignal): AsyncGenerator<string, void, unknown> {
        const url = `${this.baseURL}/api/chat/stream`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
                signal,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            const reader = response.body?.getReader();
            if (!reader) {
                throw new Error('Failed to get response reader');
            }

            const decoder = new TextDecoder();
            let buffer = '';

            try {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    buffer += decoder.decode(value, { stream: true });
                    const { chunks, remaining } = extractSseChunks(buffer);
                    buffer = remaining; // keep incomplete line
                    for (const chunk of chunks) {
                        yield chunk;
                    }
                }

                // Flush any remaining complete data in buffer
                const trimmed = buffer.trim();
                if (trimmed.startsWith('data: ') && trimmed !== 'data: [DONE]') {
                    const data = trimmed.slice(6);
                    if (data) {
                        yield unescapeSseData(data);
                    }
                }
            } finally {
                reader.releaseLock();
            }
        } catch (error) {
            console.error('Streaming error:', error);
            throw error;
        }
    }
}

export const apiService = new ApiService();
