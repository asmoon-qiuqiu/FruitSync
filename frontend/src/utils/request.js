// src/utils/request.js
import axios from "axios"
import { ElMessage } from 'element-plus'

// 1. 创建Axios实例，配置基础参数
const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 5000,
    headers: {
        "Content-Type": "application/json;charset=utf-8",
    },
});

// 2. 请求拦截器
service.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error("请求拦截器错误：", error);
        return Promise.reject(error);
    }
);

// 3. 响应拦截器
service.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        console.error("响应错误：", error);
        let errorMsg = "请求失败，请稍后重试";

        if (error.response) {
            const { status, data } = error.response;
            const requestUrl = error.config?.url || '';

            switch (status) {
                case 400:
                    errorMsg = data.detail || "参数错误";
                    break;

                case 401:
                    const detail = data.detail || '';

                    // 优先判断：如果是登录接口，肯定是用户名密码错误
                    if (requestUrl.includes('/api/login')) {
                        errorMsg = detail || "用户名或密码错误";
                    }
                    // 再判断：如果错误信息明确提到用户名密码
                    else if (detail.includes('用户名或密码错误')) {
                        errorMsg = detail;
                    }
                    // 否则视为token过期或未登录
                    else {
                        errorMsg = "登录已过期，请重新登录";

                        // 清除本地存储
                        localStorage.removeItem('token');
                        localStorage.removeItem('user');

                        // ⚠️ 使用 window.location 跳转，避免循环依赖
                        // 检查当前路径，避免重复跳转
                        if (!window.location.pathname.includes('/login')) {
                            // 延迟跳转，确保提示信息能显示
                            setTimeout(() => {
                                window.location.href = '/login';
                            }, 1500);
                        }
                    }
                    break;

                case 403:
                    errorMsg = data.detail || "没有权限访问";
                    break;

                case 422:
                    errorMsg = data.detail?.[0]?.msg || "数据格式错误";
                    break;

                case 500:
                    errorMsg = "服务器内部错误";
                    break;

                default:
                    errorMsg = data.detail || data.message || errorMsg;
            }
        } else if (error.request) {
            errorMsg = "网络异常，请检查网络是否正常";
        }


        return Promise.reject({ message: errorMsg });
    }
);

export default service;