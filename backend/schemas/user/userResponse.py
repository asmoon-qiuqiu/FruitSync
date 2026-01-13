from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    """用户信息响应模型
    作为用户数据的对外输出模板，统一返回用户的核心公开信息，避免敏感数据泄露
    字段说明：
        id: 用户唯一标识（数据库自增主键）
        username: 用户名（用户注册时设置的昵称/账号）
        email: 用户注册邮箱（已通过格式校验的合法邮箱）
        is_active: 用户账号状态（True-正常/激活，False-禁用/未激活）
        created_at: 用户注册时间（数据库记录的创建时间，UTC/本地时间统一）
    补充：
        该模型会被其他响应模型（如LoginResponse）嵌套使用，实现数据复用
    """

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
