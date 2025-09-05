# Forgebase Frontend

A modern React + TypeScript frontend for the Forgebase conversational PRD generation system.

## Features

- **Split-pane layout**: Chat interface on the left, markdown preview on the right
- **Real-time streaming**: Live chat responses using Server-Sent Events
- **Responsive design**: Mobile and tablet friendly
- **Professional UI**: Clean, modern design similar to ChatGPT/Azure
- **TypeScript**: Full type safety throughout
- **Testing**: Comprehensive test suite with Vitest
- **Performance**: Optimized builds with Vite

## Tech Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Mantine UI (theme + components)
- **State Management**: Custom hooks for local/business state
- **Markdown**: react-markdown with syntax highlighting
- **HTTP Client**: Native fetch (including streaming via ReadableStream)
- **Testing**: Vitest + Testing Library + jsdom

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests with UI
npm run test:ui
```

### Environment Variables

Create a `.env` file in the frontend directory (optional). If `VITE_API_URL` is absent the app falls back to `http://localhost:${VITE_API_PORT || 8000}`.

```bash
# Explicit full URL (recommended for non-local setups)
VITE_API_URL=http://localhost:8000

# Or alternatively specify only a port (fallback path)
VITE_API_PORT=8000
```

## Project Structure

```
src/
├── components/           # React components
│   ├── chat/            # Chat interface components
│   ├── markdown/        # Markdown preview components
│   └── ui/              # Reusable UI components
├── hooks/               # Custom React hooks
├── services/            # API service layer
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
└── test/                # Test configuration
```

## API Integration

The frontend connects to the Forgebase FastAPI backend:

- `POST /api/chat/stream` - Streaming chat responses
- `POST /api/chat/reset` - Reset conversation
- `GET /health` - Health check

## Testing

Tests are written using Vitest and Testing Library:

```bash
# Run all tests
npm run test

# Open test UI
npm run test:ui
```

## Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The build outputs to the `dist/` directory.

## Architecture

### Component Structure

- **Layout**: Main application layout with header
- **ChatInterface**: Complete chat functionality
- **MessageList**: Scrollable message history
- **MessageInput**: Auto-resizing input with keyboard shortcuts
- **MarkdownPreview**: Live markdown rendering with copy functionality

### State Management

- **Custom hooks**: `useChat`, `useProjects`, `useTheme` encapsulate domain + UI logic.
- **Local state**: Direct component concerns with `useState`.
- React Query previously handled a single mutation; after simplifying network logic it is no longer required. Reintroduce only if server caching / background refetching becomes necessary.

### Styling

- **Mantine UI**: Component library with theming
- **Custom design tokens**: Consistent colors, typography, spacing (see Mantine theme in `src/main.tsx`)
- **Responsive**: Mobile-first responsive design
- **Dark mode**: Controlled via `ThemeProvider`

## Contributing

1. Follow existing code style & lint rules (`npm run lint`).
2. Add or update tests for every new component/hook/utility.
3. Update this README and internal instructions when behavior changes.
4. Quality gate before PR:

- `npm run lint`
- `npm run test -- --run`
- `npm run build`

5. Keep changes small and focused; prefer pure utilities for shared logic (see `src/utils/chat.ts`).

## License

Same as parent project (see root LICENSE file)

Optional: add [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for additional React lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```
