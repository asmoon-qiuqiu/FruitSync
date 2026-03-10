<script setup>
import { ref, reactive, onBeforeUnmount } from 'vue'
import service from '@/utils/request'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 三步：1. 发送验证码 2. 验证验证码 3. 重置密码
const step = ref(1)
const isLoading = ref(false)
const countdown = ref(0)
let timer = null

const form = reactive({
  email: '',
  code: '',
  reset_token: '',
  new_password: '',
  confirm_password: '',
})

const router = useRouter()

const startCountdown = (sec = 60) => {
  countdown.value = sec
  if (timer) clearInterval(timer)
  timer = setInterval(() => {
    if (countdown.value > 0) countdown.value--
    else clearInterval(timer)
  }, 1000)
}

const sendCode = async () => {
  if (!form.email) return ElMessage.warning('请输入注册邮箱')
  isLoading.value = true
  try {
    const res = await service({ url: '/api/password/send-code', method: 'POST', data: { email: form.email } })
    ElMessage.success(res.data?.message || '验证码已发送')
    if (res.data?.debug_code) console.debug('debug_code:', res.data.debug_code)
    startCountdown(60)
    step.value = 2
  } catch (err) {
    ElMessage.error(err?.message || err.message || '发送验证码失败')
  } finally {
    isLoading.value = false
  }
}

const verifyCode = async () => {
  if (!form.code) return ElMessage.warning('请输入验证码')
  isLoading.value = true
  try {
    const res = await service({ url: '/api/password/verify-code', method: 'POST', data: { email: form.email, code: form.code } })
    ElMessage.success(res.data?.message || '验证码验证成功')
    form.reset_token = res.data?.reset_token
    step.value = 3
  } catch (err) {
    ElMessage.error(err.message || '验证码验证失败')
  } finally {
    isLoading.value = false
  }
}

const resetPassword = async () => {
  if (!form.new_password || form.new_password.length < 6) return ElMessage.warning('新密码至少6位')
  if (form.new_password !== form.confirm_password) return ElMessage.warning('两次输入的密码不一致')
  if (!form.reset_token) return ElMessage.warning('缺少重置令牌，请先验证验证码')

  isLoading.value = true
  try {
    const res = await service({ url: '/api/password/reset', method: 'POST', data: { token: form.reset_token, new_password: form.new_password } })
    ElMessage.success(res.data?.message || '密码重置成功')
    router.push('/login')
  } catch (err) {
    ElMessage.error(err.message || '重置密码失败')
  } finally {
    isLoading.value = false
  }
}

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="reset-wrapper">
    <form class="reset-form" @submit.prevent>
      <h3>重置密码</h3>
      <p v-if="step === 1">请输入您注册时使用的邮箱，系统会发送验证码到该邮箱。</p>
      <p v-else-if="step === 2">请输入邮箱收到的6位验证码。</p>
      <p v-else>设置新密码（至少6位）</p>

      <div class="field">
        <input type="email" placeholder="邮箱" v-model="form.email" :disabled="isLoading || step !== 1" />
      </div>

      <div v-if="step >= 2" class="field">
        <input type="text" placeholder="验证码" maxlength="6" v-model="form.code" :disabled="isLoading || step !== 2" />
        <button class="small" type="button" @click="sendCode" :disabled="countdown > 0 || isLoading">
          <span v-if="countdown > 0">重新发送 ({{ countdown }}s)</span>
          <span v-else>重新发送</span>
        </button>
      </div>

      <div v-if="step === 3" class="field">
        <input type="password" placeholder="新密码" v-model="form.new_password" :disabled="isLoading" />
      </div>
      <div v-if="step === 3" class="field">
        <input type="password" placeholder="确认新密码" v-model="form.confirm_password" :disabled="isLoading" />
      </div>

      <div class="actions">
        <button v-if="step === 1" type="button" @click="sendCode" :disabled="isLoading">{{ isLoading ? '发送中...' :
          '发送验证码' }}</button>
        <button v-else-if="step === 2" type="button" @click="verifyCode" :disabled="isLoading">{{ isLoading ? '验证中...' :
          '验证验证码' }}</button>
        <button v-else type="button" @click="resetPassword" :disabled="isLoading">{{ isLoading ? '提交中...' : '重置密码'
        }}</button>
      </div>

      <div class="extra">
        <router-link to="/login">返回登录</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped lang="scss">
.reset-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  min-height: calc(100vh - 176px);
  background: url('@public/images/login.jpg') no-repeat center;
  background-size: cover;
  background-attachment: fixed;
}

.reset-form {
  width: 420px;
  padding: 30px;
  background: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;

  h3 {
    margin: 0 0 6px
  }

  p {
    color: #666;
    margin: 0 0 18px
  }

  .field {
    display: flex;
    align-items: center;
    margin-bottom: 12px;

    input {
      flex: 1;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid #f1f2f5;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .small {
      margin-left: 8px;
      padding: 8px 10px;
      border-radius: 6px;
      border: none;
      background: #db729b;
      color: #fff;
      cursor: pointer;
    }
  }

  .actions {
    margin-top: 8px;

    button {
      width: 100%;
      padding: 12px 18px;
      border-radius: 10px;
      border: none;
      background: #db729b;
      color: #fff;
      font-size: 16px;
    }
  }

  .extra {
    margin-top: 12px;
    text-align: center;

    a {
      color: #2b99fc
    }
  }
}

@media screen and (max-width: 768px) {
  .reset-form {
    width: 100%;
    padding: 20px
  }
}
</style>
