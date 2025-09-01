---
applyTo: "frontend/**"
---

# Frontend Development Guidelines

## Project Context

Forgebase frontend is a React 18 + TypeScript + Vite application that provides a conversational chat interface for LLM interaction. It communicates with a FastAPI backend via Server-Sent Events (SSE) for real-time streaming responses.

**Core Purpose:** Enable users to have conversational workflows through a professional, responsive web interface that renders formatted responses with proper newline handling and markdown support.

## Architecture Overview

### Technology Stack
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite with hot reload and dev container support  
- **Styling:** Tailwind CSS v4 with PostCSS
- **State Management:** TanStack Query (React Query) for server state
- **HTTP Client:** Axios with interceptors
- **Streaming:** Server-Sent Events (SSE) with custom parsing

### Directory Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/           # Chat-specific components
│   │   ├── markdown/       # Markdown rendering components  
│   │   └── ui/            # Reusable UI components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API clients and external services
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Pure utility functions
│   └── test/              # Test utilities and setup
├── public/                # Static assets
└── package.json           # Dependencies and scripts
```

### Core Components
- **Layout:** Main application shell with responsive design
- **ChatInterface:** Primary chat container with message flow
- **MessageBubble:** Individual message rendering with formatting
- **MessageList:** Scrollable message history with auto-scroll
- **MessageInput:** Text input with send functionality

### Key Patterns
- **Custom Hooks:** Extract complex logic (useChat, API interactions)
- **Streaming State:** Real-time message accumulation via SSE
- **Environment Configuration:** Dynamic API URLs via VITE_API_URL
- **Error Boundaries:** Graceful error handling and recovery

## Quality Standards

### Code Quality (Enforced)
```bash
# All code must pass these checks:
npm run lint        # ESLint with TypeScript rules
npx tsc --noEmit    # TypeScript compiler type checking
npm run test:run    # Vitest unit tests (or npm test)
npm run build       # Production build validation
```

### TypeScript Requirements
- **100% Type Coverage:** No `any` types except for verified external libraries
- **Strict Mode:** Enable strict TypeScript configuration
- **Interface Definitions:** All API contracts must have TypeScript interfaces
- **Generic Types:** Use generics for reusable components and hooks

### Testing Standards
- **Unit Tests:** All custom hooks and utility functions
- **Component Tests:** Critical UI components with user interactions
- **Integration Tests:** API service methods and streaming logic
- **Coverage Target:** Minimum 80% test coverage on new code

### Performance Guidelines
- **Bundle Size:** Monitor with `npm run build` - current: 84.20 kB gzipped (target: <100 kB)
- **Lazy Loading:** Code split routes and heavy components
- **Memoization:** Use React.memo, useMemo, useCallback judiciously
- **Network:** Minimize API calls, leverage React Query caching

### Current Quality Metrics
```bash
# Latest verified results (September 2025):
✅ ESLint: 0 errors, 0 warnings
✅ TypeScript: 0 type errors
✅ Tests: 11/11 passing (2 test files)
✅ Build: Success - 84.20 kB gzipped bundle
```

## Development Best Practices

### Component Design
```typescript
// ✅ Good: Single responsibility, typed props
interface MessageBubbleProps {
    message: ChatMessage;
    isStreaming?: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
    message,
    isStreaming = false
}) => {
    // Implementation
};

// ❌ Bad: Multiple responsibilities, untyped
const MessageThing = (props: any) => {
    // Handles messages, input, and API calls
};
```

### Custom Hooks
```typescript
// ✅ Good: Focused hook with clear interface
export const useChat = () => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isStreaming, setIsStreaming] = useState(false);
    
    return {
        messages,
        isStreaming,
        sendMessage,
        resetChat
    };
};
```

### API Integration
```typescript
// ✅ Good: Typed service with error handling
class ApiService {
    async *streamChat(request: ChatRequest): AsyncGenerator<string, void, unknown> {
        try {
            // SSE implementation with proper error handling
        } catch (error) {
            console.error('Streaming error:', error);
            throw error;
        }
    }
}
```

### Error Handling
- **User-Friendly Messages:** Never expose technical errors to users
- **Retry Mechanisms:** Implement automatic retry for transient failures
- **Fallback States:** Graceful degradation when services unavailable
- **Error Boundaries:** Catch and handle React component errors

### Styling Guidelines
- **Tailwind CSS:** Use utility classes, avoid custom CSS when possible
- **Responsive Design:** Mobile-first approach with breakpoint considerations
- **Consistent Spacing:** Use Tailwind spacing scale (0.25rem increments)
- **Color Palette:** Stick to defined theme colors for consistency
- **Accessibility:** Ensure sufficient color contrast and focus states

## Environment & Configuration

### Development Setup
```bash
# Required for development
npm install          # Install dependencies
npm run dev          # Start dev server (port 5173)
npm run build        # Production build
npm run preview      # Preview production build

# Quality checks
npm run lint         # Run ESLint
npx tsc --noEmit     # TypeScript type checking
npm run test:run     # Run all tests
npm run test:ui      # Run tests with UI
```

### Environment Variables
```bash
# Root .env configuration (automatically loaded by Vite)
VITE_API_URL=http://localhost:8000    # Backend API URL
VITE_API_PORT=8000                    # Backend port for dynamic URLs
FORGEBASE_HOST=0.0.0.0               # Backend host
FORGEBASE_PORT=8000                   # Backend port
```

### Dev Container Considerations
- **Host Binding:** Vite configured with `host: '0.0.0.0'` for container access
- **Port Mapping:** Frontend runs on 5173, backend on 8000
- **Hot Reload:** Properly configured for file system watching in containers

## Streaming & SSE Implementation

### Critical SSE Handling
```typescript
// ✅ Proper newline preservation in SSE
const line = buffer.split('\n');
if (line.startsWith('data: ')) {
    const data = line.slice(6);
    // Unescape newlines for proper rendering
    const content = data.replace(/\\n/g, '\n');
}
```

### Message Rendering
```typescript
// ✅ Proper CSS for newline display
<div style={{
    whiteSpace: 'pre-wrap',    // Preserves newlines and wraps text
    wordBreak: 'break-word',   // Handles long words
    lineHeight: '1.5'          // Readable line spacing
}}>
    {message.content}
</div>
```

## Security Considerations

### XSS Prevention
- **Content Sanitization:** Sanitize any user-generated content
- **CSP Headers:** Configure Content Security Policy
- **Input Validation:** Validate all user inputs client and server-side

### API Security
- **Environment Variables:** Never commit API keys or sensitive data
- **CORS Configuration:** Ensure proper CORS setup for production
- **Request Validation:** Validate all outgoing API requests

## Deployment & Production

### Build Optimization
```bash
npm run build        # Creates optimized production bundle
npm run preview      # Test production build locally
```

### Performance Monitoring
- **Bundle Analysis:** Use build tools to analyze bundle size
- **Core Web Vitals:** Monitor LCP, FID, CLS metrics
- **Error Tracking:** Implement client-side error reporting

### Browser Support
- **Target:** Modern browsers (ES2020+)
- **Fallbacks:** Graceful degradation for older browsers
- **Testing:** Cross-browser testing for critical flows

## Troubleshooting Common Issues

### SSE/Streaming Problems
- **CORS Errors:** Check backend CORS configuration
- **Connection Issues:** Verify API URL and network connectivity  
- **Newline Display:** Ensure SSE escaping/unescaping and CSS whitespace
- **Memory Leaks:** Properly cleanup EventSource connections

### Development Issues
- **Hot Reload:** Restart dev server if file watching breaks
- **Type Errors:** Run `npx tsc --noEmit` for detailed TypeScript errors
- **Build Failures:** Check for unused imports and missing dependencies
- **Test Failures:** Use `npm run test:ui` for interactive debugging

Remember: Always prioritize user experience, maintainable code, and proper error handling. When in doubt, refer to the React and TypeScript documentation for best practices.
