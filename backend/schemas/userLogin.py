from pydantic import BaseModel


class UserLogin(BaseModel):
    """用户登录请求模型
    校验前端提交的登录数据，支持用户名/邮箱登录（后端统一处理匹配逻辑）
    字段说明：
        username: 用户名或邮箱（前端可输入其一，后端无需额外校验格式，注册时已验证）
        password: 登录密码（明文，后端加密后与数据库哈希密码对比）
    """

    username: str
    password: str
