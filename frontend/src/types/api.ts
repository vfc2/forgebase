export interface ChatMessage {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
}

export interface ChatRequest {
    message: string;
}

export interface ApiError {
    detail: string;
    status?: number;
}


export interface Project {
    id: string;
    name: string;
    createdAt: Date;
}
