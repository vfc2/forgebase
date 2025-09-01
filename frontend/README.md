# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

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

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with Typography plugin
- **State Management**: React Query (TanStack Query) for API state
- **Markdown**: react-markdown with syntax highlighting
- **HTTP Client**: Axios + fetch API for streaming
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

Create a `.env` file in the frontend directory:

```bash
VITE_API_URL=http://localhost:8000
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

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

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

- **React Query**: API state, caching, background updates
- **Custom hooks**: Business logic extraction (useChat)
- **Local state**: UI state with useState/useReducer

### Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Custom design system**: Consistent colors, typography, spacing
- **Responsive**: Mobile-first responsive design
- **Dark mode ready**: Prepared for future dark mode support

## Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass before submitting

## License

Same as parent project (see root LICENSE file)

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
