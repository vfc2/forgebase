import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/ui/Layout';
import { ChatInterface } from './components/chat/ChatInterface';
import { MarkdownPreview } from './components/markdown/MarkdownPreview';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  // For now, we'll just show empty markdown preview
  // Later this can be connected to actual markdown content from the agent
  const markdownContent = '';

  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <div className="h-full flex">
          {/* Chat Interface - Left Pane */}
          <div className="w-1/2 border-r border-gray-200">
            <ChatInterface />
          </div>

          {/* Markdown Preview - Right Pane */}
          <div className="w-1/2">
            <MarkdownPreview content={markdownContent} />
          </div>
        </div>
      </Layout>
    </QueryClientProvider>
  );
}

export default App;
