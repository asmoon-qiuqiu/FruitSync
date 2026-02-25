"""
验证码存储模型（SQLModel）
功能：定义数据库中验证码记录的表结构，存储邮箱验证码及其状态信息
适用场景：密码重置验证码、注册验证码等需要临时存储验证信息的场景
技术说明：验证码具有时效性，建议定期清理过期记录或设置数据库自动过期策略
依赖：SQLModel（ORM模型）、datetime（时间字段类型）、Field（字段约束定义）
"""

from sqlmodel import SQLModel, Field
from datetime import datetime


class VerificationCode(SQLModel, table=True):
    """
    验证码记录数据表模型（对应数据库表：verification_codes）
    存储用户邮箱验证码的核心信息，用于验证用户身份
    表设计核心原则：
        1. 关联性：通过邮箱关联用户，支持快速查询
        2. 时效性：设置有效期字段，过期验证码自动失效
        3. 唯一性：验证码字段索引，加速查询验证
        4. 状态管控：is_used标记验证码是否已使用，避免重复使用
    """

    # 数据库表名显式指定（若不指定，SQLModel会默认使用类名小写复数形式）
    __tablename__ = "verification_codes"

    # 主键字段：自增ID，默认值为None表示数据库自动生成
    id: int | None = Field(default=None, primary_key=True)
    # 邮箱字段：索引加速查询，最大长度100
    email: str = Field(index=True, max_length=100)
    # 验证码：6位数字，索引加速查询
    code: str = Field(index=True, max_length=6)
    # 验证码过期时间：用于判断验证码是否有效
    expires_at: datetime
    # 验证码使用状态：默认未使用（False），使用后标记为已使用（True）
    is_used: bool = Field(default=False)
    # 验证码类型：password_reset-密码重置，register-注册验证等
    code_type: str = Field(default="password_reset", max_length=20)
    # 记录创建时间：默认使用当前时间
    created_at: datetime = Field(default_factory=datetime.now)
