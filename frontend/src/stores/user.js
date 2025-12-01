// src/stores/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 状态：是否登录、用户信息
  const isLoggedIn = ref(false)
  const username = ref('')
  const userId = ref(null)

  // 登录方法：存入用户信息
  const login = (userData) => {
    // 字符串参数（只传username，用于注册）
    if (typeof userData === 'string') {
      username.value = userData
      isLoggedIn.value = true
    } else {
      // 接收用户对象（用于登录）
      username.value = userData.username
      userId.value = userData.id
      isLoggedIn.value = true
    }

    // 持久化用户信息到localStorage
    localStorage.setItem('user', JSON.stringify({
      isLoggedIn: true,
      username: username.value,
      userId: userId.value
    }))
  }

  // 退出方法：清除状态和本地存储
  const logout = () => {
    isLoggedIn.value = false
    username.value = ''
    userId.value = null

    // 清除用户信息和token
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  // 检查token是否有效（解析JWT的过期时间）
  const checkTokenExpired = () => {
    const token = localStorage.getItem('token')
    if (!token) {
      return true // 没有token视为已过期
    }

    try {
      // JWT格式：header.payload.signature
      const payload = token.split('.')[1]
      const decodedPayload = JSON.parse(atob(payload))

      // exp是过期时间戳（秒）
      if (decodedPayload.exp) {
        const currentTime = Math.floor(Date.now() / 1000)
        return decodedPayload.exp < currentTime
      }

      return false
    } catch (error) {
      console.error('解析token失败:', error)
      return true // 解析失败视为已过期
    }
  }

  // 初始化：页面刷新后从本地恢复状态
  const initUser = () => {
    const userStr = localStorage.getItem('user')
    const token = localStorage.getItem('token')

    // 只有同时存在用户信息和token才认为是登录状态
    if (userStr && token) {
      try {
        const user = JSON.parse(userStr)
        isLoggedIn.value = user.isLoggedIn
        username.value = user.username
        userId.value = user.userId || null
      } catch (error) {
        console.error('解析用户信息失败:', error)
        logout() // 解析失败则清除状态
      }
    }
  }

  return {
    isLoggedIn,
    username,
    userId,
    login,
    logout,
    initUser,
    checkTokenExpired
  }
})