<script setup>
  const props = defineProps({
    showPassword: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    form: {
      // 接收父组件的form
      type: Object,
      required: true,
    },
  })

  const emit = defineEmits(['toggle-password', 'change-form', 'submit'])
  // 处理表单提交，传递原生事件和表单数据
  const handleSubmit = (e) => {
    emit('submit', e)
  }
</script>

<template>
  <form
    class="login-form"
    @submit="handleSubmit"
  >
    <h3>账户登录</h3>
    <p>请输入您的账户信息</p>
    <div class="login-name">
      <input
        type="text"
        name="username"
        placeholder="用户名"
        v-model="form.username"
        :disabled="isLoading"
        novalidate
      />
    </div>
    <div class="login-password">
      <input
        class="pwd"
        :type="showPassword ? 'text' : 'password'"
        name="password"
        placeholder="密码"
        v-model="form.password"
        :disabled="isLoading"
        novalidate
      />
      <i
        class="bi bi-eye"
        @click="emit('toggle-password')"
        v-show="showPassword"
      ></i>
      <i
        class="bi bi-eye-slash"
        @click="emit('toggle-password')"
        v-show="!showPassword"
      ></i>
    </div>
    <div class="login-button">
      <div class="re-pwd">
        <a
          class="register"
          @click="emit('change-form')"
        >
          立即注册
        </a>
        <a href="#">忘记密码？</a>
      </div>
      <button
        type="submit"
        name="login"
        :disabled="isLoading"
      >
        {{ isLoading ? '加载中...' : '登录' }}
      </button>
    </div>
  </form>
</template>

<style scoped lang="scss">
  .login-form {
    flex: 1; // 与左侧占比一致
    padding: 40px;
    background: #f9fafb;
    display: flex;
    flex-direction: column;
    justify-content: center;

    .login-name {
      & [type='text'] {
        border-radius: 10px;
        border: 1px solid #f1f2f5;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        padding: 10px;
        width: 100%;
      }
    }

    .login-password {
      position: relative;

      .pwd {
        border-radius: 10px;
        border: 1px solid #f1f2f5;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        padding: 10px;
        width: 100%;
        padding-right: 35px;

        // 隐藏 Chrome/Safari 等 WebKit 内核浏览器的默认眼睛图标
        &::-webkit-credentials-cramble-button,
        &::-webkit-reveal {
          display: none;
        }

        // 隐藏 Edge/IE 浏览器的默认眼睛图标
        &::-ms-reveal {
          display: none;
        }
      }

      .bi {
        position: absolute;
        right: 4%;
        top: 38%;
        transform: translateY(-50%);
        cursor: pointer;
      }
    }

    .login-button {
      & [type='submit'] {
        background-color: #db729b;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 12px 25px;
        text-align: center;
        font-size: 18px;
        width: 100%;

        &:hover {
          background-color: #c2185b;
          cursor: pointer;
        }
      }

      .re-pwd,
      a {
        text-decoration: none;
        color: #2b99fc;

        .register {
          float: right;
          margin-bottom: 20px;
          cursor: pointer;
        }
      }
    }
  }

  @media screen and (max-width: 768px) {
    .login-form {
      max-width: 400px;
      margin: 0;
      padding: 30px 20px;
    }
  }
</style>
