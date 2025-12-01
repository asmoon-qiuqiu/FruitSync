"""
用户模块响应数据模型（Pydantic v2）
功能：定义用户信息的标准化响应结构，用于对外返回用户的公开数据（隐藏敏感字段）
适用场景：登录成功、用户信息查询、个人中心数据展示等接口的响应体
设计原则：仅包含用户公开的非敏感信息，排除哈希密码、令牌等隐私数据
依赖：Pydantic（数据模型基类）、datetime（时间类型）
"""

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


class LoginResponse(BaseModel):
    """用户登录响应模型
    定义登录成功后后端返回给前端的标准化数据结构
    字段说明：
        message: 操作提示信息（如"登录成功"）
        user: 用户公开信息（从UserResponse导入，隐藏哈希密码等敏感字段）
        token: 身份认证令牌（JWT/自定义令牌，前端后续请求需携带此令牌）
    """

    message: str
    user: UserResponse
    token: str
