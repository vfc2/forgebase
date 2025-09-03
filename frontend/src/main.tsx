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
  },
  defaultRadius: 'md',
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="auto">
      <Notifications position="top-right" />
      <App />
    </MantineProvider>
  </StrictMode>,
)
