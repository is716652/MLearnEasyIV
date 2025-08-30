import { createSSRApp } from 'vue'
// 需要先安装pinia依赖包:
// npm install pinia
import { createPinia } from 'pinia'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  app.use(createPinia())
  return {
    app,
  }
}