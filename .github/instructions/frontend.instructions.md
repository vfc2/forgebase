FastAPI Frontend Implementation Task
Project Overview
Create a professional web application frontend for a FastAPI backend. This is an MVP featuring a chat interface for LLM interaction and a markdown preview pane.
Technical Stack

Framework: React 18 with TypeScript
Build Tool: Vite
Styling: Tailwind CSS
State Management: React Query (TanStack Query) for API state
Markdown Rendering: react-markdown with syntax highlighting
HTTP Client: Axios or fetch API

UI/UX Requirements
Layout & Design

Split-pane layout: Chat interface on the left, markdown preview on the right
Responsive design: Graceful mobile/tablet adaptation
Visual style: Light theme similar to ChatGPT/Azure - clean, modern, professional, elegant
Color palette: Whites, light grays, subtle blues/greens for accents
Typography: Clean, readable fonts (Inter, system fonts)

Chat Interface (Left Pane)

ChatGPT-like design: Message bubbles, clear user/agent distinction
Input area: Bottom-fixed input with send button
Message history: Scrollable conversation history
Loading states: Typing indicators, loading spinners
Error handling: Graceful error messages, retry functionality
Auto-scroll: Scroll to latest messages
Keyboard shortcuts: Enter to send, Shift+Enter for new line

Markdown Preview (Right Pane)

Read-only display: Non-editable markdown rendering
Live updates: Updates when agent calls markdown tool
Syntax highlighting: Code blocks with proper highlighting
Scroll sync: Independent scrolling from chat
Empty state: Placeholder when no content available
Copy functionality: Easy content copying

Technical Requirements
Architecture

SOLID principles: Single responsibility, dependency injection, clean interfaces
Component structure: Modular, reusable components
Custom hooks: Extract logic into reusable hooks
Error boundaries: Graceful error handling
TypeScript: Full type safety, interfaces for API contracts

API Integration

Base URL: Configurable API endpoint
Authentication: Token-based (if required)
WebSocket: Real-time chat updates (if supported by backend)
Polling fallback: If WebSocket unavailable
Request/Response typing: TypeScript interfaces for all API calls

State Management

React Query: API state, caching, background updates
Local state: React useState/useReducer for UI state
Context: Minimal use, only for truly global state
Persistence: Chat history persistence (localStorage)

Performance & Best Practices

Code splitting: Lazy loading for routes/components
Memoization: React.memo, useMemo, useCallback where appropriate
Bundle optimization: Tree shaking, minimal dependencies
Accessibility: ARIA labels, keyboard navigation, screen reader support
Testing: Unit tests for components and hooks
Error handling: Try-catch blocks, user-friendly error messages

Implementation Phases
Phase 1: Project Setup

Initialize Vite + React + TypeScript project
Configure Tailwind CSS
Set up basic project structure
Install and configure dependencies

Phase 2: Core Components

Create layout component with split panes
Build chat message components
Implement input component with validation
Create markdown preview component

Phase 3: API Integration

Set up API client with TypeScript interfaces
Implement React Query for state management
Connect chat functionality to backend
Integrate markdown tool calling

Phase 4: Polish & Testing

Implement loading states and error handling
Add responsive design tweaks
Write unit tests for key components
Performance optimization

Key Considerations

Simplicity: Keep components focused and single-purpose
Maintainability: Clear naming, consistent patterns
User Experience: Smooth interactions, immediate feedback
Edge cases: Handle network errors, empty states, long messages
Browser compatibility: Modern browsers (ES2020+)

Deliverables

Complete React application with all specified features
TypeScript interfaces for all API interactions
Responsive design that works on desktop and mobile
Basic test coverage for critical components
README with setup and deployment instructions

Start with the project setup and core layout, then incrementally add features following the phases outlined above. Focus on getting a working MVP first, then iterate on polish and performance.