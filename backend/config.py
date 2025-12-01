# ==================== 配置 ====================

import secrets


# 数据库连接信息
# DATABASE_URL = "mysql+pymysql://root:23718@localhost:3306/fruit_db" # 同步
DATABASE_URL = "mysql+aiomysql://root:23718@localhost:3306/fruit_db"  # 异步
# 密钥-生成一个 32 字节的密钥，返回 64 个字符的十六进制字符串
SECRET_KEY = secrets.token_hex(32)
# JWT签名算法
ALGORITHM = "HS256"
# 过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 12  # 登录token过期时间-12小时
RESET_TOKEN_EXPIRE_HOURS = 1  # 重置密码token过期时间
