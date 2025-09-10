export interface ChatMessage {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
}

export interface ChatRequest {
    message: string;
    projectId?: string;
}

export interface ApiError {
    detail: string;
    status?: number;
}


export interface Project {
    id: string;
    name: string;
    prd: string;
    createdAt: Date;
    updatedAt?: Date;
}

export interface ProjectCreateRequest {
    name: string;
    prd?: string;
}

export interface ProjectUpdateRequest {
    name?: string;
    prd?: string;
}
