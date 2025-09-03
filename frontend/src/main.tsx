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
  // you can customize theme here later
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="auto">
      <Notifications position="top-right" />
      <App />
    </MantineProvider>
  </StrictMode>,
)
