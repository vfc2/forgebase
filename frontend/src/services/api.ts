import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type { ChatRequest, ApiError } from '../types/api';

class ApiService {
    private client: AxiosInstance;
    private baseURL: string;

    constructor() {
        // Use environment variable or default to localhost
        this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                console.error('API Request Error:', error);
                return Promise.reject(error);
            }
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                console.log(`API Response: ${response.status} ${response.config.url}`);
                return response;
            },
            (error) => {
                console.error('API Response Error:', error.response?.data || error.message);
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
    async *streamChat(request: ChatRequest): AsyncGenerator<string, void, unknown> {
        const url = `${this.baseURL}/api/chat/stream`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
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

                    // Split by newlines and process each complete line
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || ''; // Keep the last incomplete line in buffer

                    for (const line of lines) {
                        const trimmed = line.trim();
                        if (trimmed && trimmed !== 'data: [DONE]') {
                            if (trimmed.startsWith('data: ')) {
                                const data = trimmed.slice(6); // Remove 'data: ' prefix
                                if (data) {
                                    yield data;
                                }
                            }
                        }
                    }
                }

                // Process any remaining buffer content
                if (buffer.trim()) {
                    const trimmed = buffer.trim();
                    if (trimmed.startsWith('data: ') && trimmed !== 'data: [DONE]') {
                        const data = trimmed.slice(6);
                        if (data) {
                            yield data;
                        }
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
