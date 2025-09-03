# ForgeBase Frontend - Agent Instructions

## Project Overview

ForgeBase is a conversational AI tool for creating Product Requirements Documents (PRDs). The frontend is a React + TypeScript application with a chat interface that communicates with an AI backend to generate comprehensive PRDs.

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 7.1.4
- **UI Library**: Mantine UI 8.2.8 (AppShell, components, theming)
- **State Management**: React hooks (useChat, useTheme)
- **Testing**: Vitest + React Testing Library
- **Styling**: Mantine CSS-in-JS with custom theme
- **Linting**: ESLint with React Fast Refresh rules
- **Package Manager**: npm

## Architecture & File Structure

### Core Structure

```
src/
├── components/           # Reusable UI components
│   ├── chat/            # Chat-specific components
│   ├── layout/          # Layout components (Header, Sidebar)
│   ├── markdown/        # Markdown rendering
│   └── ui/              # Generic UI components
├── contexts/            # React contexts (ThemeContext)
├── hooks/               # Custom hooks (useChat, useTheme)
├── providers/           # Context providers (ThemeProvider)
├── services/            # API services
├── types/               # TypeScript type definitions
└── utils/               # Utility functions
```

### Key Components

- **App.tsx**: Main application with AppShell layout
- **ChatInterface**: Primary chat UI with message input/output
- **Header**: Theme toggle, user menu, navigation
- **Sidebar**: Chat history, new conversation, clear history
- **MessageBubble**: Individual message display with user/assistant styling
- **useChat**: Core chat state management hook
- **useTheme**: Theme management with localStorage persistence

## Development Standards

### Code Quality Requirements

1. **After ANY change, ALWAYS run**:

   ```bash
   npm run test    # All tests must pass (100% success rate)
   npm run lint    # Zero warnings/errors
   npm run build   # Must compile successfully
   ```

2. **Test Coverage**: Every component must have comprehensive tests
   - Component rendering and props
   - User interactions and event handling
   - Edge cases and error states
   - Accessibility compliance (aria-labels, keyboard navigation)

### React Fast Refresh Compliance

- **Hooks**: Export only hooks from `/hooks/` files
- **Components**: Export only components from component files
- **Contexts**: Separate context definitions in `/contexts/`
- **Providers**: Component providers in `/providers/`
- **Main.tsx**: All components must be exported functions

### TypeScript Standards

- Strict mode enabled
- Use `type` imports: `import type { Type } from './module'`
- Proper interface definitions in `/types/`
- No `any` types allowed

### Testing Standards

- **Location**: Co-located `*.test.tsx` files
- **Coverage**: Test all user interactions, edge cases, accessibility
- **Setup**: Use proper test wrappers (ThemeProvider, AppShell)
- **Mocking**: Mock external dependencies (ResizeObserver, useChat hook)
- **Accessibility**: Test aria-labels, keyboard navigation, focus management

### Mantine UI Patterns

- Use AppShell for layout structure
- Theme integration with `useTheme` hook
- Proper component props and styling
- ResizeObserver polyfill required for ScrollArea components
- Accessibility attributes on interactive elements

### API Integration

- **Service Layer**: `/services/api.ts` for backend communication
- **Types**: Define API interfaces in `/types/api.ts`
- **Error Handling**: Proper error states and user feedback
- **Streaming**: Support for streaming chat responses

## File Locations Reference

### Components

- Chat: `/src/components/chat/` (ChatInterface, MessageBubble, MessageInput, MessageList)
- Layout: `/src/components/layout/` (Header, Sidebar)
- UI: `/src/components/ui/` (Button, Input, Layout)

### State Management

- Theme: `/src/contexts/ThemeContext.ts`, `/src/providers/ThemeProvider.tsx`, `/src/hooks/useTheme.tsx`
- Chat: `/src/hooks/useChat.ts`

### Configuration

- Vite: `vite.config.ts`
- TypeScript: `tsconfig.json`, `tsconfig.app.json`
- Testing: `vitest.config.ts`, `/src/test/setup.ts`
- Linting: `eslint.config.js`

## Common Tasks

### Adding New Components

1. Create component in appropriate `/src/components/` subdirectory
2. Create co-located test file
3. Add proper TypeScript interfaces
4. Implement accessibility features
5. Add to index exports if needed
6. Run quality checks

### Updating State Management

1. Modify hook in `/src/hooks/`
2. Update related provider if needed
3. Update TypeScript types
4. Update all dependent components
5. Update all related tests
6. Verify no breaking changes

### API Changes

1. Update `/src/services/api.ts`
2. Update `/src/types/api.ts`
3. Update components using the API
4. Update tests with new mock data
5. Handle error cases

## Quality Checklist

- [ ] All tests pass
- [ ] ESLint clean (zero warnings/errors)
- [ ] TypeScript compiles successfully
- [ ] Build completes without errors
- [ ] Accessibility compliance verified
- [ ] Fast Refresh rules followed
- [ ] Tests added/updated for changes
- [ ] Error handling implemented
- [ ] Types properly defined

## Notes for Agents

- Always check existing patterns before implementing new features
- Maintain consistency with Mantine UI design system
- Preserve accessibility features and test coverage
- Follow the established file organization
- Consider responsive design and theme switching
- Test both light and dark themes
- Verify chat functionality end-to-end
