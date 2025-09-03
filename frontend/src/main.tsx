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
import { ThemeProvider } from './providers/ThemeProvider';
import { useTheme } from './hooks/useTheme';

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
      '#fcfcfc', // 50 - very light warm grey instead of pure white
      '#f8f9fa', // 100 - soft light grey
      '#f1f3f4', // 200 - subtle grey
      '#e8eaed', // 300 - gentle grey
      '#dadce0', // 400 - medium light grey
      '#9aa0a6', // 500 - balanced grey
      '#5f6368', // 600 - medium grey
      '#3c4043', // 700 - darker grey
      '#202124', // 800 - dark grey
      '#171717', // 900 - very dark
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
  other: {
    // Custom colors for light theme backgrounds
    lightBackground: '#fcfcfc',
    lightSurface: '#f8f9fa',
    lightBorder: '#e8eaed',
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

export function AppWithTheme() {
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
