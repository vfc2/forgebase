import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Mantine styles
import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'
// App styles
import './index.css'
import App from './App.tsx'
// Mantine providers
import { MantineProvider, createTheme } from '@mantine/core'
import { Notifications } from '@mantine/notifications'
import { ThemeProvider, useTheme } from './hooks/useTheme.tsx'

const theme = createTheme({
  fontFamily: 'Inter, system-ui, sans-serif',
  primaryColor: 'blue',
  colors: {
    blue: [
      '#f0f9ff', // 50
      '#e0f2fe', // 100
      '#bae6fd', // 200
      '#7dd3fc', // 300
      '#38bdf8', // 400
      '#0ea5e9', // 500 - your primary
      '#0284c7', // 600
      '#0369a1', // 700
      '#075985', // 800
      '#0c4a6e', // 900
    ],
    gray: [
      '#fafafa', // 50
      '#f5f5f5', // 100
      '#e5e5e5', // 200
      '#d4d4d4', // 300
      '#a3a3a3', // 400
      '#737373', // 500
      '#525252', // 600
      '#404040', // 700
      '#262626', // 800
      '#171717', // 900
    ],
  },
  defaultRadius: 'md',
  spacing: {
    xs: '8px',
    sm: '12px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  shadows: {
    xs: '0 1px 3px rgba(0, 0, 0, 0.1)',
    sm: '0 1px 6px rgba(0, 0, 0, 0.1)',
    md: '0 4px 12px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 24px rgba(0, 0, 0, 0.1)',
    xl: '0 16px 48px rgba(0, 0, 0, 0.1)',
  },
  headings: {
    fontFamily: 'Inter, system-ui, sans-serif',
    fontWeight: '600',
  },
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
    Paper: {
      defaultProps: {
        radius: 'md',
      },
    },
    TextInput: {
      defaultProps: {
        radius: 'md',
      },
    },
    Textarea: {
      defaultProps: {
        radius: 'md',
      },
    },
  },
})

function AppWithTheme() {
  const { colorScheme } = useTheme();
  
  return (
    <MantineProvider theme={theme} forceColorScheme={colorScheme}>
      <Notifications position="top-right" />
      <App />
    </MantineProvider>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <AppWithTheme />
    </ThemeProvider>
  </StrictMode>,
)
