import re
from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    """用户注册请求模型
    校验前端提交的注册数据，包括用户名、邮箱、密码的格式与规则
    字段说明：
        username: 用户名（3-10位，仅含字母、数字、下划线、中文）
        email: 注册邮箱（Pydantic内置EmailStr自动校验邮箱格式）
        password: 登录密码（至少6位字符）
        repassword: 确认密码（必须和password一致）
    """

    username: str
    email: EmailStr
    password: str
    repassword: str
    model_config = {"extra": "forbid"}

    @field_validator("username")
    def username_validator(cls, v):
        """用户名自定义校验器
        规则1：长度限制在3-10个字符之间（和前端保持一致）
        规则2：字符仅允许字母、数字、下划线、中文
        """
        # 去除首尾空格（避免用户输入空格导致校验失败）
        v_stripped = v.strip()
        if len(v_stripped) < 3 or len(v_stripped) > 10:
            raise ValueError("用户名长度必须在3-10个字符之间")
        if not re.match(r"^[a-zA-Z0-9_\u4e00-\u9fa5]+$", v_stripped):
            raise ValueError("用户名只能包含字母、数字、下划线和中文")
        return v_stripped  # 返回去空格后的用户名，避免存储空格

    @field_validator("password")
    def password_validator(cls, v):
        """密码自定义校验器：密码长度至少6个字符"""
        if len(v) < 6:
            raise ValueError("密码长度至少6个字符")
        return v

    @field_validator("repassword")
    def repassword_validator(cls, v, values):
        """确认密码校验器：必须和password一致"""
        # values 是已校验通过的字段字典（注意字段校验顺序：password先于repassword）
        password = values.data.get("password")  # Pydantic v2 用 values.data 获取字段值
        if password and v != password:
            raise ValueError("两次输入的密码不一致")
        return v
