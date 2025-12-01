import re
from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    """用户注册请求模型
    校验前端提交的注册数据，包括用户名、邮箱、密码的格式与规则
    字段说明：
        username: 用户名（3-50位，仅含字母、数字、下划线、中文）
        email: 注册邮箱（Pydantic内置EmailStr自动校验邮箱格式）
        password: 登录密码（至少6位字符）
    """

    username: str
    email: EmailStr
    password: str
    model_config = {"extra": "forbid"}

    @field_validator("username")
    def username_validator(cls, v):
        """用户名自定义校验器
        规则1：长度限制在3-50个字符之间
        规则2：字符仅允许字母、数字、下划线、中文
        """
        if len(v) < 3 or len(v) > 10:
            raise ValueError("用户名长度必须在3-50个字符之间")
        if not re.match(r"^[a-zA-Z0-9_\u4e00-\u9fa5]+$", v):
            raise ValueError("用户名只能包含字母、数字、下划线和中文")
        return v

    @field_validator("password")
    def password_validator(cls, v):
        """密码自定义校验器：密码长度至少6个字符"""
        if len(v) < 6:
            raise ValueError("密码长度至少6个字符")
        return v
