import type { ChatRequest, ApiError, Project, ProjectCreateRequest, ProjectUpdateRequest } from '../types/api';
import { extractSseChunks, unescapeSseData } from '../utils/chat';

class ApiService {
    private baseURL: string;
    private isDev: boolean;

    constructor() {
        this.baseURL = import.meta.env.VITE_API_URL || `http://localhost:${import.meta.env.VITE_API_PORT || '8000'}`;
        this.isDev = import.meta.env.MODE === 'development';
    }
    private async request<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
        const url = `${this.baseURL}${path}`;
        if (this.isDev) console.log(`API Request: ${options.method || 'GET'} ${url}`);
        let response: Response;
        try {
            response = await fetch(url, {
                headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
                ...options,
            });
    } catch {
            const err: ApiError = { detail: 'Network error - unable to reach server', status: 0 };
            throw err;
        }
        if (!response.ok) {
            let detail = `HTTP ${response.status}`;
            try {
                const data = await response.json();
                detail = data?.detail || detail;
            } catch {/* ignore json parse */}
            const err: ApiError = { detail, status: response.status };
            if (this.isDev) console.error('API Response Error:', err.detail);
            throw err;
        }
        if (response.status === 204) return undefined as T; // No Content
        try {
            const data = (await response.json()) as T;
            if (this.isDev) console.log(`API Response: ${response.status} ${url}`);
            return data;
    } catch {
            // If no body
            return undefined as T;
        }
    }

    async healthCheck(): Promise<{ status: string }> {
        return this.request<{ status: string }>('/health');
    }

    async resetChat(): Promise<void> {
        await this.request<void>('/api/chat/reset', { method: 'POST', body: JSON.stringify({}) });
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
                const err: ApiError = { detail: errorData.detail || `HTTP ${response.status}`, status: response.status };
                throw err;
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
            const apiError: ApiError = error && typeof error === 'object' && 'detail' in (error as ApiError)
                ? error as ApiError
                : { detail: error instanceof Error ? error.message : 'Streaming error' };
            if (this.isDev) console.error('Streaming error:', apiError.detail);
            throw apiError;
        }
    }

    // Project API methods
    async listProjects(): Promise<Project[]> {
        const projects = await this.request<Project[]>('/api/projects');
        // Convert date strings to Date objects
        return projects.map(project => ({
            ...project,
            createdAt: new Date(project.createdAt),
            updatedAt: project.updatedAt ? new Date(project.updatedAt) : undefined
        })).map(project => {
            // Validate that the date conversion worked
            if (isNaN(project.createdAt.getTime())) {
                console.warn('Invalid createdAt date for project:', project.id, project.createdAt);
                project.createdAt = new Date(); // Fallback to current date
            }
            if (project.updatedAt && isNaN(project.updatedAt.getTime())) {
                console.warn('Invalid updatedAt date for project:', project.id, project.updatedAt);
                project.updatedAt = undefined; // Fallback to undefined
            }
            return project;
        });
    }

    async createProject(request: ProjectCreateRequest): Promise<Project> {
        const project = await this.request<Project>('/api/projects', {
            method: 'POST',
            body: JSON.stringify(request)
        });
        // Convert date strings to Date objects with validation
        const result = {
            ...project,
            createdAt: new Date(project.createdAt),
            updatedAt: project.updatedAt ? new Date(project.updatedAt) : undefined
        };
        
        // Validate date conversion
        if (isNaN(result.createdAt.getTime())) {
            console.warn('Invalid createdAt date for created project:', result.id, project.createdAt);
            result.createdAt = new Date(); // Fallback to current date
        }
        if (result.updatedAt && isNaN(result.updatedAt.getTime())) {
            console.warn('Invalid updatedAt date for created project:', result.id, project.updatedAt);
            result.updatedAt = undefined;
        }
        
        return result;
    }

    async getProject(id: string): Promise<Project> {
        const project = await this.request<Project>(`/api/projects/${id}`);
        // Convert date strings to Date objects with validation
        const result = {
            ...project,
            createdAt: new Date(project.createdAt),
            updatedAt: project.updatedAt ? new Date(project.updatedAt) : undefined
        };
        
        // Validate date conversion
        if (isNaN(result.createdAt.getTime())) {
            console.warn('Invalid createdAt date for project:', result.id, project.createdAt);
            result.createdAt = new Date(); // Fallback to current date
        }
        if (result.updatedAt && isNaN(result.updatedAt.getTime())) {
            console.warn('Invalid updatedAt date for project:', result.id, project.updatedAt);
            result.updatedAt = undefined;
        }
        
        return result;
    }

    async updateProject(id: string, request: ProjectUpdateRequest): Promise<Project> {
        const project = await this.request<Project>(`/api/projects/${id}`, {
            method: 'PUT',
            body: JSON.stringify(request)
        });
        // Convert date strings to Date objects with validation
        const result = {
            ...project,
            createdAt: new Date(project.createdAt),
            updatedAt: project.updatedAt ? new Date(project.updatedAt) : undefined
        };
        
        // Validate date conversion
        if (isNaN(result.createdAt.getTime())) {
            console.warn('Invalid createdAt date for updated project:', result.id, project.createdAt);
            result.createdAt = new Date(); // Fallback to current date
        }
        if (result.updatedAt && isNaN(result.updatedAt.getTime())) {
            console.warn('Invalid updatedAt date for updated project:', result.id, project.updatedAt);
            result.updatedAt = undefined;
        }
        
        return result;
    }

    async deleteProject(id: string): Promise<void> {
        await this.request<void>(`/api/projects/${id}`, { method: 'DELETE' });
    }
}

export const apiService = new ApiService();
