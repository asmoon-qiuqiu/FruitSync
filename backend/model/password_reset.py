"""
密码重置模块数据模型（SQLModel）
功能：定义数据库中密码重置记录的表结构与字段约束，实现密码重置令牌的持久化存储
适用场景：用户忘记密码时，生成重置令牌并记录令牌的有效期、使用状态、关联用户等信息
技术说明：基于SQLModel实现，同时支持Pydantic数据校验和SQLAlchemy数据库操作，实现"模型即表结构"
依赖：SQLModel（ORM模型与数据校验）、datetime（时间字段类型）、Field（字段约束定义）
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated


class PasswordReset(SQLModel, table=True):
    """
    密码重置记录数据表模型（对应数据库表：password_resets）
    存储用户密码重置令牌的核心信息，用于验证令牌的有效性、有效期和使用状态
    表设计核心原则：
        1. 关联用户：通过user_id与用户表（users）建立外键关联，明确令牌归属
        2. 唯一性：token字段唯一，避免重复令牌导致的业务冲突
        3. 时效性：expires_at记录令牌有效期，防止令牌永久有效
        4. 状态管控：is_used标记令牌是否已使用，避免重复重置密码
    """

    # 数据库表名显式指定（若不指定，SQLModel会默认使用类名小写复数形式）
    __tablename__ = "password_resets"

    # 主键字段：自增ID，默认值为None表示数据库自动生成
    id: int | None = Field(default=None, primary_key=True)
    # 外键字段：关联用户表的id，索引加速查询，明确该重置记录归属的用户
    user_id: int = Field(foreign_key="users.id", index=True)
    # 重置令牌：唯一索引，最大长度100，保证令牌的唯一性且限制存储长度
    token: str = Field(unique=True, index=True, max_length=100)
    # 令牌过期时间：无额外约束，需手动传入
    expires_at: datetime
    # 令牌使用状态：默认未使用（False），使用后标记为已使用（True），防止重复使用
    is_used: bool = Field(default=False)
    # 记录创建时间：默认使用当前时间，无需手动传入，记录令牌的生成时间
    created_at: datetime = Field(default_factory=datetime.now)
