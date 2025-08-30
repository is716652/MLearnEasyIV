import { defineConfig } from 'vite'
import uniImport from '@dcloudio/vite-plugin-uni'

const uni = (uniImport as any)?.default ?? (uniImport as any)

export default defineConfig(({ mode }) => {
  const port = Number(process.env.PORT || 90)
  const outDir = process.env.OUT_DIR || 'dist2'
  return {
    plugins: [uni()],
    clearScreen: false,
    server: {
      host: '0.0.0.0',
      port,
      strictPort: true,
    },
    preview: {
      port,
    },
    build: {
      outDir,
      emptyOutDir: true,
    },
  }
})