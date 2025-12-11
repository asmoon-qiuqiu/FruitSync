from pydantic import BaseModel
from schemas.userResponse import UserResponse


class UserLogin(BaseModel):
    """用户登录请求模型
    校验前端提交的登录数据，支持用户名/邮箱登录（后端统一处理匹配逻辑）
    字段说明：
        username: 用户名或邮箱（前端可输入其一，后端无需额外校验格式，注册时已验证）
        password: 登录密码（明文，后端加密后与数据库哈希密码对比）
    """

    username: str
    password: str


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
