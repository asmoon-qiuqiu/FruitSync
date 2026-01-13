import jwt
from datetime import datetime, timedelta, timezone
from config import (
    RESET_TOKEN_EXPIRE_HOURS,
    ACCESS_TOKEN_EXPIRE_HOURS,
    SECRET_KEY,
    ALGORITHM,
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """生成JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_reset_token(data: dict):
    """生成密码重置 Token（1小时过期）"""
    expire = datetime.now(timezone.utc) + timedelta(hours=RESET_TOKEN_EXPIRE_HOURS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_reset_expiration() -> datetime:
    """获取重置令牌过期时间"""
    return datetime.now(timezone.utc) + timedelta(hours=RESET_TOKEN_EXPIRE_HOURS)
