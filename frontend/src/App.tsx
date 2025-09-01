import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/ui/Layout';
import { ChatInterface } from './components/chat/ChatInterface';
import './App.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <ChatInterface />
      </Layout>
    </QueryClientProvider>
  );
}

export default App;