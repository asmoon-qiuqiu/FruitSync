import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user' // 导入用户仓库
import App from './App.vue'
import router from './router'
import TlbsMap from 'tlbs-map-vue'
import { ElMessage } from 'element-plus'

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

// 初始化用户状态（恢复本地存储的登录信息）
const userStore = useUserStore()
userStore.initUser()
// 每5分钟检查一次token是否过期
setInterval(() => {
    if (userStore.isLoggedIn && userStore.checkTokenExpired()) {
        ElMessage.warning('Token已过期，请重新登录')
        userStore.logout()
        router.push('/login')
    }
}, 5 * 60 * 1000) // 5分钟

app.mount('#app')
