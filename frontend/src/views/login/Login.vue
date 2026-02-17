<script setup>
  import { ref, reactive } from 'vue'
  import Loading from '@/components/Loading.vue'
  import { ElMessage } from 'element-plus'
  import LoginForm from './LoginForm.vue' // 导入登录子组件
  import RegisterForm from './RegisterForm.vue' // 导入注册子组件
  import { useAuthForm } from '@/utils/useFormEye'
  import { userRegisterApi } from '@/api/register'
  import { userLoginApi } from '@/api/login'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'

  const router = useRouter()
  const userStore = useUserStore() // 创建仓库实例
  const isLoading = ref(false) // 控制loading显示/隐藏

  // 定义响应式的表单数据对象，存储登录/注册的输入内容
  const form = reactive({
    username: '', // 用户名
    email: '', // 注册邮箱
    password: '', // 密码
    repassword: '', // 确认密码
  })
  // 使用表单辅助方法
  const { isLogin, changeForm, showPassword, togglePassword } = useAuthForm(form)
  // 父组件统一的表单重置方法
  const resetFormData = () => {
    form.username = ''
    form.password = ''
    form.email = ''
    form.repassword = ''
  }
  // 定义验证规则函数
  const validateUsername = (username) => {
    const trimmed = username?.trim()
    if (!trimmed) {
      // 返回错误信息对象，方便区分错误类型或用于国际化
      return { isValid: false, message: '请输入用户名！' }
    }
    if (trimmed.length < 3 || trimmed.length > 50) {
      return { isValid: false, message: '用户名长度需在3-50个字符之间！' }
    }
    return { isValid: true } // 成功时不带消息或带空消息
  }

  const validateEmail = (email) => {
    const trimmed = email?.trim()
    if (!trimmed) {
      return { isValid: false, message: '请输入注册邮箱！' }
    }
    if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(trimmed)) {
      return { isValid: false, message: '请输入合法的邮箱格式！' }
    }
    return { isValid: true }
  }

  const validatePassword = (password) => {
    if (!password) {
      return { isValid: false, message: '请输入密码！' }
    }
    if (password.length < 6) {
      return { isValid: false, message: '密码长度至少6位！' }
    }
    // 可以在这里添加更多密码强度检查...
    return { isValid: true }
  }
  // 确认密码验证（必须和密码一致）
  const validateRepassword = (password, repassword) => {
    if (!repassword) {
      return { isValid: false, message: '请输入确认密码！' }
    }
    if (repassword !== password) {
      return { isValid: false, message: '两次输入的密码不一致！' }
    }
    return { isValid: true }
  }
  // 注册请求函数
  const handleRegister = async (e) => {
    e.preventDefault()
    isLoading.value = true

    // 执行表单验证
    const usernameValidation = validateUsername(form.username)
    if (!usernameValidation.isValid) {
      ElMessage.error(usernameValidation.message)
      isLoading.value = false
      return // 阻止继续执行
    }

    const emailValidation = validateEmail(form.email)
    if (!emailValidation.isValid) {
      ElMessage.error(emailValidation.message)
      isLoading.value = false
      return
    }

    const passwordValidation = validatePassword(form.password)
    if (!passwordValidation.isValid) {
      ElMessage.error(passwordValidation.message)
      isLoading.value = false
      return
    }
    const repasswordValidation = validateRepassword(form.password, form.repassword)
    if (!repasswordValidation.isValid) {
      ElMessage.error(repasswordValidation.message)
      isLoading.value = false
      return
    }
    // 如果所有验证都通过，则继续执行注册逻辑
    try {
      isLoading.value = true
      // API调用
      await userRegisterApi(form)
      // 注册成功后，只保存用户名
      userStore.login(form.username)
      // 提示成功
      ElMessage.success('注册成功')
      // 成功后重置表单
      resetFormData()
      // 路由跳转
      router.push('/')
    } catch (error) {
      ElMessage.error('注册失败:' + error.message)
    } finally {
      isLoading.value = false
    }
  }

  // 登录请求函数
  const handleLogin = async (e) => {
    e.preventDefault() // 阻止表单默认提交
    isLoading.value = true // 显示loading
    // 执行表单验证
    const usernameValidation = validateUsername(form.username)
    if (!usernameValidation.isValid) {
      ElMessage.error(usernameValidation.message)
      isLoading.value = false
      return
    }

    const passwordValidation = validatePassword(form.password)
    if (!passwordValidation.isValid) {
      ElMessage.error(passwordValidation.message)
      isLoading.value = false
      return
    }
    // 调用登录API
    try {
      isLoading.value = true
      const response = await userLoginApi({
        username: form.username,
        password: form.password,
      })
      console.log(response)
      // 保存token到localStorage
      localStorage.setItem('token', response.data.token)

      // 登录成功后保存用户信息到store
      userStore.login({
        id: response.data.user.id,
        username: response.data.user.username,
      })
      // 提示成功
      ElMessage.success('登录成功')
      // 成功后重置表单
      resetFormData()
      // 跳转到首页
      router.push('/')
    } catch (error) {
      ElMessage.error('登录失败:' + (error.message || '请检查用户名和密码'))
    } finally {
      isLoading.value = false
    }
  }
</script>

<template>
  <!-- 引入Loading组件，通过isLoading控制显示 -->
  <Loading
    :visible="isLoading"
    :text="isLogin ? '登录中...' : '注册中...'"
  />
  <div class="bg"></div>
  <div class="login">
    <div class="login-banner">
      <div class="banner-content">
        <h3>欢迎回来</h3>
        <p>请登录您的账户，继续探索新鲜水果世界。</p>

        <div class="feature-item">
          <i class="bi bi-apple"></i>
          <div>
            <h4>品质保障</h4>
            <p>严选果园直供，多重质检确保新鲜安全</p>
          </div>
        </div>

        <div class="feature-item">
          <i class="bi bi-lightning-charge-fill"></i>
          <div>
            <h4>极速体验</h4>
            <p>一键登录，新鲜水果随时随地选购</p>
          </div>
        </div>
      </div>

      <div class="banner-footer">© 2025 asmoon 保留所有权利</div>
    </div>

    <!-- 动态渲染登录/注册子组件，传递核心方法和状态 -->
    <LoginForm
      v-if="isLogin"
      :showPassword="showPassword"
      :isLoading="isLoading"
      :form="form"
      @toggle-password="togglePassword"
      @change-form="changeForm"
      @submit="handleLogin"
    />
    <RegisterForm
      v-else
      :showPassword="showPassword"
      :isLoading="isLoading"
      :form="form"
      @toggle-password="togglePassword"
      @change-form="changeForm"
      @submit="handleRegister"
    />
  </div>
</template>

<style scoped lang="scss">
  .bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: url('@public/images/login.jpg') no-repeat center;
    background-size: cover;
  }

  .login {
    display: flex; // 左右分栏
    min-height: calc(100vh - 276px);
    overflow: hidden; // 避免内容溢出
    margin: 50px auto;
    max-width: 1200px;

    .login-banner {
      flex: 1; // 占比 50% 左右
      background: linear-gradient(120deg, #fff0f5, #c2185b); // 渐变背景
      color: #fff;
      padding: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-around;

      .banner-content {
        h3 {
          font-size: 30px;
          margin-bottom: 20px;
        }

        p {
          font-size: 14px;
          line-height: 1.6;
        }

        .feature-item {
          display: flex;
          align-items: flex-start;
          margin-top: 30px;
          margin-bottom: 25px;
          padding: 5px 5px 5px 0;

          i {
            font-size: 24px;
            margin-right: 12px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            padding: 10px;
          }

          h4 {
            font-size: 16px;
            margin-top: 4px;
          }

          p {
            font-size: 13px;
            margin: 0;
            opacity: 0.9;
          }
        }
      }

      .banner-footer {
        font-size: 12px;
        opacity: 0.8;
      }
    }
  }

  @media screen and (max-width: 768px) {
    .bg {
      height: calc(100vh - 60px);
    }

    .login {
      max-width: 90%; // 占满屏幕宽度
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 65px 0;

      .login-banner {
        display: none;
      }
    }
  }
</style>
