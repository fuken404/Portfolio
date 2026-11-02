import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/tokens.css'
import './styles/app.css'
import { startAnalytics } from './analytics'
import App from './App.jsx'
import LanguageProvider from './i18n/LanguageProvider.jsx'

startAnalytics()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LanguageProvider>
      <App />
    </LanguageProvider>
  </StrictMode>,
)
