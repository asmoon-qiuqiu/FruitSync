"""
用户核心数据模型（SQLModel）
功能：定义数据库中用户表的结构与字段约束，存储用户的核心认证信息和状态数据
适用场景：用户注册、登录、个人信息管理等所有涉及用户数据的业务模块
技术说明：基于SQLModel实现，融合Pydantic的数据校验能力与SQLAlchemy的ORM操作能力，实现"模型即表结构"，
         支持自动生成数据库表、数据校验、CRUD操作等全流程功能
依赖：SQLModel（ORM模型与数据校验）、datetime（时间字段类型）、Field（字段约束定义）
"""

from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    """
    用户核心数据表模型（对应数据库表：users）
    存储用户的基础认证信息和账户状态，是系统的核心业务表之一
    表设计核心原则：
        1. 唯一性：用户名、邮箱作为用户标识，设置唯一约束避免重复注册
        2. 安全性：存储加密后的哈希密码（hashed_password），不存储明文密码
        3. 状态管控：通过is_active字段控制用户账户的启用/禁用状态
        4. 时间追踪：记录用户创建时间和更新时间，便于数据审计和追溯
    """

    # 显式指定数据库表名，若不指定则SQLModel默认使用类名小写复数（users），此处显式定义保持一致性
    __tablename__ = "users"

    # 主键字段：自增ID，default=None表示由数据库自动生成主键值
    id: int | None = Field(default=None, primary_key=True)
    # 用户名：唯一索引 + 长度约束
    username: str = Field(unique=True, index=True, max_length=50)
    # 邮箱：唯一索引 + 长度约束
    email: str = Field(unique=True, index=True, max_length=100)
    # 哈希密码：长度约束（存储加密后的密码）
    hashed_password: str = Field(max_length=255)
    # 账户状态：默认启用
    is_active: bool = Field(default=True)
    # 创建时间：动态生成当前时间，无需手动传入
    created_at: datetime = Field(default_factory=datetime.now)
    # 更新时间：动态生成当前时间，后续可更新
    updated_at: datetime = Field(default_factory=datetime.now)
