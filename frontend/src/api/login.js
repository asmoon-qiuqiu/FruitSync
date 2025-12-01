import service from "@/utils/request";

/**
 * 用户登录接口
 * @param {Object} data - 登录参数（用户名 + 密码）
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @returns {Promise} - 返回登录结果（包含 Token 和用户信息）
 */


export const userLoginApi = (data) => {
    return service({
        url: "/api/login",
        method: "POST",
        data: data, //传递登录表单数据
    })
};