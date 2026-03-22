import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://stunning-memory-wrrgp69rxg6xc94rp-8000.app.github.dev',
        changeOrigin: true,
        secure: true,
      },
    },
  },
})