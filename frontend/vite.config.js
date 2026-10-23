import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// En desarrollo, las peticiones a /api y /media se envían a Django.
const DJANGO = 'http://127.0.0.1:8010'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': DJANGO,
      '/media': DJANGO,
    },
  },
})
