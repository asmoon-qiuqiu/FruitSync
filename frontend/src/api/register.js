import service from "@/utils/request"; // 导入封装后的Axios实例

/**
 * 用户注册接口
 * @param {Object} data 注册表单数据（包含username/email/password）
 * @returns {Promise} 请求Promise对象
 */

export const userRegisterApi = (data) => {
    return service({
        url: "/api/register",
        method: "POST",
        data: data, // 传递注册表单数据
    })
};