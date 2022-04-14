import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { DocumentCopy } from '@element-plus/icons-vue'

const app = createApp(App)
app.use(ElementPlus)
app.component( 'DocumentCopy', DocumentCopy)
app.mount('#app')
