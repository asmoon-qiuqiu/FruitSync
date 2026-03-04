from pydantic import BaseModel, EmailStr, field_validator


# ---------------------- 密码重置-发送验证码请求 ----------------------
class SendCodeRequest(BaseModel):
    """向指定邮箱发送重置验证码的请求模型"""
    """
    校验前端提交的找回密码数据，仅需合法邮箱即可触发重置流程
    字段说明：
        email: 用户注册邮箱（Pydantic内置EmailStr自动校验格式）
    注：即使邮箱不存在，后端也会返回统一提示，避免用户信息泄露
    """
    email: EmailStr  # 自动校验邮箱格式是否合法


# ---------------------- 密码重置-验证验证码请求 ----------------------
class VerifyCodeRequest(BaseModel):
    """
    验证验证码有效性的请求模型
    校验前端提交的验证码验证数据，确保邮箱和验证码格式合法，接口内二次校验有效性
    字段说明：
        email: 接收验证码的用户邮箱（需符合RFC 5322标准格式，Pydantic自动校验）
        code: 6位数字验证码（接口内二次校验长度和有效性，仅格式校验不保证验证码正确）
    """
    email: EmailStr
    code: str  # 6位数字验证码（接口内二次校验长度）

# ---------------------- 密码重置-提交新密码请求 ----------------------
class ResetPasswordRequest(BaseModel):
    """使用JWT令牌重置密码的请求模型"""
    """
    校验前端提交的重置密码数据，包括重置令牌和新密码的合法性
    字段说明：
        token: 密码重置令牌（后端生成的唯一有效标识，用于验证重置权限）
        new_password: 新登录密码（规则与注册密码一致，至少6位字符）
    """
    token: str  # 验证验证码后获取的JWT重置令牌
    new_password: str  # 新密码（生产环境可添加复杂度校验）

    @field_validator("new_password")
    def password_validator(cls, value):
        """简单的密码复杂度校验示例（长度至少6位）"""
        if len(value) < 6:
            raise ValueError("密码长度必须至少6位")
        return value