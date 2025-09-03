export interface ChatMessage {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
}

export interface ChatRequest {
    message: string;
}

export interface ChatResponse {
    message: string;
    timestamp: string;
}

export interface ApiError {
    detail: string;
    status?: number;
}

export interface StreamingResponse {
    chunk: string;
    done: boolean;
}

export interface Project {
    id: string;
    name: string;
    createdAt: Date;
}
