import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', //根路径
      name: 'home', //路由名称
      component: () => import('../views/home/Home.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/login/Login.vue'),
      // meta: { requiresAuth: true } // 需要登录才能访问
    },

    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/Contact.vue')
    },
  ],
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 如果路由需要登录
  if (to.meta.requiresAuth) {
    // 检查是否登录且token未过期
    if (!userStore.isLoggedIn || userStore.checkTokenExpired()) {
      ElMessage.warning('请先登录')
      userStore.logout() // 清除过期状态
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
