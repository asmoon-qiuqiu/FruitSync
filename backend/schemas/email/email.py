from pydantic import BaseModel, EmailStr


# ---------------------- 密码重置-发送验证码请求 ----------------------
class SendCodeRequest(BaseModel):
    """向指定邮箱发送重置验证码的请求模型"""

    email: EmailStr  # 自动校验邮箱格式是否合法


# ---------------------- 密码重置-验证验证码请求 ----------------------
class VerifyCodeRequest(BaseModel):
    """验证验证码有效性的请求模型"""

    email: EmailStr
    code: str  # 6位数字验证码（接口内二次校验长度）


# ---------------------- 密码重置-提交新密码请求 ----------------------
class ResetPasswordRequest(BaseModel):
    """使用JWT令牌重置密码的请求模型"""

    token: str  # 验证验证码后获取的JWT重置令牌
    new_password: str  # 新密码（生产环境可添加复杂度校验）
