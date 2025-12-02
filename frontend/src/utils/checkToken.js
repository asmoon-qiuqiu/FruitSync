import { useUserStore } from "@/stores/user"
import router from "@/router"
import { ElMessage } from "element-plus"


// 初始化用户状态（恢复本地存储的登录信息）
const userStore = useUserStore()
userStore.initUser()
// 每5分钟检查一次token是否过期
const checkTokenInterval = setInterval(() => {
    if (userStore.isLoggedIn && userStore.checkTokenExpired()) {
        ElMessage.warning('Token已过期，请重新登录')
        userStore.logout()
        router.push('/login')
        clearInterval(checkTokenInterval)
    }
}, 6 * 60 * 60 * 1000) // 6小时