import { ref } from 'vue';

/**
 * 登录表单辅助方法封装：处理登录注册切换、密码显示隐藏逻辑
 * @returns {Object} 包含响应式变量和操作方法的对象
 */
export function useAuthForm() {
    // 控制登录注册切换的响应式变量，默认显示登录表单
    const isLogin = ref(true);

    // 切换登录/注册表单的方法
    const changeForm = () => {
        isLogin.value = !isLogin.value;
    };

    // 控制密码框显示/隐藏的响应式变量，默认隐藏密码
    const showPassword = ref(false);

    // 切换密码可见性的方法
    const togglePassword = () => {
        showPassword.value = !showPassword.value;
    };

    // 对外暴露变量和方法
    return {
        isLogin,
        changeForm,
        showPassword,
        togglePassword
    };
}

