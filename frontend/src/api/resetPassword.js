/**
 * 发送验证码（密码重置）
 * @param {Object} data 请求参数（包含email）
 * @returns {Promise} 请求Promise对象
 */

import service from "@/utils/request"

export const sendCodeApi = (data) => {
  return service({
    url: '/password/send-code',
    method: 'POST',
    data: data,
  })
};

/**
 * 验证验证码（密码重置）
 * @param {Object} data 请求参数（包含email/code）
 * @returns {Promise} 请求Promise对象
 */
export const verifyCodeApi = (data) => {
  return service({
    url: '/password/verify-code',
    method: 'POST',
    data: data,
  })
};

/**
 * 重置密码
 * @param {Object} data 请求参数（包含token/new_password）
 * @returns {Promise} 请求Promise对象
 */
export const resetPasswordApi = (data) => {
  return service({
    url: '/password/reset',
    method: 'POST',
    data: data,
  })
};