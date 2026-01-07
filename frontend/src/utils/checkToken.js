import { useUserStore } from "@/stores/user"
import router from "@/router"
import { ElMessage } from "element-plus"

/**
 * 初始化用户状态 + 定时检查Token过期
 * @returns {Function} 清除定时器的方法（可选）
 */
export function initTokenCheck() {
    const userStore = useUserStore()
    userStore.initUser()

    // 每6小时检查一次Token（你写的 6*60*60*1000 是6小时，不是5分钟）
    const checkTokenInterval = setInterval(() => {
        if (userStore.isLoggedIn && userStore.checkTokenExpired()) {
            ElMessage.warning('Token已过期，请重新登录')
            userStore.logout()
            router.push('/login')
            clearInterval(checkTokenInterval)
        }
    }, 6 * 60 * 60 * 1000)

    // 返回清除定时器的方法，方便后续手动停止检查
    return () => clearInterval(checkTokenInterval)
}