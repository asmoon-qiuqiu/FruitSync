import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import TlbsMap from 'tlbs-map-vue'


// 导入bootstrap样式
import 'bootstrap/dist/css/bootstrap.min.css'
// 导入bootstrap图标
import 'bootstrap-icons/font/bootstrap-icons.css'
// 引入 Bootstrap JS（包含轮播交互逻辑，已集成 Popper）
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// 导入 ElMessage 的样式
import 'element-plus/es/components/message/style/index'

const app = createApp(App)

app.use(createPinia())
app.use(TlbsMap)
app.use(router)

app.mount('#app')

// 初始化Token检查逻辑
import { initTokenCheck } from "@/utils/checkToken"
initTokenCheck()