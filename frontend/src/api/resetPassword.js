/**
 * 发送验证码（密码重置）
 * @param {Object} data 请求参数（包含email）
 * @returns {Promise} 请求Promise对象
 */
export const sendCodeApi = (data) => {
  return service({
    url: '/api/password/send-code',
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
    url: '/api/password/verify-code',
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
    url: '/api/password/reset',
    method: 'POST',
    data: data,
  })
};