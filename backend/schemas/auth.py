from pydantic import BaseModel, EmailStr, field_validator


class PasswordResetRequest(BaseModel):
    """忘记密码请求模型
    校验前端提交的找回密码数据，仅需合法邮箱即可触发重置流程
    字段说明：
        email: 用户注册邮箱（Pydantic内置EmailStr自动校验格式）
    注：即使邮箱不存在，后端也会返回统一提示，避免用户信息泄露
    """

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """重置密码确认请求模型
    校验前端提交的重置密码数据，包括重置令牌和新密码的合法性
    字段说明：
        token: 密码重置令牌（后端生成的唯一有效标识，用于验证重置权限）
        new_password: 新登录密码（规则与注册密码一致，至少6位字符）
    """

    token: str
    new_password: str

    @field_validator("new_password")
    def password_validator(cls, v):
        """新密码自定义校验器：与注册密码规则保持一致，至少6个字符"""
        if len(v) < 6:
            raise ValueError("密码长度至少6个字符")
        return v
