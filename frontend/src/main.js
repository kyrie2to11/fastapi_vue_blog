import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import naive from './plugins/naive-ui'

// 导入全局样式
import './assets/styles/main.scss'

const app = createApp(App)

// 安装插件
app.use(createPinia())
app.use(router)
app.use(naive)

app.mount('#app')