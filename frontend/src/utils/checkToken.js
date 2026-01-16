import { useUserStore } from "@/stores/user"
import router from "@/router"
import { ElMessage } from "element-plus"

/**
 * 初始化用户状态 + 定时检查Token过期
 * @returns {Function} 清除定时器的方法（可选）
 */
export function initTokenCheck() {
    let checkTokenInterval = null
    if (checkTokenInterval) {
        clearInterval(checkTokenInterval)
    }

    const userStore = useUserStore()
    userStore.initUser()

    // 每6小时检查一次Token
    checkTokenInterval = setInterval(() => {
        try {
            if (userStore.isLoggedIn && userStore.checkTokenExpired()) {
                ElMessage.warning('Token已过期，请重新登录')
                userStore.logout()
                router.push('/login')
                clearInterval(checkTokenInterval)
                checkTokenInterval = null
            }
        } catch (error) {
            console.error('检查Token过期时出错:', error)
            ElMessage.error('检查Token过期时出错')
            clearInterval(checkTokenInterval)
            checkTokenInterval = null
        }
    }, 6 * 60 * 60 * 1000)

    // 返回清除定时器的方法，方便后续手动停止检查
    return () => {
        if (checkTokenInterval) {
            clearInterval(checkTokenInterval)
            checkTokenInterval = null
        }
    }
}