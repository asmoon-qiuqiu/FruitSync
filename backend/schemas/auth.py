"""
用户认证模块数据校验模型（Pydantic v2）
功能：定义用户注册、登录、密码重置的请求参数校验规则，以及登录成功的响应数据结构
作用：1. 自动校验前端提交的请求数据合法性，返回标准化错误提示
     2. 统一后端响应数据格式，实现前后端数据契约一致
     3. 为FastAPI自动生成接口文档提供数据模型支撑
模块依赖：Pydantic（数据校验）、re（正则匹配）、自定义用户响应模型UserResponse
"""

from pydantic import BaseModel, EmailStr, field_validator
from schemas.user import UserResponse  # 导入用户信息响应模型（隐藏敏感字段）


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
